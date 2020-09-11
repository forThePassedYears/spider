# coding:utf-8
import urllib.request
import random
import re


ippools = [
    '114.125.11.23:30221',
    '10.34.107.22:4322',
    '22.243.123.44:605',
    '127.0.0.1:8080'
]

# 使用代理IP， 并创建为全局使用


def ip(ippools):
    thisip = random.choice(ippools)
    print(thisip)
    proxy = urllib.request.ProxyHandler({'http': thisip})
    opener = urllib.request.build_opener(proxy, urllib.request.HTTPHandler)
    urllib.request.install_opener(opener)


for i in range(5):
    try:
        ip(ippools)
        url = 'http://www.baidu.com'
        data = urllib.request.urlopen(url).read().decode('utf-8', 'ignore')
        print(len(data))
    except Exception as err:
        print(err)

