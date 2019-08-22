import requests
from urllib import request
import pandas as pd
import json

base_url = "https://restapi.amap.com/v3/place/text"
detail_url = "https://www.amap.com/detail/get/detail?"
mykey = '146261b0458899501a01bd9dbd2e2a05'


def get_poi_id(keywd, city):
    param = {'keywords': keywd, 'city': city, 'citylimit': True, 'key': mykey}
    reponse = requests.get(base_url, param)
    answer = reponse.json()
    return answer['pois'][0]['id']


def get_poi_polygon(poi_id):
    param = {'id': poi_id, 'key': mykey}
    reponse=request.urlopen(detail_url+poi_id)
    html = reponse.read()
    answer=json.loads(html)
    return answer


if __name__ == '__main__':

    df = pd.DataFrame(pd.read_excel('d:/poi_xuqiu.xlsx'))
    keywds = df['需求信息']
    citys = df['城市']
    for i in range(0, len(df)):
        ids = get_poi_id(keywds[i], citys[i])
        polygon = get_poi_polygon(ids)
        print(polygon)
        i += 1