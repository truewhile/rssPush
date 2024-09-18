import _config
import _rss
config = _config.ConfigLoader()
if __name__ == '__main__':
    rss = config.get_rss()
    for url_name, url in rss:
        _rss.get_rss(url_name, url)
