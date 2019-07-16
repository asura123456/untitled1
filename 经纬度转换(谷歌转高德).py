__author__ = 'feng'
import requests
import pandas as pd


def parse():
    datas = []
    datas1=[]
    datas2=[]
    totalListData = pd.read_csv('E:\locs.csv',encoding='gbk')
    totalListDict = totalListData.to_dict('index')
    for i in range(0, len(totalListDict)):
        datas.append(str(round(totalListDict[i]['centroidx'],6)) + ',' + str(round(totalListDict[i]['centroidy'],6)))
        datas1.append(str(totalListDict[i]['name']))
        datas2.append(str(totalListDict[i]['count']))
    return datas,datas1,datas2


def transform(location):
    parameters = {'coordsys': 'gps', 'locations': location, 'key': 'b87877313ab15b69b179527fff696985'}
    base = 'http://restapi.amap.com/v3/assistant/coordinate/convert'
    response = requests.get(base, parameters)
    answer = response.json()
    return answer['locations']



if __name__ == '__main__':
    i = 0
    str_file = "E:\gd_output\locdetail_gps2gd_output"
    df = pd.DataFrame(columns=['index', 'src_lon_lat', 'lon_lat','name1','count'])
    s_lonlat,name,count= parse()
    for j in s_lonlat:
        d_lonlat=transform(j)
        df.loc[i] = [i, j, d_lonlat,name[i],count[i]]
        i = i + 1
    str1 = "e:\gd_output\locdetail_gps2gd_output_api.csv"
    df.to_csv(str1,encoding='gbk', index=False)
