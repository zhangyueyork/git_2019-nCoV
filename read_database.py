#!/usr/bin/env python3.7
# coding=utf-8
#
import re
import sys
import time
sys.path.append('../DXY-2019-nCoV-Crawler')
import read2019nCoVdata as r2d
from crawler_2019_nCoV_data import readindatalst as readdata
import matplotlib.pyplot as plt
import matplotlib as mpl
print("-"*10,"import all end","-"*10)
########


def dataNorm(filename):
    # 将savedata.txt中的数据进行格式整理
    dlst = readdata(filename)[0]
    alldict = []
    for i1 in dlst:
        for k1, v1 in i1.items():
            v11 = eval(v1[0][0].rstrip('}catch(e){}'))
            v21 = v1[1]
            ######## 时间转换
            if 'searchtime' in k1:
                timestamp = re.search('(\d*\.\d*)', k1)
                timefloat = float(timestamp.group(1))
            else:
                timestamp = re.search('(\d{4})-(\d{1,2}-\d{1,2})_(\d{1,2}_\d{1,2})', k1)
                str_m_d_y_h_m = timestamp.group(2).replace('-', ' ') \
                        + ' ' + timestamp.group(3).replace('_', ':') \
                        + ' ' + timestamp.group(1)
                timefloat = time.mktime(time.strptime(str_m_d_y_h_m, '%m %d %H:%M %Y'))
            ########
            for dicti in v11:
                dicti['updateTime'] = timefloat
                alldict.append(dicti)
    return alldict
   #^^^^^^^END


def plot_dailyUpdate(provincelst, countkeyword, listdict):
    # 计算截止至请求时间，各省比前一天增加的人数
    ########
    tAlst, tBlst = r2d.timeseries(r2d.t0, 60*60*24)
    tAlst = [ti for ti in tAlst]
    tBlst = [ti for ti in tBlst]
    ######## 得到更新数据
    updatalst = []
    for pi in provincelst:
        tlst1, count1, tlst2, count2 \
                = r2d.province_evolution(pi, countkeyword, listdict, tAlst, tBlst)
        countdelta = count2[-1] - count2[-2]
        updatalst.append((pi, countdelta))
    ######## 整理数据
    sortupdatalst = sorted(updatalst, key=lambda item:item[1], reverse=True)
    count = []
    province = []
    for i1 in sortupdatalst:
        if i1[1] != 0:
            province.append(proNorm(i1[0]))
            count.append(i1[1])
    print(province)
    print(count)
    ######################## PLOT
    fig = plt.figure()
    pdata = plt.bar(province[1:11], count[1:11])
    autolabel(pdata)
    plt.rcParams['font.sans-serif']=['simhei']
    plt.xlabel('【'+province[0] + '新增' + str(count[0])+'例】')
    plt.ylabel(u'新增确诊人数')
    return fig
   #^^^^^^^END


def plot_province(provincelst, countkeyword, alldict, deltaT=60*60*24):
    tAlst, tBlst = r2d.timeseries(r2d.t0, deltaT)
    tAlst = [ti for ti in tAlst]
    tBlst = [ti for ti in tBlst]
    ########################
    fig = plt.figure()
    for pi in provincelst:
        tlst1bj, count1bj, tlst2bj, count2bj = r2d.province_evolution(pi, 
                countkeyword, alldict, tAlst, tBlst)
        ########
        tlst1bj = [(ti-r2d.t0)/3600/24 for ti in tlst1bj]
        tlst2bj = [(ti-r2d.t0)/3600/24 for ti in tlst2bj]
        ########################
#        plt.plot(tlst1bj, count1bj, '.-')
        plt.plot(tlst2bj, count2bj, '.-', label=pi)
        autolabel2(tlst2bj, count2bj)
    ########
    plt.legend()
    return fig
   #^^^^^^^END



def plot_china(provincelst, countkeyword, alldict):
    tAlst, tBlst = r2d.timeseries(r2d.t0, 60*60*24)
    tAlst = [ti for ti in tAlst]
    tBlst = [ti for ti in tBlst]
    ########################
    tlstC, countC = r2d.nationalevolution(provincelst, countkeyword, alldict, tAlst, tBlst)
    ########
    tlstC = [(ti-r2d.t0)/3600/24 for ti in tlstC]
    ######################## PLOT
    fig = plt.figure()
    plt.plot(tlstC, countC, '.-')
    autolabel2(tlstC, countC)
    plt.ylabel('确诊人数')
    return fig
   #^^^^^^^END


def plot_provincesort(provincelst, countkeyword, listdict):
    # 计算各省排名
    ########
    tAlst, tBlst = r2d.timeseries(r2d.t0, 60*60*24)
    tAlst = [ti for ti in tAlst]
    tBlst = [ti for ti in tBlst]
    ######## 得到最新数据
    updatalst = []
    for pi in provincelst:
        tlst1, count1, tlst2, count2 \
                = r2d.province_evolution(pi, countkeyword, listdict, tAlst, tBlst)
        updatalst.append((pi, count2[-1]))
    ######## 整理数据
    sortupdatalst = sorted(updatalst, key=lambda item:item[1], reverse=True)
    count = []
    province = []
    for i1 in sortupdatalst:
#        if i1[1] != 0:
        province.append(proNorm(i1[0]))
        count.append(i1[1])
    print(province)
    print(count)
    ######################## PLOT
    fig = plt.figure(figsize=(12,5))
    pdata = plt.bar(province[1:], count[1:])
    autolabel(pdata)
    plt.rcParams['font.sans-serif']=['simhei']
    plt.xlabel('【'+province[0] + '总' + str(count[0])+'例】')
    plt.ylabel(u'总确诊人数')
    return fig
   #^^^^^^^END


def autolabel(rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    # copy from matplotlib.org
    for rect in rects:
        height = rect.get_height()
        plt.annotate(str(int(height)),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')
   #^^^^^^^END


def autolabel2(xlst, ylst):
    """Attach a text label above each bar in *rects*, displaying its height."""
    # copy from matplotlib.org
    for ix, x in enumerate(xlst):
        height = ylst[ix]#'{}'.format(height),
        plt.annotate(str(int(height)),
                    xy=(x, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')
   #^^^^^^^END




def proNorm(provincestr):
    output = provincestr
    x1 = re.search('(.*?)[市省]', provincestr)
    if x1:
        output = x1.group(1)
    elif '回族' in provincestr:
        output = '宁夏'
    elif '壮族' in provincestr:
        output = '广西'
    elif '维吾尔' in provincestr:
        output = '新疆'
    elif '自治区' in provincestr:
        output = provincestr.rstrip('自治区')
    return output
   #^^^^^^^END





###############################################################################
########################
ff = open('allprovince.txt', 'r')
allprovince = [i1.replace('\n', '') for i1 in ff]
ff.close()
########################
alldict = dataNorm('savedata.txt')
print('#'*50)
print('#'*50)
print('#'*50)
######################## runrunrunrun
fig1 = plot_dailyUpdate(allprovince, 'confirmedCount', alldict) # 新增排名
fig2 = plot_china(allprovince, 'confirmedCount', alldict)  # 全国趋势
fig3 = plot_province(['北京市', '河南省'], 'confirmedCount', alldict)  # 各省趋势
fig4 = plot_provincesort(allprovince, 'confirmedCount', alldict)   # 各省排名
########################
#print(count1bj[-1])
#print(countC[-1])
########################
fig1.savefig('1.png')
fig2.savefig('2.png')
fig3.savefig('3.png')
fig4.savefig('4.png')
#plt.show()
