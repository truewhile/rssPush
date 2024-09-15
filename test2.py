import argparse
import http.client
import json
import time
import xml.etree.ElementTree as ET
from fake_useragent import UserAgent
import os
import requests
import utils.cloud115
from utils.cloud115 import lixian, get_path_list


def get_rss():
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0",
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'content-type': 'application/xml; charset=utf-8',
        'cookie': ''
    }

    form_data = {
        'ct': 'lixian',
        'ac': 'add_task_url',
        'url': 'magnet:?xt=urn:btih:2b330429701b874083ce41f0e17d09548ee9c50b',
        'savepath': '',
        'wp_path_id': '2989589485718601371',
        'uid': '102324448',
        # 'sign': 'd27f91d820853d693a842161769e5c1a',
        # 'time': '1726402783'
    }
    print(form_data)
    url = 'https://115.com/web/lixian/?ct=lixian&ac=add_task_url&url=magnet%3A%3Fxt%3Durn%3Abtih%3A2b330429701b874083ce41f0e17d09548ee9c50b&savepath=&wp_path_id=2982373681017882022&uid=16808018&sign=7a40de3e57d17e0ec8ff204b8bc99daf&time=1726397621'
    url = 'https://115.com/web/lixian/?ct=lixian&ac=add_task_url&url=magnet%3A%3Fxt%3Durn%3Abtih%3A2b330429701b874083ce41f0e17d09548ee9c50b&savepath=&wp_path_id=2982373681017882022&uid=16808018&sign=7a40de3e57d17e0ec8ff204b8bc99daf&time=1726397621'
    url_new = 'https://115.com/web/lixian/'
    response = requests.post(url_new, params=form_data, headers=headers)
    response.raise_for_status()  #
    data = response.json()

    print(data)


if __name__ == '__main__':
    # print(lixian('magnet:?xt=urn:btih:430d774a733fdf3940730bb743df7fea4aa38c1c&tr=http%3a%2f%2ft.nyaatracker.com%2fannounce&tr=http%3a%2f%2ftracker.kamigami.org%3a2710%2fannounce&tr=http%3a%2f%2fshare.camoe.cn%3a8080%2fannounce&tr=http%3a%2f%2fopentracker.acgnx.se%2fannounce&tr=http%3a%2f%2fanidex.moe%3a6969%2fannounce&tr=http%3a%2f%2ft.acg.rip%3a6699%2fannounce&tr=https%3a%2f%2ftr.bangumi.moe%3a9696%2fannounce&tr=udp%3a%2f%2ftr.bangumi.moe%3a6969%2fannounce&tr=http%3a%2f%2fopen.acgtracker.com%3a1096%2fannounce&tr=udp%3a%2f%2ftracker.opentrackr.org%3a1337%2fannounce'))
    data_list = get_path_list(2949734693203576720).get('data')
    for index in data_list:
        print(f'`{index.get('n')}-{index.get("cid")}`')
