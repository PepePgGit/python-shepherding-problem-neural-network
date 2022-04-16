import pygame as pg
from pygame.math import Vector2
import random as rand
import math

import config


class Sheep():

    def __init__(self, screen, x, y, list):
        self.position = Vector2(x, y)
        self.speed = 0.0
        self.screen = screen
        self.angle = rand.random() * math.pi * 2 * 0
        self.direction = Vector2(1, 0)
        self.list_of_sheeps = list
        self.done = False

    def draw(self):
        pg.draw.circle(self.screen, (255, 255, 255), self.position, 10)
        pg.draw.circle(self.screen, (0, 0, 0), self.position + self.direction * 5, 2)

    def move(self):
        b = True
        v = self.position + self.direction * self.speed
        l = math.sqrt(math.pow(config.FENCE_CENTER[0] - v[0], 2) + math.pow(config.FENCE_CENTER[1] - v[1], 2))
        for s in self.list_of_sheeps:  # hitboxes with other sheeps
            if s != self:
                if 10 > math.sqrt(math.pow(s.position[0] - v[0], 2) + math.pow(s.position[1] - v[1], 2)):
                    b = False
                    break
        if b:
            x1 = config.TUNNEL_POINT.x
            y1 = config.TUNNEL_POINT.y
            x2 = x1 + config.TUNNEL_SIZE.x
            y2 = y1 + config.TUNNEL_SIZE.y
            x3 = config.DESTINATION_POINT.x
            y3 = config.DESTINATION_POINT.y
            x4 = x3 + config.DESTINATION_SIZE.x
            y4 = y3 + config.DESTINATION_SIZE.y
            if l + 10 < config.FENCE_RADIUS:
                self.position = v
                if self.done:
                    self.done = False
                    config.SCORE -= 10
            if (x1 < v.x < x2 and y1 < v.y < y2) or (x3 < v.x < x4 and y3 < v.y < y4):
                if not self.done:
                    self.done = True
                    config.SCORE += 10
                self.position = v

    def running(self, dog):  # running away from dogs
        self.speed = 2
        self.move()
        self.speed = 0
        v = Vector2(self.position[0] - dog.position[0],
                    self.position[1] - dog.position[1])  # v to direction przeciwny pozcji owcy do wilka
        v /= math.sqrt(math.pow(v[0], 2) + math.pow(v[1], 2))  # czyli direction jaki powinna miec owca
        if not (v[0] - 0.1 < self.direction[0] < v[0] + 0.1 and v[1] - 0.1 < self.direction[1] < v[
            1] + 0.1):  # czek if sheep dir=v (more or less)
            if self.direction.angle_to(v) > 0:  # if not turn
                self.angle += math.radians(15)
            else:
                self.angle -= math.radians(15)
            self.direction[0] = math.cos(self.angle)
            self.direction[1] = math.sin(self.angle)

    def turn(self):
        self.angle += math.radians(4) * rand.choice([-1, 1])  # turn 4 degrees
        self.direction[0] = math.cos(self.angle)
        self.direction[1] = math.sin(self.angle)

    def moving(self, dog):  # sheep action
        if not config.point_distance(dog.position, self.position) < dog.herding_range:
            if rand.random() < 0.2:
                self.speed = 0.0
                self.move()
            else:
                self.speed = 0
        else:
            self.running(dog)


class SheepCollection():

    def __init__(self, screen):
        self.sheeps = []
        self.screen = screen
        self.x = 0
        self.y = 0

    def get_sheep_new_list(self, size):
        sheeps = []
        t = 2 * math.pi * rand.random()
        u = rand.random() + rand.random()
        if u > 1:
            r = 2 - u
        else:
            r = u
        self.x = config.FENCE_CENTER[0] + (r * math.cos(t)) * (config.FENCE_RADIUS - 10)
        self.y = config.FENCE_CENTER[1] + (r * math.sin(t)) * (config.FENCE_RADIUS - 10)
        for i in range(size):
            sheeps.append(Sheep(self.screen, self.x, self.y, []))

        return sheeps

    def get_sheep_copy_list(self, size):
        sheeps = []
        for i in range(size):
            sheeps.append(Sheep(self.screen, self.x, self.y, []))
        return sheeps
