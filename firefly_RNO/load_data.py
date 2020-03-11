# -*- coding: utf-8 -*-
"""
Created on Wed Jul  3 16:14:14 2019

@author: wangjinyang
"""
import pandas as pd
import numpy as np
from functools import reduce #排列组合高阶函数
np.set_printoptions(suppress=True) # 不以科学计数法显示
adr=r"F:\项目资料\联通日常\201907天馈寻优\Opt_data.xlsx"
# 经纬度、高程计算距离
import math
EARTH_REDIUS = 6378.137
a = 6378245
b = 6356752.3142

def rad(d):
    return d * math.pi / 180.0
    
class Ant:    #lng	lat	 Azimuth	Downdip_angle 	height 	Fre_DL 	power
    def __init__(self,x1,y1,azu,Downdip_angle,hb,fre,RsPow,x2,y2):
        self.RsPow=RsPow
        self.hb=hb
        self.fre=fre
        self.x1=x1
        self.y1=y1
        self.x2=x2
        self.y2=y2       
        self.azu=azu
        self.Downdip_angle=Downdip_angle
        self.Distance=0
        self.azimuth_Angle=0
        self.Antenna_weight=0
    def getDistance(self):
        lat1=self.y1
        lat2=self.y2
        lng1=self.x1
        lng2=self.x2
        h1=h2=0
        radLat1 = rad(lat1)
        radLat2 = rad(lat2)
        a = radLat1 - radLat2
        b = rad(lng1) - rad(lng2)
        s = 2 * math.asin(math.sqrt(math.pow(math.sin(a/2), 2) + math.cos(radLat1) * math.cos(radLat2) * math.pow(math.sin(b/2), 2)))
        s = s * EARTH_REDIUS
        s = math.sqrt(s*s+(h1-h2)*(h1-h2))
        self.Distance=s #经纬度距离，单位千米

        # 计算方位角函数
    def azimuthAngle(self):
        angle = 0.0;
        x1=self.x1
        x2=self.x2
        y1=self.y1
        y2=self.y2
        dx = x2 - x1
        dy = y2 - y1
        if  x2 == x1:
            angle = math.pi / 2.0
            if  y2 == y1 :
                angle = 0.0
            elif y2 < y1 :
                angle = 3.0 * math.pi / 2.0
        elif x2 > x1 and y2 > y1:
            angle = math.atan(dx / dy)
        elif  x2 > x1 and  y2 < y1 :
            angle = math.pi / 2 + math.atan(-dy / dx)
        elif  x2 < x1 and y2 < y1 :
            angle = math.pi + math.atan(dx / dy)
        elif  x2 < x1 and y2 > y1 :
            angle = 3.0 * math.pi / 2.0 + math.atan(dy / -dx)
        self.azimuth_Angle = (angle * 180 / math.pi)
    
    def AntennaWeight(self):              #权重参数
        w_angle =60   #定义水平半功率角
        azu=self.azu
        included_angle = abs(self.azimuth_Angle-azu)
        print("夹角",included_angle)
        if included_angle<=w_angle:                     #    接收位置位于主瓣内
            self.Antenna_weight = 2-math.cos(0.5*included_angle*math.pi/180)
        elif 3*w_angle /2>=included_angle>w_angle/2:    #    接收位置位于旁瓣内
            self.Antenna_weight = (2-math.cos(0.5*w_angle/2*math.pi/180))* \
            (2-math.cos(0.5*(included_angle-w_angle/2)*math.pi/180))
        elif included_angle > 3*w_angle/2:              #    接收位置位于背瓣内
            self.Antenna_weight = (2-math.cos(0.5*w_angle/2*math.pi/180))* \
        (2-math.cos(0.5*w_angle*math.pi/180))*(2-math.cos(0.5* \
        (included_angle-3*w_angle/2)*math.pi/180))
        else:                                           #    全向天线 
            self.Antenna_weight = 1
            
        print("权重系数",self.Antenna_weight)     
    # Okumura-Hata模型
    def rsrp(self):
        h_angle = 10   # 定义垂直半功率角
        rs_dl=0         #功率下降值
        feeder_loss=0   #馈线损耗
        Antenna_gain=0  #天线增益
        ue_h=1.5        #人体身高
        kc=0            #地貌因子
        result=0
        self.getDistance()
        self.azimuthAngle()
        self.AntennaWeight()
        apha = self.Antenna_weight
        q=self.hb/math.tan((0.5*h_angle+self.Downdip_angle)*math.pi/180)
        q=q/1000
        print(self.Distance,q)
        if self.fre > 1000:      #1800MHz频段适用于COST231Hata模型：
            a_hm=(math.log10(self.fre)*1.1-0.7)*ue_h-(1.56*math.log10(self.fre)-0.8) #天线高度修正因子
            if self.Distance < q :
                #=46.3+33.9*LOG10(B7)-13.82*LOG10(C7)-G7+(44.9-6.55*LOG10(C7))*LOG10(E7)+F7
                result= self.RsPow-apha*(46.3+33.9*math.log10(self.fre)-13.82*math.log10(self.hb) \
                                   -a_hm+(44.9-6.55*math.log10(self.hb))*math.log10(q)+kc)
            else:
                result= self.RsPow-apha*(46.3+33.9*math.log10(self.fre)-13.82*math.log10(self.hb) \
                                   -a_hm+(44.9-6.55*math.log10(self.hb))*math.log10(self.Distance)+kc)
        else:  #900MH频段适用于Hata-Okumura模型：
            if self.Distance < q :
                result= self.RsPow-rs_dl-feeder_loss-Antenna_gain- \
            (apha*(69.55+26.16*math.log10(self.fre)-13.82*math.log10(self.hb)-(3.2*(math.log10(11.75*ue_h)) \
            *(math.log10(11.75*ue_h))-4.97)*ue_h+(44.9-6.55*math.log10(self.hb))*math.log10(q)))
            else:
                result= self.RsPow-rs_dl-feeder_loss-Antenna_gain- \
            (apha*(69.55+26.16*math.log10(self.fre)-13.82*math.log10(self.hb)-(3.2*(math.log10(11.75*ue_h)) \
            *(math.log10(11.75*ue_h))-4.97)*ue_h+(44.9-6.55*math.log10(self.hb))*math.log10(self.Distance)))
        return result


