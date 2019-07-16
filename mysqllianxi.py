

import pymysql
conn = pymysql.connect ( host ="localhost",user ="root",
passwd ="FuJW_1234",db="mystudy")
cursor = conn.cursor()

n=cursor.execute ("insert into `mystudy`.`student` (`name`,`age`,`sex`,`class`,`school`) values ('rola', '21', 'fem', '1st', 'lab')")
r=cursor.fetchall()
print(r,n)

m=cursor.execute ("select * from student")
s=cursor.fetchall()
print(s,m)

cursor.close ()
conn.close()



