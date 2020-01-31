#!/usr/bin/env python3.7
# coding=utf-8
#
import re
import sys
import time
import sys
import os
import numpy as np
filepath = os.path.split(os.path.realpath(__file__))[0]
path0 = os.path.split(filepath)[0]
sys.path.append(os.path.join(path0, 'DXY-2019-nCoV-Crawler'))
import read2019nCoVdata as r2d
from crawler_2019_nCoV_data import readindatalst as readdata
import matplotlib.pyplot as plt
import matplotlib as mpl
print("-"*10,"import all end","-"*10)
########


def checkdata(filename):
    # 去除重复数据
    dlst = readdata(filename)[0]
    dlst2 = []
    print(len(dlst))
    for i1 in dlst:
        dlst2.append(str(list(i1.values())[0][0]))
    dlstin1 = list(set(dlst2))
    print(len(dlstin1))
    ########
    newlst = []
    lst2 = []
    for i1 in dlst:
        dlstvalue = str(list(i1.values())[0][0])
        if dlstvalue not in lst2:
            lst2.append(dlstvalue)
            newlst.append(i1)
    print(len(newlst))
    ########
    ff = open('savedatanew.txt', 'w')
    for i1 in newlst:
        print(i1, file=ff)
    ff.close()
   #^^^^^^^END
#checkdata('savedata.txt')
#input('xxx')


def get_citylst(province, provincekey, citykey, listdict):
    # 获取某省下属城市列表
    provincedata = r2d.selectkeydata(listdict, provincekey, province)
    citylst = []
    for dicti in provincedata:
        citydata = dicti['cities']
        for citydict in citydata:
            citylst.append(citydict[citykey].split('区')[0])
    return list(set(citylst))


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


def plot_china_f11(provincelst, countkeyword, alldict):
    tAlst, tBlst = r2d.timeseries(r2d.t0, 60*60*24)
    tAlst = [ti for ti in tAlst]
    tBlst = [ti for ti in tBlst]
    ########################
    tlstC, countC, tend = r2d.nationalevolution(provincelst, countkeyword, 
            alldict, tAlst, tBlst)
    tnow = str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(tend)))
    ########
    tlstC = [(ti-r2d.t0)/3600/24 for ti in tlstC]
    deltaCount = np.array(countC[1:]) - np.array(countC[:-1])
    ######################## PLOT
#    fig = plt.figure()
    plt.subplot(121)
    plt.subplots_adjust(left=0.07, right=0.98)
    plt.title('全国确诊人数与日增量变化 -- 截止至' + tnow + '\n 时间零点:' \
            +str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(r2d.t0))))
    plt.plot(tlstC, countC, '.-', label='总确诊人数')
    plt.plot(tlstC[1:], deltaCount, '.-', label='日增人数')
    autolabel2(tlstC, countC)
    autolabel2(tlstC[1:], deltaCount)
    plt.rcParams['font.sans-serif']=['SimHei']
    plt.ylabel('人数')
    plt.legend()
#    return fig
   #^^^^^^^END


def plot_province_f12(provincelst, countkeyword, alldict, deltaT=60*60*24):
    tAlst, tBlst = r2d.timeseries(r2d.t0, deltaT)
    tAlst = [ti for ti in tAlst]
    tBlst = [ti for ti in tBlst]
    ########################
#    fig = plt.figure()
    plt.subplot(122)
    plt.subplots_adjust(left=0.07, right=0.98)
    tnowlst = []
    for pi in provincelst:
        tlst1bj, count1bj, tlst2bj, count2bj = r2d.province_evolution(pi, 
                countkeyword, alldict, tAlst, tBlst)
        ########
        tnowlst.append(tlst1bj[-1])
        tlst1bj = [(ti-r2d.t0)/3600/24 for ti in tlst1bj]
        tlst2bj = [(ti-r2d.t0)/3600/24 for ti in tlst2bj]
        ########################
#        plt.plot(tlst1bj, count1bj, '.-')
        plt.plot(tlst2bj, count2bj, '.-', label=pi)
        autolabel2(tlst2bj, count2bj)
        plt.rcParams['font.sans-serif']=['SimHei']
    ########
    tnow = str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(max(tnowlst))))
    plt.title('几个省确诊人数变化 -- 截止至' + tnow + '\n 时间零点:' \
            +str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(r2d.t0))))
    plt.ylabel('总确诊人数')
    plt.legend()
#    return fig
   #^^^^^^^END


