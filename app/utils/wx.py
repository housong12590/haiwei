import requests
import json
import time
import datetime

app_id = 'wxebf39e33eb5ac45f'

app_secret = '12ac056a16aa0d68c31c0f2c808d83f6'

token = None

last_time = 0


def get_access_token():
    now_time = int(time.time())
    if now_time - last_time >= 7100:  # token已失效
        url = 'https://api.weixin.qq.com/cgi-bin/token'
        params = {
            'grant_type': 'client_credential',
            'appid': app_id,
            'secret': app_secret
        }
        req = requests.get(url, params)
        if req.status_code == 200:
            data = json.loads(req.text, encoding='utf8')
            global token
            token = data.get('access_token')
    return token


def send_template_msg(title, name, project_name, image, remark):
    url = 'https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=%s' \
          % get_access_token()
    params = {
        "touser": "oH1Iev7F_OtsTeY_RU_oWGC44SvY",
        "template_id": "Q89p_ZgGY_esdEAXF9gq5jgXT4OkvjHFrroGe7wAZlg",
        "url": "http://www.baidu.com",
        "data": {
            "first": {
                "value": title,
                "color": "#173177"
            },
            "keyword1": {
                "value": project_name,
                "color": "#173177"
            },
            "keyword2": {
                "value": image,
                "color": "#173177"
            },
            "keyword3": {
                "value": time.strftime("%Y-%m-%d %H:%M:%S"),
                "color": "#173177"
            },
            "keyword4": {
                "value": name,
                "color": "#173177"
            },
            "remark": {
                "value": remark,
                "color": "#173177"
            }
        }
    }
    req = requests.post(url, json.dumps(params))
    if req.status_code == 200:
        data = json.loads(req.text, encoding='utf8')
        if data.get('errmsg') == 'ok':
            return True
    return False


if send_template_msg('ceshi', 'hous', 'coasts', '123123123', '1.0.3'):
    print('发送成功')
else:
    print("发送失败")
