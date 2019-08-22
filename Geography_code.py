import re
import pandas_train as pd
import requests


def transfer(address):
    base_url="https://restapi.amap.com/v3/geocode/geo?parameters"
    param={'address':address,'key':'b87877313ab15b69b179527fff696985'}   #mykey:4dba6e72fd2739691550b2f03434794c,cfkey:b87877313ab15b69b179527fff696985
    reponse=requests.get(base_url,param)
    answer=reponse.json()
    return answer['geocodes'][0]['location']

if __name__ == '__main__':

    k=0
    sub_number=[]
    post_address=[]
    userData=pd.read_csv('c:\sender_five.csv',encoding='gbk')
    userDict=userData.to_dict('index')
    for i in range(0,len(userDict)):
        sub_number.append(userDict[i]['订购号码'])
        post_address.append(userDict[i]['配送地址'])

    df=pd.DataFrame(columns=['用户号码','用户地址','经纬度'])
    for j in post_address:
        user_location=transfer(j)
        df.loc[k]=[sub_number[k],j,user_location]
        k+=1
 #   while k<len(post_address):
  #      user_location=transfer(post_address[k])
  #      df.loc[k]=[sub_number[k],post_address[k],user_location]
   #     k=k+1
    resuleData='c:\geo_converse.csv'
    df.to_csv(resuleData,encoding='gbk',index=False)



# info(verbose=True)  shape  dtype isna()  isnull() unique() head(3) tail(3) values dropna(how='any') fillna(value=0,inplace=True) drop_duplicates(keep=lase) replace
#df.rename(columns={'city':'my_city'})  set_index('id') sort_values(by=['age'])sort_index()

