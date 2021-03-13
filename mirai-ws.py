import json, re, random, datetime, hashlib, hmac, time, urllib, base64, asyncio, aiohttp, traceback
from lxml import etree

async def atpget(id):
    try:
        async with aiohttp.ClientSession() as session:
            url = ""
            headers = {'Content-Type': 'application/json'}
            id = json.dumps({'mirai':id})
            auth = aiohttp.BasicAuth(login='', password='')
            async with session.post(url=url, data=id, auth=auth, headers=headers) as req:
                resp = await req.read()
        resp = json.loads(resp)["count"]
        return resp
    except:
        return

async def atpadd(id):
    try:
        async with aiohttp.ClientSession() as session:
            url = ""
            headers = {'Content-Type': 'application/json'}
            id = json.dumps({'mirai':id})
            auth = aiohttp.BasicAuth(login='', password='')
            async with session.post(url=url, data=id, auth=auth, headers=headers) as req:
                resp = await req.read()
        resp = json.loads(resp)["count"]
        return resp
    except:
        return

async def atpdel(id):
    try:
        async with aiohttp.ClientSession() as session:
            url = ""
            headers = {'Content-Type': 'application/json'}
            id = json.dumps({'mirai':id})
            auth = aiohttp.BasicAuth(login='', password='')
            async with session.post(url=url, data=id, auth=auth, headers=headers) as req:
                resp = await req.read()
        resp = json.loads(resp)["count"]
        return resp
    except:
        return

async def txnlp(action, params):
    try:
        secret_id = ""
        secret_key = ""
        service = "nlp"
        host = "nlp.tencentcloudapi.com"
        endpoint = "https://" + host
        region = "ap-guangzhou"
        version = "2019-04-08"
        algorithm = "TC3-HMAC-SHA256"
        timestamp = int(time.time())
        date = datetime.datetime.utcfromtimestamp(timestamp).strftime("%Y-%m-%d")
        http_request_method = "POST"
        canonical_uri = "/"
        canonical_querystring = ""
        ct = "application/json; charset=utf-8"
        payload = json.dumps(params)
        canonical_headers = "content-type:%s\nhost:%s\n" % (ct, host)
        signed_headers = "content-type;host"
        hashed_request_payload = hashlib.sha256(payload.encode("utf-8")).hexdigest()
        canonical_request = (http_request_method + "\n" +
                             canonical_uri + "\n" +
                             canonical_querystring + "\n" +
                             canonical_headers + "\n" +
                             signed_headers + "\n" +
                             hashed_request_payload)
        credential_scope = date + "/" + service + "/" + "tc3_request"
        hashed_canonical_request = hashlib.sha256(canonical_request.encode("utf-8")).hexdigest()
        string_to_sign = (algorithm + "\n" +
                          str(timestamp) + "\n" +
                          credential_scope + "\n" +
                          hashed_canonical_request)
        def sign(key, msg):
            return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()
        secret_date = sign(("TC3" + secret_key).encode("utf-8"), date)
        secret_service = sign(secret_date, service)
        secret_signing = sign(secret_service, "tc3_request")
        signature = hmac.new(secret_signing, string_to_sign.encode("utf-8"), hashlib.sha256).hexdigest()
        authorization = (algorithm + " " +
                         "Credential=" + secret_id + "/" + credential_scope + ", " +
                         "SignedHeaders=" + signed_headers + ", " +
                         "Signature=" + signature)
        headers = {"Authorization":  authorization,
                   "Content-Type": "application/json; charset=utf-8",
                   "Host": host,
                   "X-TC-Action": action,
                   "X-TC-Timestamp": str(timestamp),
                   "X-TC-Version": version,
                   "X-TC-Region": region}
        async with aiohttp.ClientSession() as session:
            async with session.post(url=endpoint, data=payload, headers=headers) as req:
                resp = await req.read()
        resp = json.loads(resp)
        return resp
    except:
        return

async def pixiv():
    try:
        async with aiohttp.ClientSession() as session:
            pix = random.randint(1, 10)
            url = "https://www.pixiv.net/ranking.php?mode=daily&content=illust&p=" + str(pix) +"&format=json"
            async with session.get(url=url) as req:
                resp = await req.read()
            pix = random.randint(0, 49)
            resp = json.loads(resp)["contents"][pix]["illust_id"]
            url = "https://www.pixiv.net/ajax/illust/" + str(resp) + "/pages"
            async with session.get(url=url) as req:
                resp = await req.read()
            resp = json.loads(resp)["body"][0]["urls"]["regular"]
            headers = {'Referer':'https://app-api.pixiv.net/'}
            async with session.get(url=resp, headers=headers) as req:
                resp = await req.read()
        resp = base64.b64encode(resp).decode()
        resp = "base64://" + resp
        return resp
    except:
        return