class Load_data():
    def __init__(self,adr):
        self.adr=adr
        self.cell_lst=[]
        self.area_rsrp=None
        self.opt_rsrp=None
        self.azu_lst = [-40,-35,-30,-25,-20,-15,-10,-5,0,5,10,15,20,25,30,35,40]  #方位角范围
        self.title_lst = [-10,-8,-6,4,2,0,2,4,6,8,10]             #下倾角范围
        self.r=0
        self.c=0
        self.Group_pool=[]
        self.Group_ID=[]
        self.df=None
        self.df_build=None
        self.run() #初始化后执行
        
    def run(self):
        df1= pd.read_excel(adr,'Opt_Area_Cell').values  # df.values 转为数组
        df2 = pd.read_excel(adr,'Opt_Cell')
        self.cell_lst=df2["cid"]
        self.df=df2
        df3 = pd.read_excel(adr,'Building_grid').values
        self.df_build=df3
        [rows1, cols1] = df1.shape
        [rows2, cols2] = df2.shape
        [rows3, cols3] = df3.shape
        
        self.area_rsrp = np.zeros((rows3,rows1))  #优化区域栅格矩阵
        self.opt_rsrp = np.zeros((rows3,rows2))  #调整小区栅格矩阵
        
        for i in range(rows3):
            for j in range(rows1):
                    ant_rsrp=Ant(df1[j][1],df1[j][2],df1[j][3],df1[j][4],df1[j][5],df1[j][6],df1[j][7],df3[i][2],df3[i][3])
                    self.area_rsrp[i][j]=ant_rsrp.rsrp()
          
        #all_rsrp = np.hstack((area_rsrp,opt_rsrp)) #汇总矩阵后统计目标函数
        #排列组合ID
        self.r=len(self.azu_lst)**len(self.cell_lst)
        self.c=len(self.title_lst)**len(self.cell_lst)
        self.Group_ID =  np.arange(self.r*self.c).reshape(self.r, self.c)
        
        #排列组合索引表
        fn = lambda x, code=',':reduce(lambda x, y: [str(i)+code+str(j) for i in x for j in y], x)
        for i in range(len(self.cell_lst)):
            group1=fn([[self.cell_lst[i]],self.azu_lst,self.title_lst], code='_')
            if i==0:
                self.Group_pool=group1
            else:
                self.Group_pool=fn([group1,self.Group_pool], code=',')
   
    
