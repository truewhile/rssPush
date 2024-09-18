import http.client
import json
import sys

from config import config_loader

config = config_loader.ConfigLoader()


# alist离线下载任务
def add_offline_download(url):
    conn = http.client.HTTPConnection(config.get_alist().get("url"))
    payload = json.dumps({
        "path": config.get_alist().get("drive"),
        "urls": [
            url
        ],
        "tool": config.get_alist().get("tools"),
        "delete_policy": "delete_on_upload_succeed"
    })
    headers = {
        'Authorization': get_token,
        'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
        'Content-Type': 'application/json'
    }
    conn.request("POST", "/api/fs/add_offline_download", payload, headers)
    res = conn.getresponse()
    data = res.read()
    json_data = json.loads(data)
    if json_data.get("code") != 200:
        print(f"请求失败，请检查alist中drive与tools是否填写正确")
        sys.exit(1)


# 获取token
def get_token():
    conn = http.client.HTTPConnection(config.get_alist().get("url"))
    payload = json.dumps({
        "username": config.get_alist().get("username"),
        "password": config.get_alist().get("passwd"),
    })
    headers = {
        'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
        'Content-Type': 'application/json'
    }
    conn.request("POST", "/api/auth/login", payload, headers)
    res = conn.getresponse()

    data = res.read()
    json_data = json.loads(data.decode("utf-8"))
    if json_data.get("code") != 200:
        print(f"请求失败，请检查alist地址与用户名密码是否填写正确")
        sys.exit(1)
    return json_data.get('data', {}).get('token', 'Token not found')
