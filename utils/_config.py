import configparser
import os
import platform
import sys


class ConfigLoader:
    def __init__(self):
        if platform.system() == "Windows":
            def_path = "C:/rssConfig"
        else:
            def_path = "/rssConfig"
        config_file = def_path + r'/RssConfig.ini'
        # 创建配置文件
        if not os.path.isfile(config_file):
            if not os.path.isdir(def_path):
                os.makedirs(def_path)
            # 创建配置对象
            config = configparser.ConfigParser()
            # 添加一些节和选项
            config['alist'] = {
                'url': '域名(ip):端口(alist.com:5244)',
                'username': '用户名',
                'passwd': '密码',
                'drive': '网盘地址如\\115,\\PikPak',
                'tools': '115 Cloud'
            }
            config['RSS'] = {
                'url1': '订阅地址'
            }
            config['115'] = {
                'enable': False,
                'cookie': '115 cookie',
                'uid': '用户uid',
                'path_id': '保存目录id'
            }

            # 将配置写入到文件
            with open(config_file, 'w', encoding='utf-8') as configfile:
                configfile.write("# alist中配置文件参数意义如下：\n")
                configfile.write("# url:alist地址\n")
                configfile.write("# username:alist用户名\n")
                configfile.write("# passwd:alist密码\n")
                configfile.write("# Drive:网盘路径使用那个网盘就用那个路径 \n")
                configfile.write(
                    "# tools:要用离线下载的工具默认115，可选115 Cloud,pikpak,aria2,SimpleHttp和qBittorrent，网盘需要与上面的路径相匹配 \n\n")
                configfile.write("# RSS参数（RSS现阶段只支持mikanani），有几个就填写几个\n")
                configfile.write(
                    "# url1:你的蜜柑订阅链接如（https://mikanani.me/RSS/Bangumi?bangumiId=3413&subgroupid=615）\n")
                configfile.write(
                    "# url2:你的蜜柑订阅链接如（https://mikanani.me/RSS/Bangumi?bangumiId=3413&subgroupid=615）\n\n")
                config.write(configfile)
            print("请编辑配置文件（Windows路径C:\\rssConfig，Linux路径/rssConfig）")
            sys.exit()
        # 初始化时加载配置文件
        self.config = configparser.ConfigParser(interpolation=None)
        self.config.read(config_file, encoding='utf-8')

    def get_alist(self):
        # 获取数据库配置
        return {
            'url': self.config.get("alist", "url"),
            'username': self.config.get("alist", "username"),
            'passwd': self.config.get("alist", "passwd"),
            'drive': self.config.get("alist", "drive"),
            'tools': self.config.get("alist", "tools")
        }

    def get_rss(self):
        # 获取API配置
        return {
            'rss_list': self.config.items('RSS')
        }

    def get_115(self):
        # 获取数据库配置
        return {
            'enable': self.config.getboolean('115', 'enable'),
            'cookie': self.config.get('115', 'cookie'),
            'path_id': self.config.get('115', 'path_id')
        }