def plot_provincesort_f21(provincelst, countkeyword, listdict):
    # 计算各省排名
    ########
    tAlst, tBlst = r2d.timeseries(r2d.t0, 60*60*24)
    tAlst = [ti for ti in tAlst]
    tBlst = [ti for ti in tBlst]
    ######## 得到最新数据
    updatalst = []
    tendlst = []
    for pi in provincelst:
        tlst1, count1, tlst2, count2 \
                = r2d.province_evolution(pi, countkeyword, listdict, tAlst, tBlst)
        updatalst.append((pi, count2[-1]))
        tendlst.append(tlst1[-1])
    ######## 整理数据
    sortupdatalst = sorted(updatalst, key=lambda item:item[1], reverse=True)
    count = []
    provincelst = []
    for i1 in sortupdatalst:
#        if i1[1] != 0:
        provincelst.append(proNorm(i1[0]))
        count.append(i1[1])
    print(provincelst)
    print(count)
    ######################## PLOT
    tnow = str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(max(tendlst))))
#    fig = plt.figure(figsize=(13,5))
    plt.subplot(211)
    plt.subplots_adjust(left=0.07, right=0.98)
    plt.title('全国各省确诊人数排名 -- 截止至' + tnow + '\n 时间零点:' \
            +str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(r2d.t0))))
    maxp = 'no'
    if count[0]/5 > count[1] and count[0]>100:
        maxp = provincelst[0]
        maxv = count[0]
        provincelst = provincelst[1:]
        count = count[1:]
    pdata = plt.bar(provincelst, count)
    ########
    if '北京' in provincelst:
        bjindex = provincelst.index('北京')
        for i1, k1 in enumerate(pdata):
            if i1 == bjindex:
                k1.set_color('red')
    ########
    autolabel(pdata)
    plt.rcParams['font.sans-serif']=['SimHei']
    if maxp != 'no':
        plt.xlabel('【'+maxp + '总' + str(maxv)+'例】')
    plt.ylabel(u'总确诊人数')
#    return fig
   #^^^^^^^END


def plot_dailyUpdate_f22(provincelst, countkeyword, listdict):
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
    tnow = str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(tlst1[-1])))
    ######## 整理数据
    sortupdatalst = sorted(updatalst, key=lambda item:item[1], reverse=True)
    count = []
    provincelst = []
    for i1 in sortupdatalst:
        if i1[1] != 0:
            provincelst.append(proNorm(i1[0]))
            count.append(i1[1])
    print(provincelst)
    print(count)
    if len(provincelst) == 0:
        provincelst = [0,0]
        count = [0,0]
    ######################## PLOT
#    fig = plt.figure(figsize=(13,5))
    plt.subplot(212)
    plt.subplots_adjust(bottom=0.05, top=0.95, left=0.07, right=0.98, hspace=0.3)
    plt.title('全国各省新增排名 -- 截止至' + tnow + '\n 时间零点:' \
            +str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(r2d.t0))))
    maxp = 'no'
    if count[0]/5 > count[1] and count[0]>100:
        maxp = provincelst[0]
        maxv = count[0]
        provincelst = provincelst[1:]
        count = count[1:]
    pdata = plt.bar(provincelst, count)
    ########
    if '北京' in provincelst:
        bjindex = provincelst.index('北京')
        for i1, k1 in enumerate(pdata):
            if i1 == bjindex:
                k1.set_color('red')
    ########
    autolabel(pdata)
    plt.rcParams['font.sans-serif']=['SimHei']
    if maxp != 'no':
        plt.xlabel('【'+str(maxp) + '新增' + str(maxv)+'例】')
    plt.ylabel(u'各省一日新增确诊人数')
#    return fig
   #^^^^^^^END


def plot_province_time1_f31(provincelst, countkeyword, alldict, deltaT=60*60*24):
    # 画某省时间变化及日增量时间变化
    ########
    tAlst, tBlst = r2d.timeseries(r2d.t0, deltaT)
    tAlst = [ti for ti in tAlst]
    tBlst = [ti for ti in tBlst]
    ########################
    tnowlst = []
    plt.subplot(121)
    plt.subplots_adjust(left=0.07, right=0.98)
    for pi in provincelst:
        tlst1bj, count1bj, tlst2bj, count2bj = r2d.province_evolution(pi, 
                countkeyword, alldict, tAlst, tBlst)
        countdelta = np.array(count2bj[1:]) - np.array(count2bj[:-1])
        tdelta = tlst2bj[1:]
        ########
        tnowlst.append(tlst1bj[-1])
        tlst1bj = [(ti-r2d.t0)/3600/24 for ti in tlst1bj]
        tlst2bj = [(ti-r2d.t0)/3600/24 for ti in tlst2bj]
        tdelta = [(ti-r2d.t0)/3600/24 for ti in tdelta]
        ########################
