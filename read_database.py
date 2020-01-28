#!/usr/bin/env python3.7
#
import re
import sys
import time
sys.path.append('../DXY-2019-nCoV-Crawler')
import read2019nCoVdata as r2d
from crawler_2019_nCoV_data import readindatalst as readdata
import matplotlib.pyplot as plt
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


###############################################################################
tlstA, tlstB = r2d.timeseries(r2d.t0, 60*60*12)
tlstA = [ti for ti in tlstA]
tlstB = [ti for ti in tlstB]
########################
ff = open('allprovince.txt', 'r')
allprovince = [i1.replace('\n', '') for i1 in ff]
ff.close()
########################
alldict = dataNorm('savedata.txt')
########################
tlst1bj, count1bj, tlst2bj, count2bj = r2d.province_evolution('湖北省', 
        'confirmedCount', alldict, tlstA, tlstB)
tlstC, countC = r2d.nationalevolution(allprovince, 'confirmedCount', alldict, tlstA, tlstB)
tlstC = [(ti-r2d.t0)/3600/24 for ti in tlstC]
tlst1bj = [(ti-r2d.t0)/3600/24 for ti in tlst1bj]
tlst2bj = [(ti-r2d.t0)/3600/24 for ti in tlst2bj]
print(count1bj[-1])
print(countC[-1])
########################
plt.figure()
plt.plot(tlst1bj, count1bj, '.-')
plt.plot(tlst2bj, count2bj, '.-')
plt.plot(tlstC, countC, '.-')
plt.show()

