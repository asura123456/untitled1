__author__ = 'Administrator'

from bs4 import BeautifulSoup

import urllib.request

#reponse=urllib.request.urlopen('BeautifulSoup.html')

soup=BeautifulSoup(open('BeautifulSoup.html'),'lxml')

#for i in soup.find_all('a',id="link2"):
#    print(i)


print(soup.select('p .sister'))
print(soup.select('head>title'))
print(soup.select('a[id="link3"]'))
print(soup.select('p href="http://example.com/tillie"'))