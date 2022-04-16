import math

import pygame as pg
from pygame.math import Vector2

import config
from config import *


class Dog(pg.sprite.Sprite):

    def __init__(self, pos):
        super(Dog, self).__init__()
        self.image = pg.Surface((50, 30), pg.SRCALPHA)
        pg.draw.polygon(self.image, (50, 120, 180), ((0, 0), (0, 30), (50, 15)))
        self.original_image = self.image
        self.rect = self.image.get_rect(center=pos)
        self.position = Vector2(pos)
        self.angle = 0
        self.direction = Vector2(1, 0)  # A unit vector pointing rightward
        self.speed = 0.0
        self.angle_speed = 0
        self.herding_range = 50
        self.circulation_direction = 0

    def move(self):
        v = self.position + self.direction * self.speed
        l = point_distance(FENCE_CENTER, v)

        if l + 5 < FENCE_RADIUS:
            self.position = v
            if l + 7 < FENCE_RADIUS or self.speed == 0:
                self.circulation_direction = 0
        else:
            if self.circulation_direction == 0:
                p = self.position
                while FENCE_RADIUS <= 5 + point_distance(FENCE_CENTER,p):
                    p += self.direction
                p = Vector2(p.x - FENCE_CENTER.x, p.y - FENCE_CENTER.y)
                p.normalize_ip()
                angle = self.direction.angle_to(p)
                if angle > 90:
                    angle -= 360
                if angle < -90:
                    angle += 360

                if angle > 0:
                    self.circulation_direction = -1
                else:
                    self.circulation_direction = 1

            self.angle_speed = self.circulation_direction
            self.update()
            self.angle_speed = 0

    def update(self):
        if self.angle_speed != 0:
            # Rotate the direction vector and then the image.
            self.direction.rotate_ip(self.angle_speed)
            self.angle += self.angle_speed
            self.image = pg.transform.rotate(self.original_image, -self.angle)
            self.rect = self.image.get_rect(center=self.rect.center)
        # Update the position vector and the rect.
        self.move()
        self.rect.center = self.position

class DogCollection():
    def __init__(self, pos):
        self.position = pos
        self.dogs = []
        self.create_new_gen()

    def create_new_gen(self):
        self.dogs = []
        for i in range(0, GEN_SIZE):
            self.dogs.append(Dog(self.position))

    def evolve_population(self):
        self.dogs.sort(key=lambda x: x.fitness, reverse=True)

        for d in self.dogs:
            print('fitness:', d.fitness)

        self.create_new_gen()

