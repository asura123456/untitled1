__author__ = 'Administrator'
import time
a="163"
b=a.encode('utf-8')

print(b)

c=[x**2 for x in range(10) if x%3==0]
d=[(x,y) for x in range(3) for y in range(3)]
print(c,d)

username=input('请输入你的名字：')
date=time.strftime('%y-%m-%d %H:%M:%S',time.localtime())
print('你好，'+username+',现在的时间是：'+date)
print('你好，%3.6f，现在的时间是：%s' %(float(username),date))
print('你好，{name}，现在的时间是：{date}' .format(date=date,name=username))


