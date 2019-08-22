import requests
import json
import re
import pandas as pd
from pandas.io.json import json_normalize 
import math
from urllib import request
from urllib.parse import quote
import time
import os
class GPS():
    def __init__(self):
        self.PI = 3.14159265358979324
        self.x_pi = 3.14159265358979324 * 3000.0 / 180.0
        self.MCBAND = (12890594.86, 8362377.87, 5591021, 3481989.83, 1678043.12, 0)
        self.MC2LL = ([1.410526172116255e-8, 0.00000898305509648872, -1.9939833816331,
                  200.9824383106796, -187.2403703815547, 91.6087516669843, - 23.38765649603339,
                  2.57121317296198, -0.03801003308653, 17337981.2],
                 [-7.435856389565537e-9, 0.000008983055097726239, -0.78625201886289,
                  96.32687599759846, -1.85204757529826, -59.36935905485877, 47.40033549296737,
                  -16.50741931063887, 2.28786674699375, 10260144.86],
                 [-3.030883460898826e-8, 0.00000898305509983578, 0.30071316287616,
                  59.74293618442277, 7.357984074871, -25.38371002664745, 13.45380521110908,
                  -3.29883767235584, 0.32710905363475, 6856817.37],
                 [-1.981981304930552e-8, 0.000008983055099779535, 0.03278182852591, 40.31678527705744,
                  0.65659298677277, -4.44255534477492, 0.85341911805263, 0.12923347998204,
                  -0.04625736007561, 4482777.06],
                 [3.09191371068437e-9, 0.000008983055096812155, 0.00006995724062, 23.10934304144901,
                  -0.00023663490511, -0.6321817810242, -0.00663494467273, 0.03430082397953,
                  -0.00466043876332, 2555164.4],
                 [2.890871144776878e-9, 0.000008983055095805407, -3.068298e-8, 7.47137025468032,
                  -0.00000353937994, -0.02145144861037, -0.00001234426596, 0.00010322952773,
                  -0.00000323890364, 826088.5])


    def delta(self, lat, lon):
        # Krasovsky 1940
        #
        # a = 6378245.0, 1/f = 298.3
        # b = a * (1 - f)
        # ee = (a^2 - b^2) / a^2
        a = 6378245.0  # a: 卫星椭球坐标投影到平面地图坐标系的投影因子。
        ee = 0.00669342162296594323  # ee: 椭球的偏心率。
        dLat = self.transformLat(lon - 105.0, lat - 35.0)
        dLon = self.transformLon(lon - 105.0, lat - 35.0)
        radLat = lat / 180.0 * self.PI
        magic = math.sin(radLat)
        magic = 1 - ee * magic * magic
        sqrtMagic = math.sqrt(magic)
        dLat = (dLat * 180.0) / ((a * (1 - ee)) / (magic * sqrtMagic) * self.PI)
        dLon = (dLon * 180.0) / (a / sqrtMagic * math.cos(radLat) * self.PI)
        return {'lat': dLat, 'lon': dLon}


    def gcj_encrypt(self, wgsLat, wgsLon):
        # WGS-84 to GCJ-02
        if self.outOfChina(wgsLat, wgsLon):
            return {'lat': wgsLat, 'lon': wgsLon}
        d = self.delta(wgsLat, wgsLon)
        return {'lat': wgsLat + d['lat'], 'lon': wgsLon + d['lon']}


    def gcj_decrypt(self, gcjLat, gcjLon):
        # GCJ-02 to WGS-84
        if self.outOfChina(gcjLat, gcjLon):
            return {'lat': gcjLat, 'lon': gcjLon}
        d = self.delta(gcjLat, gcjLon)
        return {'lat': gcjLat - d['lat'], 'lon': gcjLon - d['lon']}


    def gcj_decrypt_exact(self, gcjLon,gcjLat):
        # GCJ-02 to WGS-84 exactly
        initDelta = 0.01
        threshold = 0.000000001
        dLat = initDelta
        dLon = initDelta
        mLat = gcjLat - dLat
        mLon = gcjLon - dLon
        pLat = gcjLat + dLat
        pLon = gcjLon + dLon
        wgsLat = wgsLon = i = 0
        while True:
            wgsLat = (mLat + pLat)/2
            wgsLon = (mLon + pLon)/2
            tmp = self.gcj_encrypt(wgsLat, wgsLon)
            dLat = tmp['lat'] - gcjLat
            dLon = tmp['lon'] - gcjLon
            if ((math.fabs(dLat) < threshold) and (math.fabs(dLon) < threshold)): break
            if dLat>0 : pLat = wgsLat
            else : mLat = wgsLat
            if dLon>0 : pLon = wgsLon
            else : mLon = wgsLon
            i=i+1
            if i>10000 : break
        return round(wgsLon,7),round(wgsLat,7)


    def bd_gcj(self, bdLon,bdLat):
        # BD-09 to GCJ-02
        x = bdLon - 0.0065
        y = bdLat - 0.006
        z = math.sqrt(x * x + y * y) - 0.00002 * math.sin(y * self.x_pi)
        theta = math.atan2(y, x) - 0.000003 * math.cos(x * self.x_pi)
        gcjLon = z * math.cos(theta)
        gcjLat = z * math.sin(theta)
        return gcjLon,gcjLat

    def bd_wgs(self,bdLon,bdLat):
        # BD-09 to WGS-84
        gcj = self.bd_gcj( bdLon,bdLat)
        wgs = self.gcj_decrypt_exact(gcj[0], gcj[1])
        return  wgs


    def mercator_decrypt(self, mercatorLat, mercatorLon):
        # Web mercator to WGS-84
        # mercatorLat -> y mercatorLon -> x
        x = mercatorLon/20037508.34 * 180.
        y = mercatorLat/20037508.34 * 180.
        y = 180 / self.PI * (2 * math.atan(math.exp(y * self.PI / 180.)) - self.PI / 2)
        return {'lat' : y, 'lon' : x}


    def outOfChina(self, lat, lon):
        if lon<72.004 or lon>137.8347 : return True
        if lat<0.8293 or lat>55.8271 : return True
        return False

    def transformLat(self, x, y):
        ret = -100.0 + 2.0 * x + 3.0 * y + 0.2 * y * y + 0.1 * x * y + 0.2 * math.sqrt(math.fabs(x))
        ret += (20.0 * math.sin(6.0 * x * self.PI) + 20.0 * math.sin(2.0 * x * self.PI)) * 2.0 / 3.0
        ret += (20.0 * math.sin(y * self.PI) + 40.0 * math.sin(y / 3.0 * self.PI)) * 2.0 / 3.0
        ret += (160.0 * math.sin(y / 12.0 * self.PI) + 320 * math.sin(y * self.PI / 30.0)) * 2.0 / 3.0
        return ret

    def transformLon(self, x, y):
        ret = 300.0 + x + 2.0 * y + 0.1 * x * x + 0.1 * x * y + 0.1 * math.sqrt(math.fabs(x))
        ret += (20.0 * math.sin(6.0 * x * self.PI) + 20.0 * math.sin(2.0 * x * self.PI)) * 2.0 / 3.0
        ret += (20.0 * math.sin(x * self.PI) + 40.0 * math.sin(x / 3.0 * self.PI)) * 2.0 / 3.0
        ret += (150.0 * math.sin(x / 12.0 * self.PI) + 300.0 * math.sin(x / 30.0 * self.PI)) * 2.0 / 3.0
        return ret


    class GISError(Exception):
        """GIS Exception
        """

    def convert_MCT_2_BD09(self,lon, lat):

        ax = None
        for j in range(len(self.MCBAND)):
            if lat >= self.MCBAND[j]:
                ax = self.MC2LL[j]
                break

        if ax is None:
            raise print("error lat:%s" % lat)

        e = ax[0] + ax[1] * abs(lon)
        i = abs(lat) / ax[9]
        aw = ax[2] + ax[3] * i + ax[4] * i * i + ax[5] * i * i * i + \
             ax[6] * i * i * i * i + ax[7] * i * i * i * i * i + ax[8] * i * i * i * i * i * i
        if lon < 0:
            e *= -1
        if lat < 0:
            aw *= -1

        return e,aw
   