async def bdbk(bkmsg):
    try:
        async with aiohttp.ClientSession() as session:
            bdurl = 'https://baike.baidu.com/item/' + bkmsg
            bkmsg = urllib.parse.quote(bkmsg)
            headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0'}
            async with session.get(url=bdurl, headers = headers) as req:
                page = await req.text()
        page = etree.HTML(page)
        if page.xpath('//div[@class="lemmaWgt-subLemmaListTitle"]') != []:
            items = page.xpath('//li[@class="list-dot list-dot-paddingleft"]/div/a/@href')
            if items != []:
                bdurl = 'https://baike.baidu.com' + items[0]
                bkmsg = items[0].replace("/item/", "")
                async with aiohttp.ClientSession() as session:
                    async with session.get(url=bdurl, headers = headers) as req:
                        page = await req.text()
                        page = etree.HTML(page)
        bkimg = page.xpath('//div[@class="album-wrap"]/img/@src')
        addimg = page.xpath('//div[@class="summary-pic"]/a/img/@src')
        bkimg = bkimg + addimg
        addimg = page.xpath('//img[@class="lazy-img"]/@data-src')
        bkimg = bkimg + addimg
        addimg = page.xpath('//div[@class="pic"]/a/img/@src')
        bkimg = bkimg + addimg
        picnum = len(bkimg)
        if picnum >0:
            picnum = picnum - 1
            picnum = random.randint(0, picnum)
            bkimg = bkimg[picnum].split("?x-bce-process")
            bkimg = bkimg[0]
        for i in page.xpath('//div[@class="lemma-summary"]/div//sup'):
            i.getparent().remove(i)
        page = page.xpath('//div[@class="lemma-summary"]/div//text()')
        page = "".join(page).replace('\n', '').replace('\xa0', '')
        if page != '':
            bkmsg = page + '\nhttps://baike.baidu.com/item/' + bkmsg
            if bkimg:
                bkmsg = [{"type": "image", "data": {"file": bkimg}}, {"type": "text", "data": {"text": bkmsg}}]
            else:
                bkmsg = bkmsg
            return bkmsg
    except:
        return

