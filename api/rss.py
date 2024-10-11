import json
import os
import platform
import xml.etree.ElementTree as ET
import sqlite3
import requests

import api._115 as _115
import api.alist as alist
import api.ddplay as ddplay
from config import config_loader

config = config_loader.ConfigLoader()

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
        file_path = rss_data + '/rss.db'
        with sqlite3.connect(file_path, isolation_level=None) as con:
            con.row_factory = sqlite3.Row
            sqlite = con.cursor()
            sqlite.execute("""CREATE TABLE IF NOT EXISTS download_logs (
                            id INTEGER PRIMARY KEY,
                            title TEXT,
                            last_part TEXT,
                            link TEXT,
                            torrent_url TEXT,
                            rss_name TEXT)""")
            # 遍历每个条目并输出信息
            for item in root.findall('channel/item'):
                link = item.find('link').text
                last_part = "magnet:?xt=urn:btih:" + link.split('/')[-1]
                title = item.find('title').text
                enclosure_url = item.find('enclosure').get('url', 'N/A') if item.find(
                    'enclosure') is not None else 'N/A'
                # 创建JSON对象，判断该对象是否存在
                sqlite.execute("""select count(*) as sum from download_logs where title=? and rss_name=?""",
                               (title, url_name))
                sun = sqlite.fetchone()
                if sun['sum'] == 0:
                    print("开始下载：" + title)
                    # 启用115直接使用115连接离线下载，不然使用alist离线模式
                    if config.get_115().get('enable'):
                        _115.lixian(last_part, ddplay.get_title(title))
                    else:
                        alist.add_offline_download(last_part)
                    sqlite.execute(
                        """insert into download_logs (title, last_part, link, torrent_url,rss_name) values(?,?,?,?,?)""",
                        (title, last_part, link, enclosure_url, url_name))
    except requests.exceptions.Timeout:
        print("请求超时！")
    except requests.exceptions.RequestException as e:
        print(f"网络请求错误: {e}")
    except ET.ParseError as e:
        print(f"XML 解析错误: {e}")
    except Exception as e:
        print(f"发生错误: {e}")
