#!/usr/bin/python
# -*- coding: UTF-8 -*-

#import urllib

#page=urllib.urlopen('http://www.runoob.com/python/python-exercise-example1.html')
# !/usr/bin/python
# -*- coding: UTF-8 -*-

import urllib.request
import re
#page = urllib.request.urlopen('http://tools.android-studio.org/index.php')
#htmlcode = page.read()#读取页面源码
#print(htmlcode)

#pageFile = open('pageCode.txt','wb+')#以写的方式打开pageCode.txt
#pageFile.write(htmlcode)
#pageFile.close()

def get_html(url):
    page=urllib.request.urlopen(url)
    html=page.read()
    return html
reg =b'<li logr([\s\S]*?)</li>'#正则表达式
reg_img = re.compile(reg)#编译一下，运行更快
imglist = reg_img.findall(get_html(r'http://hz.58.com/pinpaigongyu/pn/1/?minprice=2000_4000'))#进行匹配
for img in imglist:
 print (img.decode('utf-8'))

