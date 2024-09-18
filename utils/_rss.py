import json
import platform
import sys
import xml.etree.ElementTree as ET
from xmlrpc.client import boolean

import requests
import os
import aniparse
import _config
from _115 import lixian
from _alist import add_offline_download

config = _config.ConfigLoader()


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


# 获取rss信息
def get_rss(url_name, rss_url):
    # 下载 RSS 内容
    try:
        response = requests.get(rss_url, timeout=20)
        response.raise_for_status()  # 确保请求成功
        # 解析 XML 数据
        root = ET.fromstring(response.content)
        if platform.system() == "Windows":
            def_path = "C:/rssConfig"
        else:
            def_path = "/rssConfig"
        rss_data = def_path + "/rssData"
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
                if config.get_115().get('enable'):
                    lixian(last_part, get_save_path(title))
                else:
                    add_offline_download(last_part)
    except requests.exceptions.Timeout:
        print("请求超时！")
    except requests.exceptions.RequestException as e:
        print(f"网络请求错误: {e}")
    except ET.ParseError as e:
        print(f"XML 解析错误: {e}")
    except Exception as e:
        print(f"发生错误: {e}")

#获取保存路径
def get_save_path(title):
    anime_title = aniparse.parse(title).get("anime_title")
    if anime_title:
        return "默认"
    else:
        return anime_title