async def ws_group(ws, recv_data):

    if recv_data["sub_type"] == "normal":

        group = recv_data["group_id"]
        sender = recv_data["sender"]["user_id"]
        message = recv_data["message"]
        source = recv_data["message_id"]
        bot = recv_data["self_id"]
        permission = recv_data["sender"]["role"]

        if sender == bot:
            await asyncio.sleep(180)
            sendmsg = {"action": "delete_msg", "params": {"message_id": source}}
            await ws.send_json(sendmsg)
            return

        global answer
        if str(sender) in answer:
            if answer[str(sender)] == message.strip():
                del answer[str(sender)]
                sendmsg = {"action": "send_group_msg", "params": {"group_id": group, "message": [{"type": "at", "data": {"qq": str(sender)}}, {"type": "text", "data": {"text": "\n验证通过，群内发言请遵守相关法律法规。"}}]}}
                await ws.send_json(sendmsg)
                sendmsg = {"action": "delete_msg", "params": {"message_id": source}}
                await ws.send_json(sendmsg)
                return
            else:
                sendmsg = {"action": "send_group_msg", "params": {"group_id": group, "message": [{"type": "at", "data": {"qq": str(sender)}}, {"type": "text", "data": {"text": "\n验证失败，请输入正确答案。"}}]}}
                await ws.send_json(sendmsg)
                sendmsg = {"action": "delete_msg", "params": {"message_id": source}}
                await ws.send_json(sendmsg)
                return

        hh = datetime.datetime.utcnow().hour + 8
        if hh >= 24:
            hh = hh - 24
        if 1 <= hh <= 6:
            hh = 7 - hh
            hh = hh * 3600
            if permission == "member":
                sendmsg = {"action": "set_group_ban", "params": {"group_id": group, "user_id": sender, "duration": hh}}
                await ws.send_json(sendmsg)
                sendmsg = {"action": "delete_msg", "params": {"message_id": source}}
                await ws.send_json(sendmsg)
                return

        resp = await atpget(str(sender))
        if isinstance(resp, int):
            if resp > 0:
                if permission == "member":
                    sendmsg = {"action": "set_group_kick", "params": {"group_id": group, "user_id": sender, "message":"禁止加入"}}
                    await ws.send_json(sendmsg)
                    return

        if sender == 8482303:

            if message.startswith(".查询"):
                atpmsg = message.replace(".查询", "")
                ii = await atpget(atpmsg)
                if isinstance(ii, int):
                    if ii > 0:
                        sendmsg = {"action": "send_group_msg", "params": {"group_id": group, "message": "存在"}}
                        await ws.send_json(sendmsg)
                        return
                    if ii == 0:
                        sendmsg = {"action": "send_group_msg", "params": {"group_id": group, "message": "不存在"}}
                        await ws.send_json(sendmsg)
                        return

            if message.startswith(".添加"):
                atpmsg = message.replace(".添加", "")
                ii = await atpget(atpmsg)
                if isinstance(ii, int):
                    if ii > 0:
                        sendmsg = {"action": "send_group_msg", "params": {"group_id": group, "message": "已存在"}}
                        await ws.send_json(sendmsg)
                        return
                    if ii == 0:
                        ii = await atpadd(atpmsg)
                        if isinstance(ii, int):
                            if ii > 0:
                                sendmsg = {"action": "send_group_msg", "params": {"group_id": group, "message": "添加成功"}}
                                await ws.send_json(sendmsg)
                                return

            if message.startswith(".删除"):
                atpmsg = message.replace(".删除", "")
                ii = await atpget(atpmsg)
                if isinstance(ii, int):
                    if ii == 0:
                        sendmsg = {"action": "send_group_msg", "params": {"group_id": group, "message": "不存在"}}
                        await ws.send_json(sendmsg)
                        return
                    if ii > 0:
                        ii = await atpdel(atpmsg)
                        if isinstance(ii, int):
                            if ii > 0:
                                sendmsg = {"action": "send_group_msg", "params": {"group_id": group, "message": "删除成功"}}
                                await ws.send_json(sendmsg)
                                return

        msg_str = re.findall(r"[\u4e00-\u9fa5]", message)
        msg_str = "".join(msg_str)

        if msg_str != "":
            action = "SensitiveWordsRecognition"
            params = {"Text": msg_str}
            resp = await txnlp(action, params)

            if "SensitiveWords" in resp["Response"]:
                resp = resp["Response"]["SensitiveWords"]
                if resp:
                    for i in resp:
                        ii = await atpget(i)
                        if isinstance(ii, int):
                            if ii == 0:
                                if permission == "member":
                                    sendmsg = {"action": "delete_msg", "params": {"message_id": source}}
                                    await ws.send_json(sendmsg)
                                    return

        bktg = 0
        bkkw = ["百科", "是啥", "啥是", "是谁", "谁是", "是什么", "什么是"]
        for kw in bkkw:
            if message.find(kw) > -1:
                bkmsg = message.replace(kw, "")
                bktg=1
                break
        if bktg == 1:
            bkmsg = await bdbk(bkmsg)
            if bkmsg:
                sendmsg = {"action": "send_group_msg", "params": {"group_id": group, "message": bkmsg}}
                await ws.send_json(sendmsg)
                return

        atbot = "[CQ:at,qq=" + str(bot) +"]"
        if message.find(atbot) > -1:
            msg_str = message.replace(atbot, "")
            action = "ChatBot"
            params = {"Query": msg_str}
            resp = await txnlp(action, params)
            if resp:
                resp = resp["Response"]["Reply"]
                if resp:
                    sendmsg = {"action": "send_group_msg", "params": {"group_id": group, "message": resp}}
                    await ws.send_json(sendmsg)
                    return

        if message.startswith("来张"):
            resp = await pixiv()
            if resp:
                sendmsg = {"action": "send_group_msg", "params": {"group_id": group, "message": [{"type": "image", "data": {"file": resp, "type": "flash"}}]}}
                await ws.send_json(sendmsg)
                return

group_id = 0

async def ws_event(ws, recv_data):

    if recv_data["notice_type"] == "group_decrease":
        sender = recv_data["user_id"]
        resp = await atpget(str(sender))
        if isinstance(resp, int):
            if resp > 0:
                return
            if resp == 0:
                await atpadd(str(sender))
                return

    if recv_data["notice_type"] == "group_increase":
        group = recv_data["group_id"]
        sender = recv_data["user_id"]
        resp = await atpget(str(sender))
        if isinstance(resp, int):
            if resp > 0:
                sendmsg = {"action": "set_group_kick", "params": {"group_id": group, "user_id": sender, "message":"禁止加入"}}
                await ws.send_json(sendmsg)
                return
            if resp == 0:
                global group_id
                group_id = group
                sendmsg = {"action": "get_stranger_info", "params": {"user_id": sender, "no_cache": True}}
                await ws.send_json(sendmsg)
                return

fstpc = 0
fstmo = 0
pcver = ""
mover = ""