def getPOIdata():
    global total_record
    josn_data = get_data(1)
    if (total_record % page_size) != 0:
        page_number = int(total_record / page_size) + 2
    else:
        page_number = int(total_record / page_size) + 1

    with open(json_name, 'w') as f:
        f.write(json.dumps(josn_data).rstrip(']'))
        for each_page in range(2, page_number):
            html = json.dumps(get_data(each_page)).lstrip('[').rstrip(']')
            if html:
                html = "," + html
            f.write(html)
        f.write(']')
    print('POI数据完成获取')

def get_data(pageindex):
    global total_record
    time.sleep(0.5)
    url = url_amap.replace('pageindex', str(pageindex))
    url = quote(url, safe='/:?&=')
    html = ""
    with request.urlopen(url) as f:
        html = f.read()
    rr = json.loads(html)
    if total_record == 0:
        total_record = int(rr['total'])
    return rr['results']

def getRegion_baidu():
    translateGps = GPS()
    col_name=['uid','name','address','bd_lng','bd_lat','gcj02_lng','gcj02_lat','wgs84_lng','wgs84_lat']
    df = pd.DataFrame(columns=col_name)
    fp = open(json_name, 'r')
    result = json.loads(fp.read())
    df1 = json_normalize(result)
    df1=df1[['uid','province','city','area', 'name','address','detail_info.tag', 'location.lat', 'location.lng']]
    for i in result:
        uid=i['uid']
        poinstUrl = 'http://map.baidu.com/?pcevaname=pc4.1&qt=ext&uid={}&ext_ver=new&l=12'
        r_point = requests.get(poinstUrl.format(uid),headers = {'user-agent':'Mozilla/5.0'})
        r_point.encoding = 'ascii'

        jd = json.loads(r_point.text)        
        strjd=str(jd)
        if strjd.find("'content': {'geo'")!=-1:
            points = re.findall('[0-9]{8}.[0-9]+,[0-9]{7}.[0-9]+',jd['content']['geo'])
        
            sub_lat_lng = []        

            for strs in points:
                temp = strs.split(',')
                temp[0] = round(float(temp[0]),6)
                temp[1] = round(float(temp[1]),6)
                bd09 = translateGps.convert_MCT_2_BD09(temp[0],temp[1])
                gcj02=translateGps.bd_gcj(bd09[0],bd09[1])
                wgs84=translateGps.bd_wgs(bd09[0],bd09[1])
                txt=(i['uid'],i['name'],i['address'])
                tmp=str(sub_lat_lng)     
                jwd=str(bd09[0])+", "+str(bd09[1])           
                if tmp.find(jwd)==-1:
                    sub_lat_lng.append(txt+bd09+gcj02+wgs84)
                df_temp = pd.DataFrame(sub_lat_lng,columns=col_name)
            df=pd.concat([df,df_temp])
    return df1,df


if __name__=="__main__":
    
    json_name = 'data_tmap.json'
    df2=pd.DataFrame(pd.read_excel('d:/gaoxiao.xlsx'))
    city='杭州市'
    tag='教育培训'
    api_key='KUPUfwHIQCDljg9idU0q7gooSWI8L2gF'

    keyword = df2['名称']
    for kwd in keyword:
        url_amap = 'http://api.map.baidu.com/place/v2/search?query=' + kwd + '&tag=' + tag + '&page_size=20&page_num=0&scope=2&region=' + city + '&coord_type=3&output=json&ak=' + api_key
        page_size = 20
        page_index = r'page_num=1'
        total_record = 0
        getPOIdata()
        df=getRegion_baidu()

    writer = pd.ExcelWriter(r'D:\biankuang_baidu.xlsx')
    df[0].to_excel(writer,sheet_name='POI_list')
    df[1].to_excel(writer,sheet_name='AOI_list')
    writer.save()
    print('AOI数据完成获取')