import cx_Oracle
import csv
import os
import re
import time


db = cx_Oracle.connect('**', '**', '134.149.*.*/OSS')
cursor = db.cursor()

today=time.strftime('%Y%m%d')
namedate=str(int(today)-1)
startdate="'"+str(int(today)-1)+"'"
enddate="'"+str(int(today))+"'"
print(startdate);print(enddate);

path=os.getcwd()
f = open(path+'\指标脚本.sql')
full_sql = f.read()
full_sql=re.sub('&start_date',startdate,full_sql)
full_sql=re.sub('&end_date',enddate,full_sql)
print(full_sql)
sql_commands = full_sql
cursor.execute(sql_commands)
result = cursor.fetchall()

suffix = ".csv"
newfile ='/南平联通KPI指标监控_'+ namedate + suffix
if not os.path.exists(newfile):
    f = open(newfile, 'w')
    print(newfile)
    f.close()
    print(newfile + " created.")
else:
    print(newfile + " already existed.")

with open(path+"\\" +'/南平联通KPI指标监控_'+ namedate +".csv","w",newline='') as csvfile:
    writer = csv.writer(csvfile)
    title = [(
             'PERIOD_START_TIME', 'AREA', 'LNCEL_TAC', 'LNCEL_ENB_ID', 'LNCEL_LCR_ID', 'LNCEL_CELL_NAME', 'RRC建立成功率服务类',
             'RRC建立成功率非服务类', 'RRC拥塞率(%)', 'ERAB建立成功率(ALL)(%)', 'ERAB拥塞率(%)', '无线接通率(ALL)(%)', '掉线率(%)', 'eNB内切换成功率(%)',
             'S1切换成功率(%)', 'eNB间X2切换出请求次数1', 'eNB间X2切换出请求次数', 'eNB间X2切换出成功次数', 'X2切换成功率(%)', '切换成功率(%)', 'eNB切换成功次数',
             'eNB切换请求次数', 'S1切换成功次数', 'S1切换请求次数', 'X2切换成功次数', 'X2切换请求次数', 'X2占比(%)', '小区下行吞吐量(G)', '小区上行吞吐量(G)',
             '小区下行吞吐率(kbps)', '小区上行吞吐率(kbps)', '下行PRB平均利用率(%)', '上行PRB平均利用率(%)', '双流占比(ALL)(%)', 'FL16小区内平均用户数',
             'FL16小区内最大用户数', 'FL16A小区内平均用户数', 'FL16A小区内最大用户数', '系统每PRB干扰平均值', '系统每PRB干扰最大值', 'CSFB成功率(%)',
             '基础型CS Fallback次数', '增强型CS Fallback次数', 'LTE弱覆盖重定向比例%', '覆盖触发重定向W总数', '重定向到WCDMA的总次数', 'LTE弱覆盖比例%',
             '覆盖触发重定向W总数', 'PS域ERAB建立成功次数', '测量基础重定向次数', '盲重定向次数', '增强型重定向', 'CQI大于等于7比例(%)', '去尾平均速率')]
    writer.writerows(title)
    writer.writerows(result)
cursor.close()