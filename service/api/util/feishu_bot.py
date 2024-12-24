import json
import urllib2

'''
    check: https://open.feishu.cn/document/client-docs/bot-v3/add-custom-bot?lang=zh-CN#f62e72d5
'''

def _send(data):
    url = "https://open.feishu.cn/open-apis/bot/v2/hook/55f58a72-8f02-481e-8a9e-ba1073095af5"
    headers = {'Content-Type': 'application/json'}
    json_data = json.dumps(data)
    request = urllib2.Request(url, json_data, headers)
    try:
        response = urllib2.urlopen(request)
        response_data = response.read()
        print("Response:", response_data)
    except urllib2.HTTPError as e:
        print("HTTP Error:", e.code)
    except urllib2.URLError as e:
        print("Error:", e.reason)


def feishu_bot_send_text(text):
    data = {
        "msg_type": "text",
        "content": {
            "text": text
        }
    }
    _send(data)


def feishu_bot_send_rich_text(title, text, url = None):
    content = [
        {
            "tag": "text",
            "text": text
        },
        {
            "tag": "a",
            "text": "detail",
            "href": url
        }
    ]
    if url is None:
        content = {
            "tag": "text",
            "text": text
        }

    data = {
        "msg_type": "post",
        "content": {
            "post": {
                "zh_cn": {
                    "title": title,
                    "content": [content]
                }
            }
        }
    }
    _send(data)