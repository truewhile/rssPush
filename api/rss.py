import json
import os
import platform
import xml.etree.ElementTree as ET

import aniparse
import requests

import api._115 as _115
import api.alist as alist
from config import config_loader

config = config_loader.ConfigLoader()


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
                    _115.lixian(last_part, get_save_path(title))
                else:
                    alist.add_offline_download(last_part)
    except requests.exceptions.Timeout:
        print("请求超时！")
    except requests.exceptions.RequestException as e:
        print(f"网络请求错误: {e}")
    except ET.ParseError as e:
        print(f"XML 解析错误: {e}")
    except Exception as e:
        print(f"发生错误: {e}")


# 获取保存路径
def get_save_path(title):
    anime_title = aniparse.parse(title).get("anime_title")
    if anime_title:
        return anime_title.replace("/", "")
    else:
        return "默认"
import hashlib


def calculate_md5_first_16mb_from_url(url):
    md5_hash = hashlib.md5()
    chunk_size = 1024  # 每次读取 1KB
    total_read = 0
    max_bytes = 16 * 1024 * 1024  # 16MB in bytes

    with requests.get(url, stream=True) as r:
        r.raise_for_status()  # 检查请求是否成功
        for chunk in r.iter_content(chunk_size=chunk_size):
            if chunk:
                if total_read + len(chunk) > max_bytes:
                    # 如果当前读取的数据超过 16MB，则只取剩余的部分
                    chunk = chunk[:max_bytes - total_read]
                md5_hash.update(chunk)
                total_read += len(chunk)

                # 一旦读取了 16MB，停止
                if total_read >= max_bytes:
                    break

    return md5_hash.hexdigest()
if __name__ == '__main__':
    # anime_title = aniparse.parse("[喵萌奶茶屋&LoliHouse] 时不时会用俄语向我撒娇的邻座阿莉娅同学 / 不时轻声地以俄语遮羞的邻座艾莉同学 / Roshidere - 11 [WebRip 1080p HEVC-10bit AAC][简繁日内封字幕] [426 MB]").get("anime_title").replace("/", "")
    # print(anime_title)
    # def calculate_md5_first_16mb(file_path):
    #     md5_hash = hashlib.md5()
    #     chunk_size = 16 * 1024 * 1024  # 16MB in bytes
    #
    #     with open(file_path, "rb") as f:
    #         # 读取前 16MB 数据
    #         data = f.read(chunk_size)
    #         md5_hash.update(data)
    #
    #     return md5_hash.hexdigest()
    #
    #
    # # 示例使用
    # file_path = "C:/Users/whileTrue/Downloads/义妹生活11全片简中.mp4_-_高律酸.mp4"
    # md5_value = calculate_md5_first_16mb(file_path)
    # print(f"文件前 16MB 的 MD5 值: {md5_value}")
    md = calculate_md5_first_16mb_from_url("http://10.0.0.2:5244/d/%E6%9C%AC%E5%9C%B0%E5%8A%A8%E6%BC%AB/%5BLoliHouse%5D%20Tsue%20to%20Tsurugi%20no%20Wistoria%20-%2010%20%5BWebRip%201080p%20HEVC-10bit%20AAC%20SRTx2%5D.mkv?sign=E-NsNzU8rELvon953GmhBJGvTY90s09bu1182N5cIxc=:0")
    print(md)
