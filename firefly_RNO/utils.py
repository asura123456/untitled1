import math
import target_fun
dat=target_fun.Data() #初始化数据
target_fun.run(dat)     #导入数据
    
def distance(firefly, other_firefly):
    return math.sqrt((other_firefly.x - firefly.x) ** 2 + (other_firefly.y - firefly.y) ** 2)

def Ackley_global_minimum(firefly):
    firefly.x=int(firefly.x)
    firefly.y=int(firefly.y)

    return round(target_fun.objective_fun(dat,firefly),4)
     
def Ackley_global_maximum(firefly):
    result = abs(firefly.x) + abs(firefly.y)
    result *= math.exp(-(firefly.x ** 2 + firefly.y ** 2))
    return result

def Michalewicz(firefly):
    return  -(math.sin(firefly.x) * math.sin((firefly.x**2)/math.pi)**20) + -(math.sin(firefly.y) * math.sin((2 * firefly.y**2)/math.pi)**20)

def description(fireflies):
    fireflies = sorted(fireflies, key=lambda x:(-x.brightness)) #按brightness降序
    for i, firefly in enumerate(fireflies):
        k=target_fun.get_group(dat,firefly)
        print(i, "x:", firefly.x, "y:", firefly.y, "brightness:", firefly.brightness,"   Group",k)

def index_of_alpha(fireflies):
    alpha = fireflies[0]
    for firefly in fireflies:
        if firefly.brightness > alpha.brightness:
            alpha = firefly
    return fireflies.index(alpha)