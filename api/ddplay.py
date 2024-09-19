import re

import aniparse
import requests
import json


def get_anime_name(file_name):
    try:
        # 请求头
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

        # 请求数据
        data = {
            "fileName": file_name,
            "fileHash": "033bd94b1168d7e4f0d644c3c95e35bf",
            "matchMode": "hashAndFileName"
        }

        # 发起 POST 请求
        response = requests.post('https://api.dandanplay.net/api/v2/match', headers=headers, data=json.dumps(data))
        response.raise_for_status()
        data = response.json()
        anime = data.get('matches')[0]
        return anime.get('animeTitle')
    except requests.exceptions.Timeout:
        print("请求超时！")
    except requests.exceptions.RequestException as e:
        print(f"网络请求错误: {e}")
    except Exception as e:
        print(f"发生错误: {e}")


def get_title(title):
    # 如果字符串以 '[' 或 '【' 开头，截取第一个 ']' 或 '】' 后的内容
    if title[0] == '[' or title[0] == '【':
        pos = title.find(']') if title[0] == '[' else title.find('】')
        title = title[pos + 1:].strip() if pos != -1 else title
    anime_title = aniparse.parse(title).get('anime_title')
    if anime_title:
        chinese_characters = re.findall(r'[\u4e00-\u9fff]', anime_title)
        return ''.join(chinese_characters).replace("/", "").strip() if chinese_characters else anime_title.replace("/","").strip()
    else:
        return get_anime_name(title)