def check_angle(x,y,n): #检查下倾角方位角是否超限
    if n==0 :
        if x+y>=360:
            return x+y-360
        elif x+y<0:
            return x+y+360
        else:
            return x+y
    if n==1:
        if x+y>12:
            return 12
        elif x+y <0:
            return 0
        else:
            return x+y
class Firefly:
    def __init__(self, x, y, brightness):
        self.x = x							  
        self.y = y							  
        self.brightness = brightness		  #亮度
        self.attractiveness = self.brightness #吸引力
        
if __name__ == '__main__':
    '''
    #Ant:    #lng	lat	 Azimuth	Downdip_angle 	height 	Fre_DL 	power
    a1=Ant(118.587801,24.831921,60,4,23,1850,18,118.587293,24.833579)
    a2=Ant(118.587801,24.831921,60,4,23,1850,18,118.588574,24.833555)
    a3=Ant(118.587801,24.831921,60,4,23,1850,18,118.589709,24.833323)
    a4=Ant(118.587801,24.831921,60,4,23,1850,18,118.590264,24.832905)
    a5=Ant(118.587801,24.831921,60,4,23,1850,18,118.590469,24.832347)
    a6=Ant(118.587801,24.831921,60,4,23,1850,18,118.590555,24.831494)
    a7=Ant(118.587801,24.831921,60,4,23,1850,18,118.590222,24.830913)
    rs=[a1.rsrp(),a2.rsrp(),a3.rsrp(),a4.rsrp(),a5.rsrp(),a6.rsrp(),a7.rsrp()]
    ah=[a1.Antenna_weight,a2.Antenna_weight,a3.Antenna_weight,a4.Antenna_weight,a5.Antenna_weight,a6.Antenna_weight,a7.Antenna_weight]
    '''
    adr=r"F:\项目资料\联通日常\201907天馈寻优\Opt_data.xlsx"
    data=Load_data(adr)
    n=data.Group_ID[0][1]
    g1=data.Group_pool[n]
    g1=g1.split(',')
    gf=pd.DataFrame(g1)
    gf['cid'],gf['azu'],gf['title']=zip(*gf[0].map(lambda x: x.split('_')))
    gf=gf[['cid','azu','title']]
    gf=gf.apply(pd.to_numeric, errors="ignore") #object转数值
    df=pd.merge(data.df,gf,on='cid')#合并两个表
    df["Azimuth"]=df.apply(lambda x: check_angle(x['Azimuth'],x['azu'],0), axis = 1)
    df["Downdip_angle"]=df.apply(lambda x: check_angle(x['Downdip_angle'],x['title'],1), axis = 1)
    df=df.values
    for i in range(data.opt_rsrp.shape[0]):
        for j in range(data.opt_rsrp.shape[1]):
            ant_rsrp=Ant(df[j][1],df[j][2],df[j][3],df[j][4],df[j][5],df[j][6],df[j][7],data.df_build[i][2],data.df_build[i][3])
            data.opt_rsrp[i][j]=ant_rsrp.rsrp()   
    all_rsrp = np.hstack((data.area_rsrp,data.opt_rsrp)) #汇总矩阵后统计目标函数
    res = np.max(all_rsrp,axis=1)
    all_rsrp[all_rsrp >-110].size  #电平大于-100个数
    data_df = pd.DataFrame(data.area_rsrp)
    writer = pd.ExcelWriter(r'F:\项目资料\联通日常\201907天馈寻优\Save_调整前.xlsx')
    data_df.to_excel(writer,'page_1',float_format='%.5f') # float_format 控制精度
    writer.save()