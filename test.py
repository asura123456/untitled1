import re
import time
import pandas_train as pd


ti=time.struct_time(time.localtime())
df=pd.DataFrame(columns=['year', 'mouth', 'day','hour','minute','second','week','year_day','work_day'])
df.loc[1]=ti

print(df)
a = "kdl(al1ddd)23d345.jpgwidth"
b ="kdlal123345"
c="abc,1237877,456,789,mnp"
d="3adkkdk"
tinydict = {'name': 'john','code':6734, 'dept': 'sales'}
list = [ 'runoob', 786 , 2.23, 'john', 70.2 ]
reg=re.search("[a-z]+$", d)
ticks=time.time()
localtime=time.asctime(time.localtime(ticks))
today=time.strftime("%Y%m%d%h%m%s")
print(type(localtime))

#print(localtime)


