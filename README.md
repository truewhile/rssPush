# alist-rssPush
监控rss订阅推送到alist离线下载
现阶段只编译了Debian,windows,Openwrt版本，如果有其它环境需要请自行编译
````bash
apt install python3
apt install python3-pip
pip install -r requirements.txt
pyinstaller --onefile rssPush.py
````
下载二进制文件后./rssPush一次后生成配置文件，修改配置文件后再次运行进行rss推送
设置定时任务 每15分钟刷新订阅
````bash
(crontab -l 2>/dev/null; echo "*/15 * * * * ./root/rssPush >> /rssPush/logs.log") | crontab -
````