#        plt.plot(tlst1bj, count1bj, '.-')
        plt.plot(tlst2bj, count2bj, '.-', label='总确诊人数')
        plt.plot(tdelta, countdelta, '.-', label='日增人数')
        autolabel2(tlst2bj, count2bj)
        autolabel2(tdelta, countdelta)
        plt.rcParams['font.sans-serif']=['SimHei']
    ########
    tnow = str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(max(tnowlst))))
    plt.title(str(provincelst)+'人数整体趋势 -- 截止至' + tnow + '\n 时间零点:' \
            +str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(r2d.t0))))
    plt.ylabel('人数')
    plt.legend()
#    return fig
   #^^^^^^^END


def plot_provinceson_time2_f32(province, provincekey, citykey, 
        countkeyword, alldict, deltaT=60*60*24):
    tAlst, tBlst = r2d.timeseries(r2d.t0, deltaT)
    tAlst = [ti for ti in tAlst]
    tBlst = [ti for ti in tBlst]
    citylst = get_citylst(province, provincekey, citykey, alldict)
    ########################
    plt.subplot(122)
    plt.subplots_adjust(left=0.07, right=0.98)
    tnowlst = []
    for pi in citylst:
        tlst1bj, count1bj, tlst2bj, count2bj = r2d.city_evolution(province, provincekey, 
                pi, citykey, countkeyword, alldict, tAlst, tBlst)
        ########
        tnowlst.append(tlst1bj[-1])
        tlst1bj = [(ti-r2d.t0)/3600/24 for ti in tlst1bj]
        tlst2bj = [(ti-r2d.t0)/3600/24 for ti in tlst2bj]
        ########################
#        plt.plot(tlst1bj, count1bj, '.-')
        plt.plot(tlst2bj, count2bj, '.-', label=pi)
        autolabel2(tlst2bj, count2bj)
        plt.rcParams['font.sans-serif']=['SimHei']
    ########
    tnow = str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(max(tnowlst))))
    plt.title(province+'辖区 -- 截止至' + tnow + '\n 时间零点:' \
            +str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(r2d.t0))))
    plt.ylabel('总确诊人数')
    plt.legend()
#    return fig
   #^^^^^^^END


def plot_citysort_f41(province, countkeyword, listdict):
    # 计算各市排名
    ########
    tAlst, tBlst = r2d.timeseries(r2d.t0, 60*60*24)
    tAlst = [ti for ti in tAlst]
    tBlst = [ti for ti in tBlst]
    citylst = get_citylst(province, 'provinceName', 'cityName', alldict)
    ######## 得到最新数据
    updatalst = []
    tendlst = []
    for pi in citylst:
        tlst1, count1, tlst2, count2 \
                = r2d.city_evolution(province, 'provinceName', 
                        pi, 'cityName', countkeyword, listdict, tAlst, tBlst)
        updatalst.append((pi, count2[-1]))
        tendlst.append(tlst1[-1])
    ######## 整理数据
    sortupdatalst = sorted(updatalst, key=lambda item:item[1], reverse=True)
    count = []
    provincelst = []
    for i1 in sortupdatalst:
#        if i1[1] != 0:
        provincelst.append(i1[0])
        count.append(i1[1])
    print(provincelst)
    print(count)
    ######################## PLOT
    tnow = str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(max(tendlst))))
    plt.subplot(211)
    plt.subplots_adjust(bottom=0.05, top=0.95, left=0.07, right=0.98)
    plt.subplots_adjust(left=0.07, right=0.98)
    plt.title(province+'累计排名 -- 截止至' + str(tnow) + '\n 时间零点:' \
            +str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(r2d.t0))))
    maxp = 'no'
    if count[0]/5 > count[1] and count[0]>100:
        maxp = provincelst[0]
        maxv = count[0]
        provincelst = provincelst[1:]
        count = count[1:]
    pdata = plt.bar(provincelst, count)
    ########
#    if '北京' in province[1:]:
#        bjindex = province[1:].index('北京')
#        for i1, k1 in enumerate(pdata):
#            if i1 == bjindex:
#                k1.set_color('red')
    ########
    autolabel(pdata)
    plt.rcParams['font.sans-serif']=['SimHei']
    if maxp != 'no':
        plt.xlabel('【'+str(maxp) + '总' + str(maxv)+'例】')
    plt.ylabel(u'总确诊人数')
#    return fig
   #^^^^^^^END


