import pygame, sys
import math
import random
import time
from pygame.locals import*

pygame.init()
screen = pygame.display.set_mode((1200,800),0,32)
ffList = []

class Firefly:

    def __init__(self, x, y, brightness): 
        self.x = x
        self.y = y
        self.brightness = brightness  #brightness 亮度
        self.r = int(math.sqrt((self.brightness)/math.pi))  #个人理解为吸引度
        if self.r < 1:
            self.r = 1  

    def DrawOnScreen(self):
        pygame.draw.circle(screen, pygame.Color(131, 245, 44,255), (self.x, self.y), self.r, 0)

    def Calculations(self):
        deltaX = 0
        deltaY = 0
        for f in ffList:
            if f != self:                                                  #萤火虫“f”不能吸引到“g”（自身）
                vectorX = (f.x - self.x)
                vectorY = (f.y - self.y)
                currentLen = math.sqrt(vectorX**2 + vectorY**2)         #2只萤火虫之间的欧氏距离

                if currentLen > 50:                                     #如果萤火虫的距离超过50像素，它们就会互相吸引
                    relBrightness = (f.brightness/currentLen)           #萤火虫的相对亮度与当前距离成反比。
                    vectorX = vectorX/currentLen                        #规范化X矢量
                    vectorY = vectorY/currentLen                        #规范化Y矢量
                    deltaX += relBrightness * vectorX
                    deltaY += relBrightness * vectorY
                else:                                                   #如果萤火虫的距离在1到50像素之间，它们会互相排斥。
                    deltaX = random.randrange(-3,4)
                    deltaY = random.randrange(-3,4)

        #如果从其他萤火虫那里没有足够的拉力，就会产生随机移动。
        if abs(deltaX) < 5 and abs(deltaY) < 5:
            self.x += random.randrange(-4,5)
            self.y += random.randrange(-4,5)
        #如果从其他萤火虫那里有足够的拉力，给运动增加噪音。
        else:
            self.x += int(deltaX) + random.randrange(-1,2)
            self.y += int(deltaY) + random.randrange(-1,2)
        
        #在这里处理边界，这样萤火虫就不能离开窗户了。
        if self.x > 1200:
            self.x = 1200
        if self.x < 0:
            self.x = 0
        if self.y > 800:
            self.y = 800
        if self.y < 0:
            self.y = 0

class Mouse:
    def __init__(self):
        (self.x, self.y) = pygame.mouse.get_pos()
        self.brightness = 600
        self.r = int(math.sqrt((self.brightness)/math.pi))
        if self.r < 1:
            self.r = 1

    def DrawOnScreen(self):
        pygame.draw.circle(screen, pygame.Color(255,255,255,255), (self.x, self.y), self.r, 0)

for i in range(150):                                                    #这个循环产生萤火虫
    x = int(random.randrange(0,1200))                                   #随机x坐标
    y = int(random.randrange(0,800))                                    #随机y坐标
    brightness = random.randrange(1,65)
    ffList.append(Firefly(x,y, brightness))
ffList.append(Mouse())

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    
    screen.fill(pygame.Color(0,0,0,255))
    for g in ffList:
        if not isinstance(g, Mouse):
            g.Calculations()
            g.DrawOnScreen()
        else:
            (g.x, g.y) = pygame.mouse.get_pos()
            g.DrawOnScreen()

    pygame.display.update()