# _*_ condig:utf-8_*_
import os

PID = os.system('netstat -tunlp | egrep -v grep | grep 8069 |wc -l')

if PID != 1:
    os.system('systemctl restart odoo12')
try:
    print("启动odoo12.... 值为：%s" % PID)
except OSError as error:

    print("odoo12 启动错误%s，错误为：%s" % error, PID)
    print("错误信息执行：sudo journalctl -u odoo12")


