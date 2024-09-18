import time

import config.config_loader as config_loader
import api.rss as rss

config = config_loader.ConfigLoader()

if __name__ == '__main__':
    print("运行时间：" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "\n")
    rss_config = config.get_rss().get("rss_list")
    for url_name, url in rss_config:
        rss.get_rss(url_name, url)
