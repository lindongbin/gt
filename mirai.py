import json, re, random, datetime, hashlib, hmac, time, urllib, base64, asyncio, aiohttp
from enum import Enum
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
            resp = json.loads(resp)["body"][0]["urls"]["original"]
            headers = {'Referer':'https://app-api.pixiv.net/'}
            async with session.get(url=resp, headers=headers) as req:
                resp = await req.read()
        resp = base64.b64encode(resp).decode()
        resp = "base64:" + resp
        return resp
    except:
        return

async def bdbk(bkmsg):
    try:
        async with aiohttp.ClientSession() as session:
            bdurl = 'https://baike.baidu.com/item/' + bkmsg
            headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0'}
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
            bkmsg = page + '\nhttps://baike.baidu.com/item/' + urllib.parse.quote(bkmsg)
            if bkimg:
                bkmsg = [{"type": "Image", "url": bkimg}, {"type": "PlainText", "msg": bkmsg}]
            else:
                bkmsg = [{"type": "PlainText", "msg": bkmsg}]
            return bkmsg
    except:
        return

baike = 0
pximg = 0
chatbot = 0

async def ws_msg(websocket, recv_data):

    global baike
    global pximg
    global chatbot

    recv_data = json.loads(recv_data)
    msg = Enum("msg", recv_data)

    if msg.type.value == "GroupMessage":
        group = Enum("group", msg.group.value)
        sender = Enum("sender", msg.sender.value)
        message = recv_data["message"]
        source = message[0]["id"]

        hh = datetime.datetime.now().hour + 12
        if hh >= 24:
            hh = hh - 24
        if 1 <= hh <= 6:
            hh = 7 - hh
            hh = hh * 3600
            if sender.permission.value == "member":
                sendmsg = json.dumps({"type": "MuteMember", "bot": msg.bot.value, "group": group.id.value, "member": sender.id.value, "time": hh})
                await websocket.send(sendmsg)
                sendmsg = json.dumps({"type": "Recall", "messageSource": source})
                await websocket.send(sendmsg)
                return

        for i in message:
            ii = 0
            if "PlainText" in i.values():
                ii = 1
                break

        if ii == 1:

            resp = await atpget(str(sender.id.value))
            if resp > 0:
                if sender.permission.value == "member":
                    sendmsg = json.dumps({"type": "Recall", "messageSource": source})
                    await websocket.send(sendmsg)
                    return

            msg_str = ""
            for i in message:
                if i["type"] == "PlainText":
                    msg_str =  msg_str + i["msg"]
            
            msg_str = re.findall(r"[\u4e00-\u9fa5]", msg_str)
            msg_str = "".join(msg_str)

            action = "SensitiveWordsRecognition"
            params = {"Text": msg_str}
            resp = await txnlp(action, params)

            if "SensitiveWords" in resp["Response"]:
                resp = resp["Response"]["SensitiveWords"]
                if resp:
                    for i in resp:
                        ii = await atpget(i)
                        if ii == 0:
                            if sender.permission.value == "member":
                                sendmsg = json.dumps({"type": "Recall", "messageSource": source})
                                await websocket.send(sendmsg)
                                return

            for i in message:
                if i["type"] == "PlainText":
                    msg_str = i["msg"]
                    break

            if sender.id.value == 8482303:
                if msg_str == ".开启百科":
                    baike = 1
                    return
                if msg_str == ".关闭百科":
                    baike = 0
                    return
                if msg_str == ".开启闲聊":
                    chatbot = 1
                    return
                if msg_str == ".关闭闲聊":
                    chatbot = 0
                    return
                if msg_str == ".开启色图":
                    pximg = 1
                    return
                if msg_str == ".关闭色图":
                    pximg = 0
                    return
                
                if msg_str.startswith(".查询"):
                    atpmsg = msg_str.replace(".查询", "")
                    ii = await atpget(atpmsg)
                    if ii > 0:
                        sendmsg = json.dumps({"type": "SendToGroup", 
                                              "bot": msg.bot.value,
                                              "group": group.id.value,
                                              "message": [{"type": "PlainText", "msg": "存在"}]})
                        await websocket.send(sendmsg)
                        return
                    elif ii == 0:
                        sendmsg = json.dumps({"type": "SendToGroup", 
                                              "bot": msg.bot.value,
                                              "group": group.id.value,
                                              "message": [{"type": "PlainText", "msg": "不存在"}]})
                        await websocket.send(sendmsg)
                        return
                    else:
                        sendmsg = json.dumps({"type": "SendToGroup", 
                                              "bot": msg.bot.value,
                                              "group": group.id.value,
                                              "message": [{"type": "PlainText", "msg": "错误"}]})
                        await websocket.send(sendmsg)
                        return

                if msg_str.startswith(".添加"):
                    atpmsg = msg_str.replace(".添加", "")
                    ii = await atpget(atpmsg)
                    if ii > 0:
                        sendmsg = json.dumps({"type": "SendToGroup", 
                                              "bot": msg.bot.value,
                                              "group": group.id.value,
                                              "message": [{"type": "PlainText", "msg": "已存在"}]})
                        await websocket.send(sendmsg)
                        return
                    elif ii == 0:
                        ii = await atpadd(atpmsg)
                        if ii > 0:
                            sendmsg = json.dumps({"type": "SendToGroup", 
                                                  "bot": msg.bot.value,
                                                  "group": group.id.value,
                                                  "message": [{"type": "PlainText", "msg": "添加成功"}]})
                            await websocket.send(sendmsg)
                            return
                        else:
                            sendmsg = json.dumps({"type": "SendToGroup", 
                                                  "bot": msg.bot.value,
                                                  "group": group.id.value,
                                                  "message": [{"type": "PlainText", "msg": "添加失败"}]})
                            await websocket.send(sendmsg)
                            return
                    else:
                        sendmsg = json.dumps({"type": "SendToGroup", 
                                              "bot": msg.bot.value,
                                              "group": group.id.value,
                                              "message": [{"type": "PlainText", "msg": "错误"}]})
                        await websocket.send(sendmsg)
                        return

                if msg_str.startswith(".删除"):
                    atpmsg = msg_str.replace(".删除", "")
                    ii = await atpget(atpmsg)
                    if ii == 0:
                        sendmsg = json.dumps({"type": "SendToGroup", 
                                              "bot": msg.bot.value,
                                              "group": group.id.value,
                                              "message": [{"type": "PlainText", "msg": "不存在"}]})
                        await websocket.send(sendmsg)
                        return
                    elif ii > 0:
                        ii = await atpdel(atpmsg)
                        if ii > 0:
                            sendmsg = json.dumps({"type": "SendToGroup", 
                                                  "bot": msg.bot.value,
                                                  "group": group.id.value,
                                                  "message": [{"type": "PlainText", "msg": "删除成功"}]})
                            await websocket.send(sendmsg)
                            return
                        else:
                            sendmsg = json.dumps({"type": "SendToGroup", 
                                                  "bot": msg.bot.value,
                                                  "group": group.id.value,
                                                  "message": [{"type": "PlainText", "msg": "删除失败"}]})
                            await websocket.send(sendmsg)
                            return
                    else:
                        sendmsg = json.dumps({"type": "SendToGroup", 
                                              "bot": msg.bot.value,
                                              "group": group.id.value,
                                              "message": [{"type": "PlainText", "msg": "错误"}]})
                        await websocket.send(sendmsg)
                        return

            if baike == 1:
                bktg = 0
                bkkw = ["百科", "是啥", "啥是", "是谁", "谁是", "是什么", "什么是"]
                for kw in bkkw:
                    if msg_str.find(kw) > -1:
                        bkmsg = msg_str.replace(kw, "")
                        bktg=1
                        break
                if bktg == 1:
                    bkmsg = await bdbk(bkmsg)
                    if bkmsg:
                        sendmsg = json.dumps({"type": "SendToGroup", 
                                              "bot": msg.bot.value,
                                              "group": group.id.value,
                                              "message": bkmsg})
                        await websocket.send(sendmsg)
                        return

            if chatbot == 1:
                for i in message:
                    if i["type"] == "At":
                        if i["target"] == msg.bot.value:
                            action = "ChatBot"
                            params = {"Query": msg_str}
                            resp = await txnlp(action, params)
                            resp = resp["Response"]["Reply"]
                            if resp:
                                sendmsg = json.dumps({"type": "SendToGroup", 
                                                      "bot": msg.bot.value,
                                                      "group": group.id.value,
                                                      "message": [{"type": "PlainText", "msg": resp}]})
                                await websocket.send(sendmsg)
                                return

            if pximg == 1:
                if msg_str.startswith("来张"):
                    resp = await pixiv()
                    if resp:
                        sendmsg = json.dumps({"type": "SendToGroup", 
                                              "bot": msg.bot.value,
                                              "group": group.id.value,
                                              "message": [{"type": "Image", "url": resp}]})
                        await websocket.send(sendmsg)
                        return

async def alive(websocket):
    while True:
        hh = datetime.datetime.now().hour + 12
        if hh >= 24:
            hh = hh - 24
        mm = datetime.datetime.now().minute
        resp = "现在是" + str(hh) + "时" + str(mm) + "分"
        sendmsg = json.dumps({"type": "SendToFriend", 
                              "bot": 1009383773,
                              "friend": 8482303,
                              "message": [{"type": "PlainText", "msg": resp}]})
        await websocket.send(sendmsg)
        delay = random.randint(2, 5)
        delay = delay * 60
        await asyncio.sleep(delay)

async def main():
    async with aiohttp.ClientSession() as session:
        async with session.ws_connect("ws://0.0.0.0:8090") as ws:
            await ws.send_str("lindongbin")
            await ws.send_str("8482303")
            asyncio.get_event_loop().create_task(alive(ws))
            while True:
                recv_data = await ws.receive_json()
                await ws_msg(ws, recv_data)

asyncio.get_event_loop().run_until_complete(main())
