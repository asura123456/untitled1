import re
import pandas_train as pd
import requests
#s=open('temp.txt','w+')

#li_re = re.compile('<li logr([\s\S]*?)</li>')
#li_list = re.findall(li_re,s)

#print(li_list)

#a=[1,2,3,4,5,6]
#print(len(a))
#for i in range(len(a)):
 #   print(i)


base_url="https://restapi.amap.com/v3/geocode/geo?parameters"
param={'address':'北京市朝阳区阜通东大街6号','key':'4dba6e72fd2739691550b2f03434794c'}
reponse=requests.get(base_url,param)
answer=reponse.json()
print(answer)