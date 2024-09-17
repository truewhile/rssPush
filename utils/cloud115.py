import requests


headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0",
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'content-type': 'application/xml; charset=utf-8',
        'cookie': 'UID=16808018_R1_1726492897; CID=b84ca42deb9eac60f47e165fe98cfc71; SEID=3cf713e82d981c0cc669c6b88ea32841b3c1126568c77d157876e022aeccefbe72d04db9792b28ce4ddd06961d0c63ddee1772f5746ea10cfa19478d'
    }

def lixian(url):
    form_data = {
        'ct' :'lixian',
        'ac' :'add_task_url',
        'url': url,
        'savepath': '',
        'wp_path_id': '2949725193306342620',
        'uid': '16808018',
        # 'sign': 'd27f91d820853d693a842161769e5c1a',
        # 'time': '1726402783'
    }
    url_new = 'https://115.com/web/lixian/'
    response = requests.post(url_new ,params=form_data, headers=headers)
    response.raise_for_status()  #
    data = response.json()
    print(data)
    return data
def get_path_list(cid):
    params = {
        "aid": 1,
        "cid": cid,
        "o": "user_ptime",
        "asc": 0,
        "offset": 0,
        "show_dir": 1,
        "limit": 40,
        "snap": 0,
        "natsort": 1,
        "record_open_time": 1,
        "count_folders": 1,
        "format": "json"
    }
    url_new = 'https://webapi.115.com/files'
    response = requests.get(url_new, params=params, headers=headers)
    response.raise_for_status()  #
    data = response.json()
    return data
if __name__ == '__main__':
    lixian('magnet:?xt=urn:btih:63f592d48e28225fdb2ecd8f7e4150d8d6ab9b83&tr=http%3a%2f%2ft.nyaatracker.com%2fannounce&tr=http%3a%2f%2ftracker.kamigami.org%3a2710%2fannounce&tr=http%3a%2f%2fshare.camoe.cn%3a8080%2fannounce&tr=http%3a%2f%2fopentracker.acgnx.se%2fannounce&tr=http%3a%2f%2fanidex.moe%3a6969%2fannounce&tr=http%3a%2f%2ft.acg.rip%3a6699%2fannounce&tr=https%3a%2f%2ftr.bangumi.moe%3a9696%2fannounce&tr=udp%3a%2f%2ftr.bangumi.moe%3a6969%2fannounce&tr=http%3a%2f%2fopen.acgtracker.com%3a1096%2fannounce&tr=udp%3a%2f%2ftracker.opentrackr.org%3a1337%2fannounce')