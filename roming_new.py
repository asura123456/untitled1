
import pandas as pd
import os

#filename=[]
#mypath=os.getcwd()
#filelist=os.listdir(mypath)
#for i in filelist:
 #   if "附着" in i:
 #       filename.append(i)
#print(filename)

#for j in filename:
df=pd.DataFrame(pd.read_csv("南平附着用户的流量小区归属地信息-20200309.csv",dtype={"用户流量MB":object,"归属地(省)":object,"归属地(市)":object},encoding="gbk"))
#df_group=df.groupby(["用户号码"],as_index=False)['用户流量MB'].agg([max,sum])      #分组，提取最大、汇总流量
#df_inner=pd.merge(df_group,df,str='inner',on='用户号码')                           #与源表合并
#df_fi=df_inner.loc[df_inner['用户流量MB']==df_inner['max']]    #筛选最大流量的子协议
#df_sort=df_fi.sort_values('sum',ascending=False).dropna(how='any').reset_index().head(30)    #按用户使用总流量排序

print(df[5])