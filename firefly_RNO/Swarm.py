import random
from Firefly import Firefly
import config
import utils

class Swarm:
    def __init__(self, alpha, absorption):
        self.alpha = alpha
        self.absorption = absorption
        self.fireflies = []
        self.most_attractive = []
        self.minX = config.MIN_X
        self.maxX = config.MAX_X
        self.minY = config.MIN_Y
        self.maxY = config.MAX_Y
        self.width = self.maxX - self.minX
        self.height = self.maxY - self.minY
        self.fireflies_generator(config.POPULATION)

    def move(self, firefly, other_firefly):
        fraction = 2
        delta_x = (other_firefly.x - firefly.x) / fraction
        delta_y = (other_firefly.y - firefly.y) / fraction
        firefly.x += delta_x
        firefly.y += delta_y

        
    def move_randomly(self, firefly):
        new_x_direction = random.randrange(self.minX, self.maxX)
        new_y_direction = random.randrange(self.minY, self.maxY)
        delta_x = new_x_direction - firefly.x
        delta_y = new_y_direction - firefly.y
        firefly.x += delta_x / self.width
        firefly.y += delta_y / self.height


    def get_attractiveness(self, firefly, other_firefly):
        distance = utils.distance(firefly, other_firefly)
        if distance == 0:
            return other_firefly.brightness
        else:
            return other_firefly.brightness / (self.absorption * distance)

    def update_attractiveness(self):
        self.most_attractive = []
        for firefly in self.fireflies:
            attractiveness_best = 0
            most_attractive = firefly
            for other_firefly in self.fireflies:
                if firefly is not other_firefly and firefly.brightness < other_firefly.brightness:
                    attractiveness = self.get_attractiveness(firefly, other_firefly)
                    if attractiveness_best < attractiveness:
                        attractiveness_best = attractiveness
                        most_attractive = other_firefly
            self.most_attractive.append(most_attractive)

    def fireflies_generator(self, population):
        for i in range(population):
            x = random.randrange(self.minX, self.maxX, 1)
            y = random.randrange(self.minY, self.maxY, 1)
            brightness = 0
            self.fireflies.append(Firefly(x, y, brightness))

    def __str__(self):
        #tmp_area = [['..' for _ in range(self.width)] for _ in range(self.height)]

        for i, firefly in enumerate(self.fireflies):
            if self.minX < 0:
                x = firefly.x + self.width / 2
            else:
                x = firefly.x
            if self.minY < 0:
                y = firefly.y + self.height / 2
            else:
                y= firefly.y
            if x > self.width or x < 0 or y < 0 or y > self.height:
                print("Firefly", i, "is out", firefly.x, firefly.y)
            #tmp_area[int(y)][int(x)] = str(i)
        #for ar in tmp_area:
            #print(ar)