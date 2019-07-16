
import requests

#猎鹰轨迹地址
s_add='http://tsapi.amap.com/v1/track/service/add'
s_list='http://tsapi.amap.com/v1/track/service/list'
t_add='http://tsapi.amap.com/v1/track/terminal/add'
t_list='http://tsapi.amap.com/v1/track/terminal/list'
t_add_col='http://tsapi.amap.com/v1/track/terminal/column/add'
t_list_col='http://tsapi.amap.com/v1/track/terminal/column/list'

#参数
falcon_key='4dba6e72fd2739691550b2f03434794c'
s_aparam={'key':falcon_key,'name':'lieyingguiji','desc':'demo'}
s_lparam={'key':falcon_key}
t_aparam={'key':falcon_key,'sid':'34798','name':'nuoio'}
t_lparam={'key':falcon_key,'sid':'34798'}
t_aparam_col={'key':falcon_key,'sid':'34798','column':'connect','type':'int'}
t_lparam_col={'key':falcon_key,'sid':'34798'}


#s_response=requests.post(s_add,s_aparam)      #添加Service    sid:34798
#t_resquests=requests.post(t_add,t_aparam)     #添加Terminal   tid:102853645

s_l_resquests=requests.get(s_list,s_lparam)   #罗列Service
t_l_resquests=requests.get(t_list,t_lparam)   #罗列Terminal
t_a_resquests_col=requests.post(t_add_col,t_aparam_col)  #添加Terminal字段
t_l_resquests_col=requests.get(t_list_col,t_lparam_col)  #罗列Terminal字段

servers=s_l_resquests.text
terminal=t_l_resquests.text
#terminal_a_col=t_a_resquests_col.text
terminal_l_col=t_l_resquests_col.text
t_dict=t_l_resquests_col.json()     #高德API JSON转字典

print(servers)
print(terminal)
print(terminal_l_col)
print(t_dict['data']['results'][1]['column'])
