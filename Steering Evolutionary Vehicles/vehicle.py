import pygame
import random
from vectors import Vector
from math import sin, cos, pi, atan

screenWidth = 1000
screenHeight = 600
win = pygame.display.set_mode((screenWidth, screenHeight))

GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

edge_dist = 25
mutation_rate = 0.05
check_debug = False

class Vehicle :
    def __init__(self, dna = False) :
        self.length = 20
        self.max_speed = 2
        self.max_force = 0.05

        self.pos = Vector(random.randint(0, screenWidth), random.randint(0, screenHeight))
        self.vel = Vector(self.max_speed*random.random(), self.max_speed*random.random())
        self.acc = Vector(self.max_force*random.random(), self.max_force*random.random())
        self.color = GREEN

        self.health = 1
        self.eaten = 0

        if not dna :
            self.dna = [0]*4
            self.dna[0] = -2 + 4 * random.random()  # food weight
            self.dna[1] = -2 + 4 * random.random()  # poison weight
            self.dna[2] = random.randint(10, 150)  # food perception
            self.dna[3] = random.randint(10, 150)  # poison perception
        else :
            self.dna = dna.copy()
            
            for i in range(2) :
                if random.random() < mutation_rate :
                    self.dna[i] += -0.1 + 0.2*random.random()
                
            for i in range(2, 4) :
                if random.random() < mutation_rate :
                    self.dna[i] += random.randint(-10, 10)

    def show(self) :
        x = self.pos.x
        y = self.pos.y
        l = self.length
        vel = self.vel

        if vel.x == 0 :
            if vel.y > 0 :
                angle = pi/2
            else :
                angle = 3*pi/2
        else :
            angle = atan(vel.y / vel.x)

        if vel.x < 0 :  
            angle += pi

        x1 = x + l * cos(angle)
        y1 = y + l * sin(angle)
        x2 = x - (l/2) * cos(pi/4 - angle)
        y2 = y + (l/2) * sin(pi/4 - angle)
        x3 = x - (l/2) * cos(pi/4 + angle)
        y3 = y - (l/2) * sin(pi/4 + angle)

        x, y = int(x), int(y)
        x1, y1 = int(x1), int(y1)
        x2, y2 = int(x2), int(y2)
        x3, y3 = int(x3), int(y3)

        if check_debug :
            self.debug(x, y, angle)

        self.set_color()
        pygame.draw.polygon(win, self.color, [(x1, y1), (x2, y2), (x3, y3)])

    def debug(self, x, y, angle) :
        x1 = x + 3 * self.length * self.dna[0] * cos(angle)
        y1 = y + 3 * self.length * self.dna[0] * sin(angle)
        pygame.draw.line(win, GREEN, (x, y), (x1, y1), 3)

        x2 = x + 3 * self.length * self.dna[1] * cos(angle)
        y2 = y + 3 * self.length * self.dna[1] * sin(angle)
        pygame.draw.line(win, RED, (x, y), (x2, y2), 2)

        
        try :
            pygame.draw.circle(win, GREEN, (x, y), self.dna[2], 3)
        except :
            pass
        
        try :
            pygame.draw.circle(win, RED, (x, y), self.dna[3], 2)
        except :
            pass

    def update(self) :
        self.vel.add(self.acc)
        self.pos.add(self.vel)
        self.acc.mult(0)

        self.health -= 0.0025

    def eat(self, list, nutrition, perception) :
        
        record = 99999
        closest = None
        for i in range(len(list) - 1, -1, -1) :
            d = list[i].dist(self.pos)

            if d < 2 * self.max_speed :
                list.pop(i)
                self.eaten += 1
                self.health += nutrition
            else :
                if d < record and d < perception :
                    record = d
                    closest = list[i]

        if closest is not None :
            return self.seek(closest)

        return Vector(0, 0)

    def behaviors(self, good, bad) :
        steerG = self.eat(good, 0.3, self.dna[2])
        steerB = self.eat(bad, -0.75, self.dna[3])

        steerG.mult(self.dna[0])
        steerB.mult(self.dna[1])

        self.applyForce(steerG)
        self.applyForce(steerB)

    def seek(self, target) :
        desired = target.subtract(self.pos)

        desired.setMag(self.max_speed)

        steer = desired.subtract(self.vel)
        if steer.mag > self.max_force :
            steer.setMag(self.max_force)

        return steer

    def applyForce(self, f) :
        self.acc.add(f)

    def boundaries(self) :
        desired = None

        if self.pos.x < edge_dist :
            desired = Vector(self.max_speed, self.vel.y)
        
        elif self.pos.x > screenWidth - edge_dist :
            desired = Vector(-self.max_speed, self.vel.y)

        elif self.pos.y < edge_dist :
            desired = Vector(self.vel.x, self.max_speed)

        elif self.pos.y > screenHeight - edge_dist :
            desired = Vector(self.vel.x, -self.max_speed)

        if desired is not None :
            desired.setMag(self.max_speed)

            steer = desired.subtract(self.vel)
            steer.setMag(self.max_force)

            self.applyForce(steer)

    def set_color(self) :
        if self.health < 0 :
            self.health = 0
        elif self.health > 1 :
            self.health = 1

        self.color = (int((1 - self.health)*255), int(self.health*255), 0)

    def dead(self) :
        return self.health <= 0

    def clone(self) :
        if random.random() < 0.001 :
            return Vehicle(self.dna)
        
        return None

vehicles = []
for i in range(50) :
    v = Vehicle()
    vehicles.append(v)


food = []
for i in range(40) :
    x = random.randint(edge_dist, screenWidth - edge_dist)
    y = random.randint(edge_dist, screenHeight - edge_dist)
    food.append(Vector(x, y))

poison = []
for i in range(20) :
    x = random.randint(edge_dist, screenWidth - edge_dist)
    y = random.randint(edge_dist, screenHeight - edge_dist)
    poison.append(Vector(x, y))

run = True
play = False
while run :

    pygame.time.delay(5)

    for event in pygame.event.get() :
        if event.type == pygame.QUIT :
            run = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] :
        pygame.time.delay(100)
        check_debug = not check_debug
    if keys[pygame.K_s] :
        play = True

    if play :
        win.fill(0)

        prob = 0.5
        while len(food) < 40 and random.random() < prob :
            x = random.randint(edge_dist, screenWidth - edge_dist)
            y = random.randint(edge_dist, screenHeight - edge_dist)
            food.append(Vector(x, y))

        while len(poison) < 20 and random.random() < prob :
            x = random.randint(edge_dist, screenWidth - edge_dist)
            y = random.randint(edge_dist, screenHeight - edge_dist)
            poison.append(Vector(x, y))

        for i in range(len(food)) :
            pygame.draw.circle(win, GREEN, (food[i].x, food[i].y), 4)

        for i in range(len(poison)) :
            pygame.draw.circle(win, RED, (poison[i].x, poison[i].y), 4)

        for i in range(len(vehicles) - 1, -1, -1) :
            v = vehicles[i]

            new_vehicle = v.clone()
            if new_vehicle is not None :
                vehicles.append(new_vehicle)

            if v.dead() :
                x = v.pos.x
                y = v.pos.y

                food.append(Vector(int(x), int(y)))

                vehicles.pop(i)
                continue

            v.boundaries()
            v.behaviors(food, poison)
            v.update()
            v.show()

        pygame.display.update()
 
pygame.quit()