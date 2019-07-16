# -*- coding:utf-8 -*-

import itchat
import os
import datetime

import time
from apscheduler.schedulers.blocking import BlockingScheduler


# 登陆成功后开启定时任务
def after_login():
    sched.add_job(send_KPI_ChatRoom, 'interval', seconds=300)   ##5min
    sched.start()

def send_kpi_report():
   myKPIChatRoom = itchat.search_chatrooms(name=u'网优自动化群')
   srcFilePath = u"C:/Users/lizhangzheng/Desktop/lte每日指标监控.xlsx"
   dstFilePath = u"C:/Users/lizhangzheng/Desktop/lte.xlsx"
   srcFilePath_3G = u"C:/Users/lizhangzheng/Desktop/wcdma每日指标监控.xlsx"
   dstFilePath_3G = u"C:/Users/lizhangzheng/Desktop/wcdma.xlsx"

   if len(myKPIChatRoom) > 0:
      # 4G
      if os.path.exists("C:/Users/lizhangzheng/Desktop/4G.txt"):
         file_object = open("C:/Users/lizhangzheng/Desktop/4G.txt")
         try:
            all_the_text = file_object.read()
            itchat.send('%s' % all_the_text, toUserName=myKPIChatRoom[0]['UserName'])
         finally:
            file_object.close()
         if os.path.exists(srcFilePath):
            os.rename(srcFilePath, dstFilePath)  #改成英文名
            try:
               print("-----4G excel begin send")
               b = itchat.send_file(dstFilePath, toUserName=myKPIChatRoom[0]['UserName'])
            except:
               print("4G Excel transport failed")
         time.sleep(300)
         os.remove("C:/Users/lizhangzheng/Desktop/4G.txt")
         os.remove(dstFilePath) #发送完毕30s立刻删除报表

      # 3G
      if os.path.exists("C:/Users/lizhangzheng/Desktop/3G.txt"):
         file_object = open("C:/Users/lizhangzheng/Desktop/3G.txt")
         try:
            all_the_text = file_object.read()
            itchat.send('%s' % all_the_text, toUserName=myKPIChatRoom[0]['UserName'])
         finally:
            file_object.close()
         if os.path.exists(srcFilePath_3G):
            os.rename(srcFilePath_3G, dstFilePath_3G)  #改成英文名
            try:
               print("-----3G excel begin send")
               b = itchat.send_file(dstFilePath_3G, toUserName=myKPIChatRoom[0]['UserName'])
            except:
               print("3G Excel transport failed")
         time.sleep(300)
         os.remove("C:/Users/lizhangzheng/Desktop/3G.txt")
         os.remove(dstFilePath_3G)



def send_KPI_ChatRoom():
   print("---------Report CurrentTime")
   myChatRoom = itchat.search_chatrooms(name=u'联通指标通报')
   if len(myChatRoom) > 0:
      itchat.send('%s' % datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), toUserName=myChatRoom[0]['UserName'])
   send_kpi_report()

# 报表生成后微信发送文件
def KPIReport_send():
   myChatRoom = itchat.search_chatrooms(name=u'联通指标通报')
   if len(myChatRoom) > 0:
      ##itchat.send_msg("test", myChatRoom[0]['UserName'])
      itchat.send('%s' % "test", toUserName=myChatRoom[0]['UserName'])
      f = 'D:/lst.txt'
      # itchat.send("@fil@%s" % 'D:/lst.txt', toUserName=myChatRoom[0]['UserName'])
      if os.path.exists(f):
         print("----------file exist")
         try:
            b = itchat.send_file(f, toUserName=myChatRoom[0]['UserName'])
            print("success")
         except:
            print("fail")

if __name__ == '__main__':
   sched = BlockingScheduler()
   itchat.auto_login(hotReload=True)
   itchat.run(blockThread=False)
   after_login()

'''
from wxpy import *

bot = Bot(cache_path=True)
myKPIGroup = bot.groups().search('ooo')[0]
myKPIGroup.send('test')
myKPIGroup.send_file('test.txt')
##print(len(bot.groups().search("网优自动化支撑".encode('utf-8').decode('utf-8'))))
## myKPIgroup = bot.groups().search('网优自动化支撑').count()
## myKPIgroup.send_msg('test')
'''