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
        response = requests.post('https://api.dandanplay.net/api/v2/match', headers=headers, data=json.dumps(data),
                                 verify=False)
        response.raise_for_status()
        data = response.json()
        anime = data.get('matches')[0]
        print(anime.get('animeTitle'))
    except requests.exceptions.Timeout:
        print("请求超时！")
    except requests.exceptions.RequestException as e:
        print(f"网络请求错误: {e}")
    except Exception as e:
        print(f"发生错误: {e}")