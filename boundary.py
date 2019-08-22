#!/usr/bin/env python
import math
import pandas as pd
import requests
import json
#import time
#import random

def GCJ2WGS(location):
    # location格式如下：locations[1] = "113.923745,22.530824"
   
    lon = float(location[0:location.find(",")])
    lat = float(location[location.find(",") + 1:len(location)])
    a = 6378245.0 # 克拉索夫斯基椭球参数长半轴a
    ee = 0.00669342162296594323 #克拉索夫斯基椭球参数第一偏心率平方
    PI = 3.14159265358979324 # 圆周率
    # 以下为转换公式
    x = lon - 105.0
    y = lat - 35.0
    # 经度
    dLon = 300.0 + x + 2.0 * y + 0.1 * x * x + 0.1 * x * y + 0.1 * math.sqrt(abs(x));
    dLon += (20.0 * math.sin(6.0 * x * PI) + 20.0 * math.sin(2.0 * x * PI)) * 2.0 / 3.0;
    dLon += (20.0 * math.sin(x * PI) + 40.0 * math.sin(x / 3.0 * PI)) * 2.0 / 3.0;
    dLon += (150.0 * math.sin(x / 12.0 * PI) + 300.0 * math.sin(x / 30.0 * PI)) * 2.0 / 3.0;
    #纬度
    dLat = -100.0 + 2.0 * x + 3.0 * y + 0.2 * y * y + 0.1 * x * y + 0.2 * math.sqrt(abs(x));
    dLat += (20.0 * math.sin(6.0 * x * PI) + 20.0 * math.sin(2.0 * x * PI)) * 2.0 / 3.0;
    dLat += (20.0 * math.sin(y * PI) + 40.0 * math.sin(y / 3.0 * PI)) * 2.0 / 3.0;
    dLat += (160.0 * math.sin(y / 12.0 * PI) + 320 * math.sin(y * PI / 30.0)) * 2.0 / 3.0;
    radLat = lat / 180.0 * PI
    magic = math.sin(radLat)
    magic = 1 - ee * magic * magic
    sqrtMagic = math.sqrt(magic)
    dLat = (dLat * 180.0) / ((a * (1 - ee)) / (magic * sqrtMagic) * PI);
    dLon = (dLon * 180.0) / (a / sqrtMagic * math.cos(radLat) * PI);
    wgsLon = lon - dLon
    wgsLat = lat - dLat
    return wgsLon,wgsLat

def crawl():
    df=pd.read_excel('D:\\340302.xls',sheet_name='Sheet1')
    #df_result=pd.DataFrame(columns=['PoiID','cityName','Name','location','address','Boundstr'])
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
               'Cookie': 'key=bfe31f4e0fb231d29e1d3ce951e2c780; isg=BJKSVdHhHcEsE2G6aDC0_yKI-lh0o5Y9D7ZnKlzuOsUwbz9pXDH8TW3J2yt2BA7V; UM_distinctid=167117440c3315-057c1acca6601-784a5037-100200-167117440c56bf; guid=a61f-024d-fc89-5e5d; cna=bNJyFLujMWMCAXB6j8K/Jtmm; dev_help=xRfqWuLEwqmadeE6s9NAVjMxMWRiODM4YjhkYTU5OTQxNmY2OWQ1NDQ0OWRhNmRkMjI1ZTNjNmM4MDUxODkyNzA3MTkyNTAzZmQyZTI4MDETOzrUF8i7BHfznR%2FPGrvlK6QGHSpoQMXZypUn6tN1RPB3ZhMVMoIGBz79vO4FhvDDQG3n8F7zpaxOqlNxjeSnjgZ69XdBuW4J1C985gD5aRuqqFBS7nIF1YlUyn7SaTM%3D; passport_login=MTMxOTgwODE3LGFtYXBfMTg2MDk2MDg2MTBBVlhUOVJoUHQsNmtqeDg3ZGd3aTRkcjJ5bzF5Y213d2czdDhlZjJtaTMsMTU0MjE4NjE0NSxPRE5oTnpNME0yRXlOall4T0RCaE5HUm1PRGt6TVRjeE9UYzVNVFEzTkdJPQ%3D%3D; _uab_collina=154218609343659688201686; CNZZDATA1255626299=1864638281-1542182007-null%7C1542246809'}
    i=0
    for x in df['id']:
        try:
            str='https://gaode.com/service/poiInfo?query_type=IDQ&pagesize=20&pagenum=1&qii=true&cluster_state=5&need_utd=true&utd_sceneid=1000&div=PC1000&addr_poi_merge=true&is_classify=true&zoom=11&id=' + x + '&city=340200'
            html = requests.get(url=str, headers=headers)
            jj = json.loads(html.text)
            #print(jj)
            c = jj['data']['poi_list']
            c = dict(c[0])
            #print(c)
            df.loc[i,'PoiID']=x
            df.loc[i,'cityName']=c['cityname']
            df.loc[i,'Name']=c['disp_name']
            df.loc[i,'location']="%s,%s"%GCJ2WGS(c['longitude'] + ',' + c['latitude'])
            df.loc[i,'address']=c['address']
            boundary=c['domain_list'][-1]['value']
            df.loc[i,'Boundstr']="_".join(["%s,%s" % GCJ2WGS(x) for x in boundary.split("_")])            
            print(x)
            print(i)
            #time.sleep(random.randint(0,3))  # 暂停0~3秒的整数秒，时间区间：[0,3]
            i=i+1
        except:
            print(i)
            print('获取不到'+ x)
            #time.sleep(random.randint(0,3))  # 暂停0~3秒的整数秒，时间区间：[0,3]
            i=i+1
    print('执行完毕')
    writer=pd.ExcelWriter("D:\\boundary11.xls")
    df.to_excel(writer,'sheet1')
    writer.save()

if __name__ == '__main__':
    crawl();


