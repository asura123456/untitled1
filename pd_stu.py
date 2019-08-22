import pandas as pd
import numpy as np
df=pd.DataFrame(pd.read_excel('d:\dataf.xls'))
#df['price']=df['price'].fillna(df['price'].mean())                                                     #数据清洗
df1=pd.DataFrame({
    "id":[1001,1002,1003,1004,1005,1006,1007,1008],
    "gender":['male','female','male','female','male','female','male','female'],
    "pay":['Y','N','Y','Y','N','Y','N','Y',],
    "m-point":[10,12,20,40,40,40,30,20]
})
df_inner=pd.merge(df,df1,how='left')
df_inner['city']=df_inner['city'].str.lower()                                                                       #数据清洗
df_inner.set_index('id')
df_inner=df_inner.sort_values(by=['age'])                                                                                  #数据排序
df_inner=df_inner.sort_index()                                                                                             #数据排序
df_inner['group']=np.where(df_inner['price']>3000,'high','low')                                                            #数据分组
df_inner.loc[(df_inner['city']=='beijing')&(df_inner['price']>3000),'flag']=1                                              #数据分组
df_inner['flag']=df_inner['flag'].astype('str')
df_inner['flag']=df_inner['flag'].map(str.strip)                                                                    #数据清洗

split=pd.DataFrame((x.split('-') for x in df_inner['category ']),index=df_inner.index,columns=['category_new','size'])       #数据分列

df_split=pd.merge(df_inner,split,right_index=True,left_index=True)                                                           #数据分列合并

cuts=[15,25,35,45,55]                                                       #数据切片
cates=pd.cut(df_split['age'],cuts,right=False)                              #数据切片


#df_inner=df_inner.dropna(how='any')                                               #数据清洗
df_inner.to_excel('d:\dataf_out.xls')
print(df_split)
print(pd.value_counts(cates))                                                #数据切片

print(df_split.loc[df_split['city'].isin(['beijing','shanghai'])])