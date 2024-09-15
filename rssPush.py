import argparse
import configparser
import http.client
import json
import sys
import xml.etree.ElementTree as ET
import time
import platform
import requests
import os

alist_url = ""
path = ""
tool = ""
def_path = ""
if platform.system() == "Windows":
    def_path = "C:/rssConfig"
else:
    def_path = "/rssConfig"

parser = argparse.ArgumentParser(description="rss推送器")
parser.add_argument("--path", default=def_path, type=str, help="可执行文件路径")
current_directory = parser.parse_args().path
configPath = current_directory + r'/RssConfig.ini'


def check_and_write_json(json_file, json_obj):
    # 如果文件存在，则读取文件内容
    if os.path.exists(json_file):
        with open(json_file, 'r', encoding='utf-8') as file:
            try:
                data = json.load(file)  # 读取JSON文件
            except json.JSONDecodeError:
                data = []  # 如果文件为空或损坏，初始化为空列表
    else:
        data = []  # 如果文件不存在，初始化为空列表

    # 判断目标对象是否已经存在
    if json_obj in data:
        return True
    else:
        # 如果不存在，添加对象并写回文件
        data.append(json_obj)
        with open(json_file, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        return False


# 添加离线下载任务
def add_offline_download(token, url):
    conn = http.client.HTTPConnection(alist_url)
    payload = json.dumps({
        "path": path,
        "urls": [
            url
        ],
        "tool": tool,
        "delete_policy": "delete_on_upload_succeed"
    })
    headers = {
        'Authorization': token,
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
def get_token(username, passwd):
    conn = http.client.HTTPConnection(alist_url)
    payload = json.dumps({
        "username": username,
        "password": passwd
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


def get_rss(token, url_name, rss_url):
    # 下载 RSS 内容
    try:
        response = requests.get(rss_url, timeout=20)
        response.raise_for_status()  # 确保请求成功
        # 解析 XML 数据
        root = ET.fromstring(response.content)
        rss_data = current_directory + "/rssData"
        if not os.path.exists(rss_data):
            # 如果目录不存在，则创建该目录
            os.makedirs(rss_data)
        file_path = rss_data + '/' + url_name + '.json'
        # 遍历每个条目并输出信息
        for item in root.findall('channel/item'):
            link = item.find('link').text
            last_part = "magnet:?xt=urn:btih:" + link.split('/')[-1]
            title = item.find('title').text
            enclosure_url = item.find('enclosure').get('url', 'N/A') if item.find('enclosure') is not None else 'N/A'
            # 创建JSON对象，判断该对象是否存在
            rssJson = {"title": title, "last_part": last_part, "link": link, "torrent_url": enclosure_url}
            index = check_and_write_json(file_path, rssJson)
            if not index:
                print("开始下载：" + title)
                add_offline_download(token, last_part)
    except requests.exceptions.Timeout:
        print("请求超时！")
    except requests.exceptions.RequestException as e:
        print(f"网络请求错误: {e}")
    except ET.ParseError as e:
        print(f"XML 解析错误: {e}")
    except Exception as e:
        print(f"发生错误: {e}")


def create_config():
    # 创建配置文件
    if not os.path.isfile(configPath):
        os.makedirs(current_directory)
        # 创建配置对象
        config = configparser.ConfigParser()
        # 添加一些节和选项
        config['alist'] = {
            'url': '域名(ip):端口(alist.com:5244)',
            'username': '用户名',
            'passwd': '密码',
            'Drive': '网盘地址如\\115,\\PikPak',
            'tools': '115 Cloud',
        }
        config['RSS'] = {
            'url1': '订阅地址'
        }

        # 将配置写入到文件
        with open(configPath, 'w', encoding='utf-8') as configfile:
            configfile.write("# alist中配置文件参数意义如下：\n")
            configfile.write("# url:alist地址\n")
            configfile.write("# username:alist用户名\n")
            configfile.write("# passwd:alist密码\n")
            configfile.write("# Drive:网盘路径使用那个网盘就用那个路径 \n")
            configfile.write(
                "# tools:要用离线下载的工具默认115，可选115 Cloud,pikpak,aria2,SimpleHttp和qBittorrent，网盘需要与上面的路径相匹配 \n\n")
            configfile.write("# RSS参数（RSS现阶段只支持mikanani），有几个就填写几个\n")
            configfile.write(
                "# url1:你的蜜柑订阅链接如（https://mikanani.me/RSS/Bangumi?bangumiId=3413&subgroupid=615）\n")
            configfile.write(
                "# url2:你的蜜柑订阅链接如（https://mikanani.me/RSS/Bangumi?bangumiId=3413&subgroupid=615）\n\n")
            config.write(configfile)
        print("请编辑配置文件（Windows路径C:\\rssConfig，Linux路径/rssConfig）")
        sys.exit()


if __name__ == '__main__':

    print("运行时间：" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "\n")
    # 创建配置文件
    create_config()
    config = configparser.ConfigParser(interpolation=None)
    # # # 读取配置文件
    configPath = current_directory + r'/RssConfig.ini'
    config.read(configPath, encoding='utf-8')
    alist_url = config.get('alist', 'url')
    path = config.get('alist', 'Drive')
    tool = config.get('alist', 'tools')
    user = config.get('alist', 'username')
    passwd = config.get('alist', 'passwd')
    token = get_token(user, passwd)
    # # 获取RSS
    urls = config.items('RSS')
    for urlName, url in urls:
        get_rss(token, urlName, url)
