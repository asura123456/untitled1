
import pandas as pd
import os

filename=[]
mypath=os.getcwd()
filelist=os.listdir(mypath)
for i in filelist:
    if "附着" in i:
        filename.append(i)
print(filename)

for j in filename:
    df=pd.DataFrame(pd.read_csv(j,skiprows=[1],encoding="gbk"))
    df_sort=df.sort_values('用户流量MB',ascending=False).dropna(how='any')
    df_fi=df_sort.loc[df_sort['归属地(省)']!='福建'].reset_index().head(30)
    df_sub=pd.DataFrame((int(x[9:])/1771 for x in df_fi['用户号码']),index=df_fi.index,columns=["号码"])
    df_net=pd.DataFrame((("3G" if len(x)==13 else "4G") for x in df_fi['GCI']),index=df_fi.index,columns=["网络"])
    df_inner=pd.merge(df_sub,df_fi,how='inner',left_index=True,right_index=True)
    df_final=pd.merge(df_inner,df_net,how='inner',left_index=True,right_index=True)
    df_final.drop(['用户号码','GCI','index'],axis=1,inplace=True)
    df_final.to_csv(j[7:],encoding='gbk')