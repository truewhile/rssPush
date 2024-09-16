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

# alist
# alist 链接地址
alist_url = ""
# alist中网盘路径
path = ""
# alist 离线工具选择
tool = ""

# 115
# 115cookie
cookie = ""
# 115用户id
uid = ""
# 115离线下载路径id
path_id = ""
# 是否直接使用115离线
enable_115 = False

# 配置文件默认路径
def_path = ""
if platform.system() == "Windows":
    def_path = "C:/rssConfig"
else:
    def_path = "/rssConfig"

# 运行时参数
parser = argparse.ArgumentParser(description="rss推送器")
parser.add_argument("--path", default=def_path, type=str, help="可执行文件路径")
current_directory = parser.parse_args().path
configPath = current_directory + r'/RssConfig.ini'


# 'wp_path_id': '2949725193306342620',
# 判断rss订阅信息是否已下载
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


# alist离线下载任务
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


# 获取rss信息
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
                # 启用115直接使用115连接离线下载，不然使用alist离线模式
                if enable_115:
                    lixian_115(last_part)
                else:
                    add_offline_download(token, last_part)
    except requests.exceptions.Timeout:
        print("请求超时！")
    except requests.exceptions.RequestException as e:
        print(f"网络请求错误: {e}")
    except ET.ParseError as e:
        print(f"XML 解析错误: {e}")
    except Exception as e:
        print(f"发生错误: {e}")


# 创建配置文件
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
        config['115'] = {
            'enable': False,
            'cookie': '115 cookie',
            'uid': '用户uid',
            'path_id': '保存目录id'
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


# 115离线下载
def lixian_115(url):
    # # # 读取配置文件
    config = configparser.ConfigParser(interpolation=None)
    config.read(configPath, encoding='utf-8')
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0",
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'content-type': 'application/xml; charset=utf-8',
        # 'cookie': 'UID=16808018_R1_1726492897; CID=b84ca42deb9eac60f47e165fe98cfc71; SEID=3cf713e82d981c0cc669c6b88ea32841b3c1126568c77d157876e022aeccefbe72d04db9792b28ce4ddd06961d0c63ddee1772f5746ea10cfa19478d'
        'cookie': cookie
    }
    form_data = {
        'ct': 'lixian',
        'ac': 'add_task_url',
        'url': url,
        'savepath': '',
        'wp_path_id': path_id,
        # 'uid': '16808018',
        'uid': uid,
        # 'sign': 'd27f91d820853d693a842161769e5c1a',
        # 'time': '1726402783'
    }
    response = requests.post('https://115.com/web/lixian/', params=form_data, headers=headers)
    response.raise_for_status()
    data = response.json()
    if data.get("errno") != 0:
        print(f"离线下载失败，请检查115 cookie是否失效，{data}")
        sys.exit(1)


if __name__ == '__main__':
    print("运行时间：" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "\n")
    # 创建配置文件
    create_config()
    config = configparser.ConfigParser(interpolation=None)
    # # # 读取配置文件
    config.read(configPath, encoding='utf-8')
    alist_url = config.get('alist', 'url')
    path = config.get('alist', 'Drive')
    tool = config.get('alist', 'tools')
    user = config.get('alist', 'username')
    passwd = config.get('alist', 'passwd')
    cookie = config.get('115', 'cookie')
    path_id = config.get('115', 'path_id')
    uid = config.get('115', 'uid')
    token = get_token(user, passwd)
    # # 获取RSS
    urls = config.items('RSS')
    for urlName, url in urls:
        get_rss(token, urlName, url)
