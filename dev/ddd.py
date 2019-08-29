#!/usr/bin/env python
# -*- coding:utf-8 -*-
import urllib    # Python中的cURL库
import urllib.request
from urllib import request,parse
import time    # 时间函数库，包含休眠函数sleep()
url = 'https://blog.csdn.net/jianxin1053/article/details/79649507'    # 希望刷阅读量的文章的URL
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'    # 伪装成Chrome浏览器
refererData = 'http://www.baidu.com'    #伪装成是从baidu.com搜索到的文章
dict ={
    'name':'boss',    #请求参数
}
data=bytes(parse.urlencode(dict),encoding='utf-8')    # 将GET方法中待发送的数据设置为空
headers = {'User-Agent' : user_agent, 'Referer' : refererData}    # 构造GET方法中的Header
count = 0    # 初始化计数器
req = urllib.request.Request(url, data, headers,method='POST')    # 组装GET方法的请求
while 1:    # 一旦开刷就停不下来
    rec = urllib.request.urlopen(req)    # 发送GET请求，获取博客文章页面资源
    #page = rec.read()    # 读取页面内容到内存中的变量，这句代码可以不要
    count += 1    # 计数器加1
    print (count)    # 打印当前循环次数
    if count%5:
        time.sleep(0.01)
    else:
        time.sleep(61)
    #print(page)
print (page)    # 打印页面信息，这句代码永远不会执行





