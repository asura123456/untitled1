import webbrowser

from wxpy import *

from pyecharts import Line,Map

x = ["福建", "广东", "上海", "北京", "四川", "陕西"]
y =  [40, 12, 13, 10, 10, 10]

line=Line("比例")
line.add("", x, y, mark_point=["average"])

kwarg1=dict(maptype='china', is_visualmap=True,visual_text_color='#e6f')
map=Map("地图")

map.add("收入分布",x,y,**kwarg1)

line.render('test.html')
map.render('map.html')

webpath=r'C:\Users\Administrator.WIN7U-20180806T\AppData\Roaming\360se6\Application\360se.exe'
webbrowser.register('360se',None,webbrowser.BackgroundBrowser(webpath))
webbrowser.get('360se').open('map.html')

# bot=Bot(cache_path='true')
# my_friend=bot.friends()

#  for friend in my_friend:
 #    print(friend)