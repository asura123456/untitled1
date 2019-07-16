import matplotlib.pyplot as plt
import numpy as np

plt.style.use('fivethirtyeight')
fig,ax=plt.subplots()
x=np.linspace(0,10,1000)
y=np.cos(2*np.pi*x)*np.exp(-x)+1
y1=-np.cos(2*np.pi*x)*np.exp(-x)+1
ax.axis([0,6,0.3,1.8])
ix=(x>1)&(x<3)

ax.plot(x,y,label="$\cos(2\pi{x})\ e^{-x}+1$",linewidth=1)   #p 五角星；s 正方形; d 菱形; h 六边形;-实线;--双划线；：虚线；:.点划线
ax.plot(x,y1,label="$-\cos(2\pi{x})\ e^{-x}+1$",linewidth=1)

ax.fill_between(x,y,y1,where=ix,facecolor='hotpink',alpha=0.3)
ax.text(2,0.6,r"$\int_a^bf(x)\mathrm{dx}$",horizontalalignment='center')
plt.title("MatPlot")
plt.xlabel("time(s)")
plt.ylabel("volt(mv)")

plt.legend(loc=8)
plt.show()
