import re, json, asyncio, aiohttp, aiofiles, argparse

parser = argparse.ArgumentParser()
parser.add_argument('-y', dest='lzy_ylogin')
parser.add_argument('-p', dest='lzy_phpdisk_info')
parser.add_argument('-f', dest='lzy_folder_id')
args = parser.parse_args()

cookies = {'ylogin': args.lzy_ylogin, 'phpdisk_info': args.lzy_phpdisk_info}
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0'}

async def upload(filename):
    url = "https://pc.woozooo.com/fileup.php"
    fields={"task": "1", "folder_id": args.lzy_folder_id, "id": "WU_FILE_0", "name": filename, "type": "application/octet-stream"}
    with aiohttp.MultipartWriter("form-data") as mpwriter:
        part = mpwriter.append(open(filename, 'rb'))
        part.set_content_disposition('form-data', name="upload_file", filename=filename, quote_fields=False)
        for key, value in fields.items():
            part = mpwriter.append(value)
            part.set_content_disposition('form-data', name=key)
        headers["Content-Type"] = mpwriter.content_type
    async with aiohttp.ClientSession() as session:
        async with session.post(url=url, headers=headers, data=mpwriter, cookies=cookies, timeout=0) as req:
            resp = await req.read()
            resp = json.loads(resp)["info"]
            print(filename + resp)

async def download(url, filename):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                f = await aiofiles.open(filename, mode='wb')
                await f.write(await resp.read())
                await f.close()

async def main():
    url = "https://pc.woozooo.com/doupload.php"
    data = {'task': 5, 'folder_id': args.lzy_folder_id, 'pg': 1}
    async with aiohttp.ClientSession() as session:
        async with session.post(url=url, data=data, headers=headers, cookies=cookies) as req:
            files = await req.text()
            files = files.encode('utf-8').decode('unicode_escape')
        url = "https://ftp.mozilla.org/pub/firefox/releases/"
        async with session.get(url=url) as req:
            resp = await req.text()
        resp1 = re.findall(r'(?<=">)\d+\.\d+(?=/<)', resp)
        resp1.sort(key=lambda x: (int(x.split(".")[0]), int(x.split(".")[1])))
        resp1 = resp1[-1]
        resp2 = re.findall(r'(?<=">)\d+\.\d+\.\d+(?=/<)', resp)
        resp2.sort(key=lambda x: (int(x.split(".")[0]), int(x.split(".")[1]), int(x.split(".")[2])))
        resp2 = resp2[-1]
        if resp1.split(".")[0] == resp2.split(".")[0]:
            resp = resp2
        else:
            resp = resp1
        url32 = "https://ftp.mozilla.org/pub/firefox/releases/" + resp + "/win32/zh-CN/Firefox%20Setup%20" + resp + ".exe"
        url64 = "https://ftp.mozilla.org/pub/firefox/releases/" + resp + "/win64/zh-CN/Firefox%20Setup%20" + resp + ".exe"
        resp32 = "firefox-" + resp + "-win32.exe"
        resp64 = "firefox-" + resp + "-win64.exe"
        if files.find(resp32) == -1 or files.find(resp64) == -1:
            await download(url32, resp32)
            await download(url64, resp64)
        if files.find(resp32) == -1:
            await upload(resp32)
        else:
            print(resp32 + "已存在")
        if files.find(resp64) == -1:
            await upload(resp64)
        else:
            print(resp64 + "已存在")

        url = "https://api.github.com/repos/mozilla-mobile/fenix/releases/latest"
        async with session.get(url=url) as req:
            resp = await req.read()
        resp = json.loads(resp)["tag_name"].replace("v", "")
        if resp.find("rc") == -1:
            url32m = "https://github.com/mozilla-mobile/fenix/releases/download/v" + resp + "/fenix-" + resp + "-armeabi-v7a.apk"
            url64m = "https://github.com/mozilla-mobile/fenix/releases/download/v" + resp + "/fenix-" + resp + "-arm64-v8a.apk"
            resp32m = "fenix-" + resp + "-armeabi-v7a-官方版.apk"
            resp64m = "fenix-" + resp + "-arm64-v8a-官方版.apk"
            if files.find(resp32m) == -1 or files.find(resp64m) == -1:
                await download(url32m, resp32m)
                await download(url64m, resp64m)
            if files.find(resp32m) == -1:
                await upload(resp32m)
            else:
                print(resp32m + "已存在")
            if files.find(resp64m) == -1:
                await upload(resp64m)
            else:
                print(resp64m + "已存在")

asyncio.get_event_loop().run_until_complete(main())