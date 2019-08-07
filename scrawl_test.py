import requests
from urllib import request
import json

url='https://www.amap.com/detail/get/detail?id=B000A816R6'
headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
    'Host':'www.amap.com',
    'Cookie': 'UM_distinctid=16c1caae97b35-0d8bfd813-4349052c-100200-16c1caae97d29; passport_login=MjQyMTQ4MDU0LGFtYXBfMTg2MDU5OTEzNjFBQ3VQaHVIM2osb3V6NGk3YnptcG5icXZrNmg2bGFrbmFmbW5sNzJ2ZHIsMTU2Mzg3MTc4NixOREUxWm1ZME9XUTVNVFZoWmprelpHVTNaamd3WkRabFkyWTFPVE13WldFPQ%3D%3D; dev_help=076cjGN6uyg6EIEygQEU9mY0YzY0ZTYzYzQ3NmQ2MmJkOTFhMmNlNjhkMTc3NjMxOTQ1YjY3MTg5MWVmNWM1MTA0ZWYyYmUxZGY3ZmY5OGI%2BugRfGX1T5XrTHQxwhbFJStNrGyaj4MBF%2B64l8hyic8%2FusEFVaJhh%2FtGMbcmS4h4%2FSlXUQJ0dSy0ha5UWyaAAcS9SbPN4K1Ft5k7aPRXF8UMga5VpHN%2Bf9%2BOSGGTOSaw%3D; guid=52b5-e805-1388-9908; cna=knO0FWvaBl4CAdz5v6rhARcf; _uab_collina=156508106338566968589276; CNZZDATA1255626299=1603378664-1565079939-%7C1565079939; l=cBPUv6n4qUH1aju8BOfZdurza77T2CdjGsPzaNbMiICPO5Bv7m9hWZFa36KJCnGVL6lBB3-qf7eUBPT7AyUCh1iBQ21A6M9c.; isg=BIqKf20W448obm8gedvhLzEb23Asew7VnzSxRBTGi11oxz6B2Q9Y5Vvx13O-N4Zt',
    'X-Requested-With': 'XMLHttpRequest',
    'Referer': 'https://www.amap.com/place/B000A816R6'
}
user_agent="Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36"
proxy = {'https':'120.83.106.16:9999', 'https':'47.94.85.21:3129'}

sel_proxy=request.ProxyHandler(proxy)
opener=request.build_opener(sel_proxy)

request.install_opener(opener)
opener.addheaders=[('User-Agent',user_agent)]
html=request.urlopen(url).read()

tt=json.loads(html)

print(tt)