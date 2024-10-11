import os
import platform
import sqlite3
import sys

import requests

from config import config_loader

config = config_loader.ConfigLoader()
cookie = config.get_115().get("cookie")
headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0",
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'cookie': cookie
}


# 获取用户uid
def get_uid():
    # 找到 UID 的值
    uid_value = [item.split('=')[1] for item in cookie.split('; ') if item.startswith('UID')][0]
    # 提取 UID 中的数字部分
    uid_number = uid_value.split('_')[0]
    return uid_number


# 查询文件夹是否存在
def search(dir_name) -> str:
    try:
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
            sqlite.execute("""CREATE TABLE IF NOT EXISTS path_115 (
                            id INTEGER PRIMARY KEY,
                            dir_name TEXT,
                            father_id TEXT,
                            dir_id TEXT)""")
            father_id = config.get_115().get("path_id")
            sqlite.execute("""select * from path_115 where dir_name=? and father_id=?""",
                           (dir_name, father_id))
            dir_info = sqlite.fetchone()
            if dir_info is not None and dir_info["dir_id"] is not None:
                return dir_info["dir_id"]
            if father_id is None:
                father_id = '0'
            form_data = {
                'offset': '0',
                'limit': '30',
                'search_value': dir_name,  # 已解码为中文
                'aid': '1',
                'cid': father_id,
                'count_folders': '1',
                'format': 'json'
            }
            response = requests.get('https://webapi.115.com/files/search', params=form_data, headers=headers)
            response.raise_for_status()
            data = response.json()
            datas = data.get('data')
            # 使用列表解析来过滤目录
            directories = [item for item in datas if 'dp' in item and 'fid' not in item]
            # 如果找到目录，打印目录信息
            if directories:
                sqlite.execute("""insert into path_115 (dir_name, father_id,dir_id) values (?, ?,?)""",
                               (dir_name, father_id, directories[0].get('cid')))
                return directories[0].get('cid')
            else:
                dir_id = add_dir(father_id, dir_name)
                sqlite.execute("""insert into path_115 (dir_name, father_id,dir_id) values (?, ?,?)""",
                               (dir_name, father_id, dir_id))
                return dir_id
    except requests.exceptions.Timeout:
        print("请求超时！")
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(f"网络请求错误: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"发生错误: {e}")
        sys.exit(1)


# 创建文件夹
def add_dir(father_id, dir_name) -> str:
    try:
        url = "https://webapi.115.com/files/add"
        form_data = {
            "pid": father_id,
            "cname": dir_name
        }
        response = requests.post(url, headers=headers, data=form_data)
        response.raise_for_status()
        data = response.json()
        return data.get("cid")
    except requests.exceptions.Timeout:
        print("请求超时！")
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(f"网络请求错误: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"发生错误: {e}")
        sys.exit(1)


# 115离线下载
def lixian(url, path_name):
    try:
        form_data = {
            'ct': 'lixian',
            'ac': 'add_task_url',
            'url': url,
            'wp_path_id': search(path_name),
            'uid': get_uid()
        }
        response = requests.post('https://115.com/web/lixian/', params=form_data, headers=headers)
        response.raise_for_status()
        data = response.json()
        if data.get("errno") != 0:
            print(f"离线下载失败，请检查115 cookie是否失效，{data}")
            sys.exit(1)
    except requests.exceptions.Timeout:
        print("请求超时！")
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(f"网络请求错误: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"发生错误: {e}")
        sys.exit(1)
