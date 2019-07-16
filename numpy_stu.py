import numpy as np

a=np.random.rand(3,3)                    #创建指定形状(示例为10行10列)的数组(范围在0至1之间)
b=np.random.uniform(0,10)                #创建指定范围内的一个数
c=np.random.randint(0,10)                #创建指定范围内的一个整数
d=np.random.normal(1.75,0.1,(4,5))       #正态生成4行5列的二维数组
e=d[1:3,2:4]                             #截取第1至2行的第3至4列(从第0行算起)

f=np.arange(1,30,2)
g=f.reshape([5,3])
h=np.linspace(5,10,9)                   #线性生成linspace(start, stop, num, endpoint, retstep, dtype)
i=np.logspace(1,10,10,base=2)           #幂logscale(start, stop, num, endpoint, base, dtype)
j=slice(2,6,2)                          #start从0开始，end从1开始
print(i,i[2:6:2],i[j])                  #start从0开始，end从1开始
print(g,'\n',g[...,1:])                 #第二列


