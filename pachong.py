from bs4 import BeautifulSoup
from urllib.parse import urljoin
import requests
import csv
import time

url="http://hz.58.com/pinpaigongyu/pn/{page}/?minprice=2000_4000"
page=0

csv_file=open(r"C:\Users\Administrator.WIN7U-20180806T\Desktop\houseNew.csv",'w+',newline='')
csv_writer=csv.writer(csv_file,delimiter=',')

while True:
    time.sleep(5)
    page+=1
    response=requests.get(url.format(page=page))
    html=BeautifulSoup(response.text,"lxml")

    house_list=html.select(".list>li")

    if not house_list:
        break

    for house in house_list:
        house_title=house.select("h2")[0].string
        house_url=urljoin(url,house.select("a")[0]["href"])
        house_pic=urljoin(url,house.select("img")[0]["lazy_src"])
        house_info_list=house_title.split()

        if "公寓" in house_info_list[0] or "青年社区" in house_info_list[0]:
            house_location=house_info_list[0]

        else:
            house_location=house_info_list[1]

        house_money=house.select(".money")[0].select("b")[0].string

        csv_writer.writerow([house_title,house_location,house_money,house_pic])
        csv_file.closed

