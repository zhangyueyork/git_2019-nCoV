#!/usr/bin/python3
#!coding=utf-8
# 分析2019-nCoV感染人数数据
import re
import urllib.request as urllib2
from urllib import error
import http.client
import ssl
import json
########
from time import time, asctime, localtime
#import matplotlib.pyplot as plt
#import numpy as np
#from sys import argv
#
print('-'*10,'import end','-'*10)


def readindatalst(filename):
    ######################## 读入已有数据
    ff = open(filename, 'r')
    lst = [eval(i1.replace('\n', '')) for i1 in ff]
    ff.close()
    ########
    timekeylst = []
    for dicti in lst:
        print('saveddata---', dicti.keys())
        for keyi in dicti.keys():
            timekeylst.append(keyi)
    return lst, timekeylst
   #^^^^^^^END


def savedatalst(filename, newdatadict):
    ######## 保存数据
    olddata, oldtimekey = readindatalst(filename)
    for keyi in newdatadict:
        newtimekey = keyi
    ########
    print('#'*50)
    if newtimekey not in oldtimekey:
        ff = open(filename, 'a', encoding='utf-8')
        print(newdatadict, file=ff)
        ff.close()
        print('savein--->', newtimekey)
    else:
        print('dataexist')
   #^^^^^^^END


def request_content(url,contentpattern):
    ######## url+orbitcontent to items
    print('ininin')
    ssl._create_default_https_context = ssl._create_unverified_context
    ########
    try:
        response = urllib2.urlopen(url)#, headers=headers)
    except error.HTTPError as e:
        print(e.reason)
        print(e.code)
        print(e.headers)
    except error.URLError as e:
        print(e.reason)
    ########
    try:
        print('try2')
        content = response.read().decode('utf-8')
    except http.client.IncompleteRead as e:
        print('except3')
        content = e.partial.decode('utf-8', 'ignore')
    ########
    pattern=re.compile(contentpattern,re.S)
    items=re.findall(pattern,content)
    return items
   #^^^^^^^END


def newDXYweb(url):
    ######################## 收集数据
    ######## 正文
    pattern1 = 'window\.getAreaStat = (.*?)</script>'
    items_url= request_content(url, pattern1)
    print(len(items_url))
    ######## 时间
    pattern_time = 'class="mapTitle___2QtRg">(.*?)</p>'
#    pattern_time = '截至(.*?)北京时间'
    time_stamp = request_content(url, pattern_time)
    if len(time_stamp) > 0:
        time_stamp = time_stamp[0].replace(' ', '_').replace(':', '_')
        time_stampre = re.search('截至_(.*?)_全?国?数据统计', 
                re.sub('[（）]', '_', time_stamp))
        if time_stampre:
            time_stamp = time_stampre.group(1)
    else:
        time_stamp = 'searchtime-'+str(time()) + '-'+str(asctime(localtime(time())))
    print('newdata---', time_stamp)
    ######################## 各省数据
    # 各省数据
    pattern2 = (
            '"provinceShortName":"(.{2,3})",'
            '"confirmedCount":(\d*?),'
            '"suspectedCount":(\d*?),'
            '"curedCount":(\d*?),'
            '"deadCount":(\d*?),'
            '"comment":"(.*?)",'
            )
    match2 = re.findall(pattern2, items_url[0])
    print('#'*20, 'read web end', '#'*20)
    return {time_stamp:[items_url, match2]}
   #^^^^^^^END


###############################################################################
if __name__ == '__main__':
    url = 'https://3g.dxy.cn/newh5/view/pneumonia'
    ######## 读入丁香园数据
    newdatadict = newDXYweb(url)
    ######## 保存数据
    savedatalst('savedata.txt', newdatadict)