def plot_dailyUpdate_city_f42(province, countkeyword, listdict):
    # 计算截止至请求时间，各省比前一天增加的人数
    ########
    tAlst, tBlst = r2d.timeseries(r2d.t0, 60*60*24)
    tAlst = [ti for ti in tAlst]
    tBlst = [ti for ti in tBlst]
    citylst = get_citylst(province, 'provinceName', 'cityName', alldict)
    ######## 得到更新数据
    updatalst = []
    for pi in citylst:
        tlst1, count1, tlst2, count2 \
                = r2d.city_evolution(province, 'provinceName', 
                        pi, 'cityName', countkeyword, listdict, tAlst, tBlst)
        countdelta = count2[-1] - count2[-2]
        updatalst.append((pi, countdelta))
    tnow = str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(tlst1[-1])))
    ######## 整理数据
    sortupdatalst = sorted(updatalst, key=lambda item:item[1], reverse=True)
    count = []
    provincelst = []
    for i1 in sortupdatalst:
        if i1[1] != 0:
            provincelst.append(proNorm(i1[0]))
            count.append(i1[1])
    print(provincelst)
    print(count)
    if len(provincelst) == 0:
        provincelst = [0,0]
        count = [0,0]
    ######################## PLOT
    plt.subplot(212)
    plt.subplots_adjust(bottom=0.05, top=0.95, left=0.07, right=0.98, hspace=0.3)
    plt.title(province+ '本日新增确诊 -- 截止至' + tnow + '\n 时间零点:' \
            +str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(r2d.t0))))
    maxp = 'no'
    if count[0]/5 > count[1] and count[0]>100:
        maxp = provincelst[0]
        maxv = count[0]
        provincelst = provincelst[1:]
        count = count[1:]
    pdata = plt.bar(provincelst, count)
    ########
#    if '北京' in province[1:]:
#        bjindex = province[1:].index('北京')
#        for i1, k1 in enumerate(pdata):
#            if i1 == bjindex:
#                k1.set_color('red')
    ########
    autolabel(pdata)
    plt.rcParams['font.sans-serif']=['SimHei']
    if maxp != 'no':
        plt.xlabel('【'+str(maxp) + '新增' + str(maxv)+'例】')
    plt.ylabel(u'一日新增确诊人数')
#    return fig
   #^^^^^^^END


###############################################################################
########################
ff = open(os.path.join(filepath, 'allprovince.txt'), 'r')
allprovince = [i1.replace('\n', '') for i1 in ff]
ff.close()
########################
alldict = dataNorm(os.path.join(filepath, 'savedata.txt'))
#alldict = dataNorm('savedata.txt')
print('#'*50)
print('#'*50)
print('#'*50)
###############################################################################
os.system(command='/bin/rm '+os.path.join(filepath, '1.png'))
os.system(command='/bin/rm '+os.path.join(filepath, '2.png'))
os.system(command='/bin/rm '+os.path.join(filepath, '3.png'))
os.system(command='/bin/rm '+os.path.join(filepath, '4.png'))
######################## runrunrunrun
fig1 = plt.figure(figsize=(12,6))
plot_china_f11(allprovince, 'confirmedCount', alldict)  # 全国趋势
plot_province_f12(['北京市', '天津市', '河北省', '河南省'], 
        'confirmedCount', alldict)  # 各省趋势
fig1.savefig(os.path.join(filepath, '1.png'))
########################
fig2 = plt.figure(figsize=(13, 10))
plot_provincesort_f21(allprovince, 'confirmedCount', alldict)   # 各省排名
plot_dailyUpdate_f22(allprovince, 'confirmedCount', alldict) # 新增排名
fig2.savefig(os.path.join(filepath, '2.png'))
########################
print(sys.argv)
print(len(sys.argv))
province1 = '北京市'
if len(sys.argv) ==2:
    if sys.argv[1] in allprovince:
        province1 = sys.argv[1]
#province1 = '湖北省'
########
fig3 = plt.figure(figsize=(12,6))
plot_province_time1_f31([province1], 'confirmedCount', alldict) # 省趋势与日增
plot_provinceson_time2_f32(province1, 'provinceName', 'cityName',    
        'confirmedCount', alldict)  # 辖区趋势
fig3.savefig(os.path.join(filepath, '3.png'))
########################
fig4 = plt.figure(figsize=(13, 10))
plot_citysort_f41(province1, 'confirmedCount', alldict)  # 辖区总量排名
plot_dailyUpdate_city_f42(province1, 'confirmedCount', alldict)  # 辖区新增排名
fig4.savefig(os.path.join(filepath, '4.png'))
#########################
#from PIL import Image
#Image.open(os.path.join(filepath, '1.png')).save(os.path.join(filepath, '1.gif'), 'GIF')
#Image.open(os.path.join(filepath, '2.png')).save(os.path.join(filepath, '2.gif'), 'GIF')
#Image.open(os.path.join(filepath, '3.png')).save(os.path.join(filepath, '3.gif'), 'GIF')
#Image.open(os.path.join(filepath, '4.png')).save(os.path.join(filepath, '4.gif'), 'GIF')

##plt.show()
