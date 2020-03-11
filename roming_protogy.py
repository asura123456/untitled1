import pandas as pd

filedate=input("请输入需执行的日期：")
filename_pro="南平协议大小类流量"+str(filedate)+".csv"
filename_packet="流量小区归属地信息-2020"+str(filedate)+".csv"
filename_out="漫入流量日TOPN"+str(filedate)+".csv"

df=pd.DataFrame(pd.read_csv(filename_pro,encoding="utf-8"))
df2=pd.DataFrame(pd.read_csv(filename_packet,encoding="gbk"))

df_sub=pd.DataFrame((('46001D970'+str(x*1771)) for x in df2["号码"]),columns=["用户号码"])         #用户号码转成加密号码
df2=df2.join(df_sub)                                                                     #合并，用于过滤TOP30的索引
df_inner=pd.merge(df,df2,how='inner',on="用户号码")                                     #数据合并，得到TOP30数据
df_pro=df_inner.groupby(["用户号码"],as_index=False)['流量(MB)'].max()                  #用户号码分组求最大
df_inner.drop(['SUB_PROT_ID','PROTOCOL_ID','index','用户号码'],axis=1,inplace=True)     #删除无用字段

df_final=pd.merge(df_pro,df_inner,how='inner',on="流量(MB)")                            #过滤用户流量最大

df_final.to_csv(filename_out,encoding="gbk")
print("执行完毕！")