#!/usr/bin/env python3

#Copyright © 2023 <copyright holders>
#Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import argparse, subprocess, gzip, os, shutil, re, zipfile, hashlib, platform, requests, tqdm

def get_download_dir():
    download_loc = ""
    if os.environ.get("XDG_CACHE_HOME", None) is None:
        download_loc = os.path.join('/', "home", os.environ.get("SUDO_USER", os.environ["USER"]), ".cache", "redroid", "downloads")
    else:
        download_loc = os.path.join(os.environ["XDG_CACHE_HOME"], "redroid", "downloads")
    if not os.path.exists(download_loc):
        os.makedirs(download_loc)
    return download_loc

def run(args):
    result = subprocess.run(args=args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.stderr:
        print(result.stderr.decode("utf-8"))
        raise subprocess.CalledProcessError(
                    returncode = result.returncode,
                    cmd = result.args,
                    stderr = result.stderr
                )
    return result

def download_file(url, f_name):
    md5 = ""
    response = requests.get(url, stream=True)
    total_size_in_bytes = int(response.headers.get('content-length', 0))
    block_size = 1024  # 1 Kibibyte
    progress_bar = tqdm.tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
    with open(f_name, 'wb') as file:
        for data in response.iter_content(block_size):
            progress_bar.update(len(data))
            file.write(data)
    progress_bar.close()
    with open(f_name, "rb") as f:
        bytes = f.read()
        md5 = hashlib.md5(bytes).hexdigest()
    if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
        raise ValueError("Something went wrong while downloading")
    return md5

def host():
    machine = platform.machine()

    mapping = {
        "i686": ("x86", 32),
        "x86_64": ("x86_64", 64),
        "aarch64": ("arm64-v8a", 64),
        "armv7l": ("armeabi-v7a", 32),
        "armv8l": ("armeabi-v7a", 32)
    }
    if machine in mapping:
        # if mapping[machine] == "x86_64":
        #     with open("/proc/cpuinfo") as f:
        #         if "sse4_2" not in f.read():
        #             print("x86_64 CPU does not support SSE4.2, falling back to x86...")
        #             return ("x86", 32)
        return mapping[machine]
    raise ValueError("platform.machine '" + machine + "'"
                     " architecture is not supported")

class bcolors:
    RED = '\033[31m'
    YELLOW = '\033[33m'
    GREEN = '\033[32m'
    ENDC = '\033[0m'

def print_color(str, color):
    print(color+str+bcolors.ENDC)

class General:
    def download(self):
        loc_md5 = ""
        if os.path.isfile(self.dl_file_name):
            with open(self.dl_file_name,"rb") as f:
                bytes = f.read()
                loc_md5 = hashlib.md5(bytes).hexdigest()
        while not os.path.isfile(self.dl_file_name) or loc_md5 != self.act_md5:
            if os.path.isfile(self.dl_file_name):
                os.remove(self.dl_file_name)
                print_color("md5 mismatches, redownloading now ....",bcolors.YELLOW)
            loc_md5 = download_file(self.dl_link, self.dl_file_name)
        
    def extract(self):
        print_color("Extracting archive...", bcolors.GREEN)
        print(self.dl_file_name)
        print(self.extract_to)
        with zipfile.ZipFile(self.dl_file_name) as z:
            z.extractall(self.extract_to)
    def copy(self):
        pass
    def install(self):
        # pass
        self.download()
        self.extract()
        self.copy()

class Magisk(General):
    download_loc = get_download_dir()
    dl_link = "https://raw.githubusercontent.com/lindongbin/gt/master/app-release.apk"
    dl_file_name = os.path.join(download_loc, "magisk.apk")
    extract_to = "/tmp/magisk_unpack"
    copy_dir = "./magisk"
    magisk_dir = os.path.join(copy_dir, "system", "etc", "init", "magisk")
    machine = host()
    oringinal_bootanim = """
service bootanim /system/bin/bootanimation
    class core animation
    user graphics
    group graphics audio
    disabled
    oneshot
    ioprio rt 0
    task_profiles MaxPerformance
    
"""
    bootanim_component = """
on post-fs-data
    start logd
    exec u:r:su:s0 root root -- /system/etc/init/magisk/magisk{arch} --auto-selinux --setup-sbin /system/etc/init/magisk
    exec u:r:su:s0 root root -- /system/etc/init/magisk/magiskpolicy --live --magisk "allow * magisk_file lnk_file *"
    mkdir /sbin/.magisk 700
    mkdir /sbin/.magisk/mirror 700
    mkdir /sbin/.magisk/block 700
    copy /system/etc/init/magisk/config /sbin/.magisk/config
    rm /dev/.magisk_unblock
    exec u:r:su:s0 root root -- /sbin/magisk --auto-selinux --post-fs-data
    wait /dev/.magisk_unblock 40
    rm /dev/.magisk_unblock

on zygote-start
    exec u:r:su:s0 root root -- /sbin/magisk --auto-selinux --service

on property:sys.boot_completed=1
    mkdir /data/adb/magisk 755
    exec u:r:su:s0 root root -- /sbin/magisk --auto-selinux --boot-complete
    exec -- /system/bin/sh -c "if [ ! -e /data/data/io.github.huskydg.magisk ] ; then pm install /system/etc/init/magisk/magisk.apk ; fi"
   
on property:init.svc.zygote=restarting
    exec u:r:su:s0 root root -- /sbin/magisk --auto-selinux --zygote-restart
   
on property:init.svc.zygote=stopped
    exec u:r:su:s0 root root -- /sbin/magisk --auto-selinux --zygote-restart
    """.format(arch=machine[1])

    def download(self):
        if os.path.isfile(self.dl_file_name):
            os.remove(self.dl_file_name)
        print_color("Downloading latest Magisk-Delta now .....", bcolors.GREEN)
        download_file(self.dl_link, self.dl_file_name)    

    def copy(self):
        if os.path.exists(self.copy_dir):
            shutil.rmtree(self.copy_dir)
        if not os.path.exists(self.magisk_dir):
            os.makedirs(self.magisk_dir, exist_ok=True)

        if not os.path.exists(os.path.join(self.copy_dir, "sbin")):
            os.makedirs(os.path.join(self.copy_dir, "sbin"), exist_ok=True)

        print_color("Copying magisk libs now ...", bcolors.GREEN)
        
        lib_dir = os.path.join(self.extract_to, "lib", self.machine[0])
        for parent, dirnames, filenames in os.walk(lib_dir):
            for filename in filenames:
                o_path = os.path.join(lib_dir, filename)  
                filename = re.search('lib(.*)\.so', filename)
                n_path = os.path.join(self.magisk_dir, filename.group(1))
                shutil.copyfile(o_path, n_path)
                run(["chmod", "+x", n_path])
        shutil.copyfile(self.dl_file_name, os.path.join(self.magisk_dir,"magisk.apk") )

        # Updating Magisk from Magisk manager will modify bootanim.rc, 
        # So it is necessary to backup the original bootanim.rc.
        bootanim_path = os.path.join(self.copy_dir, "system", "etc", "init", "bootanim.rc")
        gz_filename = os.path.join(bootanim_path)+".gz"
        with gzip.open(gz_filename,'wb') as f_gz:
            f_gz.write(self.oringinal_bootanim.encode('utf-8'))
        with open(bootanim_path, "w") as initfile:
            initfile.write(self.oringinal_bootanim+self.bootanim_component)

        os.chmod(bootanim_path, 0o644)

def main():
    dockerfile = ""
    tags = []
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-a', '--android-version',
                        dest='android',
                        help='Specify the Android version to build',
                        default='13.0.0_64only',
                        choices=['13.0.0', '13.0.0_64only', '12.0.0', '12.0.0_64only', '11.0.0', '10.0.0', '9.0.0', '8.1.0'])
    parser.add_argument('-m', '--install-magisk', dest='magisk',
                        help='Install Magisk ( Bootless )',
                        action='store_true')
    parser.add_argument('-c', '--container', 
                        dest='container',
                        default='docker',
                        help='Specify container type', 
                        choices=['docker', 'podman'])

    args = parser.parse_args()
    dockerfile = dockerfile + \
        "FROM redroid/redroid:{}-latest\n".format(
            args.android)
    tags.append(args.android)
    if args.magisk:
        Magisk().install()
        dockerfile = dockerfile+"COPY magisk /\n"
        tags.append("magisk")
    print("\nDockerfile\n"+dockerfile)
    with open("./Dockerfile", "w") as f:
        f.write(dockerfile)
    new_image_name = "redroid/redroid:"+"_".join(tags)
    subprocess.run([args.container, "build", "-t", new_image_name, "."])
    print_color("Successfully built {}".format(
        new_image_name), bcolors.GREEN)

if __name__ == "__main__":
    main()
