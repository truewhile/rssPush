import argparse
import http.client
import xml.etree.ElementTree as ET
from fake_useragent import UserAgent
import os
import requests


def getRss(rss_url):
    headers = {
        'User-Agent': UserAgent().random,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'content-type': 'application/xml; charset=utf-8'
    }
    response = requests.get(rss_url, headers=headers)
    response.raise_for_status()  # 确保请求成功
    # 解析 XML 数据
    root = ET.fromstring(response.content)

    # 遍历每个条目并输出信息
    for item in root.findall('channel/item'):
        guid = item.find('guid').text
        print(guid)
        link = item.find('link').text
        last_part = "magnet:?xt=urn:btih:" + link.split('/')[-1]
        print(last_part)
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="rss推送器")
    parser.add_argument("path", type=str, help="可执行文件路径")
    #getRss("https://mikanani.me/RSS/Bangumi?bangumiId=3413&subgroupid=615")
    #current_directory = os.path.dirname(os.path.abspath(__file__))
    print(parser.parse_args().path)