async def chkver():
    try:
        global fstpc
        global fstmo
        global pcver
        global mover
        url = "https://pc.woozooo.com/doupload.php"
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0'}
        data = {'task': 5, 'folder_id': , 'pg': 1}  
        cookies = {'ylogin': '', 'phpdisk_info': ''}
        async with aiohttp.ClientSession() as session:
            async with session.post(url=url, data=data, headers=headers, cookies=cookies) as req:
                files = await req.text()
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
            pv = resp
            if fstpc == 0:
                pcver = pv
                fstpc = 1
            url = "https://api.github.com/repos/mozilla-mobile/fenix/releases/latest"
            async with session.get(url=url) as req:
                resp = await req.read()
            mv = json.loads(resp)["tag_name"].replace("v", "")
            if fstmo == 0:
                mover = mv
                fstmo = 1
            sendmsg = ""
            pv32 = "firefox-" + pv + "-win32.exe"
            pv64 = "firefox-" + pv + "-win64.exe"
            if pcver != pv and files.find(pv32) > -1 and files.find(pv64) > -1:
                sendmsg = sendmsg + "国际版火狐v" + pv + "已发布"
                pcver = pv
            mv32 = "fenix-" + mv + "-armeabi-v7a.apk"
            mv64 = "fenix-" + mv + "-arm64-v8a.apk"
            if mover != mv and files.find(mv32) > -1 and files.find(mv64) > -1:
                if sendmsg != "":
                    sendmsg = sendmsg + "\n"
                sendmsg = sendmsg + "安卓版火狐v" + mv + "已发布"
                mover = mv
            if sendmsg != "":
                sendmsg = {"action": "send_group_msg", "params": {"group_id": , "message": [{"type": "at","data": {"qq": "all"}}, {"type": "text", "data": {"text": "\n" + sendmsg}}]}}
            return sendmsg
    except:
        return ""

async def alive(ws):
    while True:
        hh = datetime.datetime.utcnow().hour + 8
        if hh >= 24:
            hh = hh - 24
        mm = datetime.datetime.now().minute
        resp = "现在是" + str(hh) + "时" + str(mm) + "分"
        sendmsg = {"action": "send_private_msg", "params": {"user_id": 8482303, "message": resp}}
        await ws.send_json(sendmsg)
        if hh > 7:
            sendmsg = await chkver()
            if sendmsg != "":
                await ws.send_json(sendmsg)
        delay = random.randint(2, 5)
        delay = delay * 60
        await asyncio.sleep(delay)

answer = {}

async def ws_handle(ws, recv_data):
    if recv_data.type == aiohttp.WSMsgType.TEXT:
        recv_data = json.loads(recv_data.data)
        if "post_type" in recv_data:
            if recv_data["post_type"] == "message" or recv_data["post_type"] == "message_sent":
                await ws_group(ws, recv_data)
                return
            if recv_data["post_type"] == "notice":
                await ws_event(ws, recv_data)
                return
        if "data" in recv_data:
            if isinstance(recv_data["data"], dict):
                if "level" in recv_data["data"]:
                    level = recv_data["data"]["level"]
                    sender = recv_data["data"]["user_id"]
                    if isinstance(level, int):
                        global group_id
                        if level < 4:
                            sendmsg = {"action": "set_group_kick", "params": {"group_id": group_id, "user_id": sender, "message": "禁止加入"}}
                            await ws.send_json(sendmsg)
                            await atpadd(str(sender))
                            return
                        else:
                            x = random.randint(0, 9)
                            y = random.randint(0, 9)
                            z = x + y
                            global answer
                            answer[str(sender)] = str(z)
                            sendmsg = {"action": "send_group_msg", "params": {"group_id": group_id, "message": [{"type": "at", "data": {"qq": str(sender)}}, {"type": "text", "data": {"text": "\n【人机验证】\n请在5分钟内回答以下问题，否则将被踢出：\n" + str(x) + "+" + str(y) + "=?"}}]}}
                            await ws.send_json(sendmsg)
                            await asyncio.sleep(120)
                            if str(sender) in answer:
                                sendmsg = {"action": "send_group_msg", "params": {"group_id": group_id, "message": [{"type": "at", "data": {"qq": str(sender)}}, {"type": "text", "data": {"text": "\n【人机验证】\n请在3分钟内回答以下问题，否则将被踢出：\n" + str(x) + "+" + str(y) + "=?"}}]}}
                                await ws.send_json(sendmsg)
                                await asyncio.sleep(180)
                                if str(sender) in answer:
                                    del answer[str(sender)]
                                    sendmsg = {"action": "set_group_kick", "params": {"group_id": group_id, "user_id": sender, "message": "禁止加入", "reject_add_request": True}}
                                    await ws.send_json(sendmsg)
                                    return

async def main():
    retry = True
    while retry == True:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.ws_connect("ws://127.0.0.1:8090") as ws:
                    asyncio.get_event_loop().create_task(alive(ws))
                    while True:
                        recv_data = await ws.receive()
                        asyncio.get_event_loop().create_task(ws_handle(ws, recv_data))
        except:
            traceback.print_exc()
            await asyncio.sleep(5)
            retry = True

asyncio.get_event_loop().run_until_complete(main())
