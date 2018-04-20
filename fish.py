from math import pi, sqrt, cos, sin, atan2
from random import random

import pygame
from pygame import Color, Surface
from pygame.sprite import collide_circle, Sprite
from pygame.draw import line, rect
# from pygame.locals import *


class Fish(Sprite):

    def __init___(self, screen, spawn, size, color, id):
        Sprite.__init__(self)

        self.image = pygame.Surface(size)
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.blindFOV = 0.5
        self.blindLeft = pi - self.blindFOV/2.
        self.blindRight = pi + self.blindFOV/2.
        initialDirection = random() * 2 * pi

        self.MAX_SPEED = 6
        self.vel = [1, 2]
        self.vel[0] = self.MAX_SPEED*cos(initialDirection)
        self.vel[1] = self.MAX_SPEED*sin(initialDirection)
       
        self.draw_fish(screen, spawn, size, color)
        self.draw_direction_line()

    def draw_fish(self, screen, spawn, size, color):
        rect(screen, (90, 2, 90), (spawn, size))

    def draw_direction_line(self):
        endX = (self.rect[0] + 2 * self.vel[0])
        endY = (self.rect[1] + 2 * self.vel[1])
        screen = pygame.display.get_surface()
        line(screen, Color(255, 0, 0),
             (self.rect[0], self.rect[1]), (endX, endY), 3)

    def fish_collision(self, sprite1, sprite2):
        """
            Collision Detection.
        """
        return False if sprite1 == sprite2 else collide_circle(sprite1, sprite2)  # nota :E501

    def orientation_from_components(self, dx, dy):
        """
            return oriantation's angle.
        """
        if float(dx) == 0:
            orientation = pi / 2 if (float(dy) >= 0) else 3*pi / 2
        else:
            orientation = atan2(float(dy), float(dx))
        return orientation

    def calc_orientation(self):
        """
            Based on xVel, yVel, which way am I facing? 
        """
        return self.orientation_from_components(self.vel[0], self.vel[1])

    def behind_me(self, otherFish):
        """
            Return True if another fish is behind this fish. 
            Uses xVel, yVel and position.
        """
        theta1 = self.calc_orientation()
        theta2 = self.direction_to(otherFish)
        return abs(theta1-theta2) > self.blindLeft and abs(theta1-theta2) < self.blindRight
    
    def direction_to(self, otherFish):
        """Use the two coordinates to determine direction to other fish."""
        dx = otherFish.rect[0] - self.rect[0]
        dy = otherFish.rect[1] - self.rect[1]
        return self.orientation_from_components(dx, dy)
    
    def distance_to(self, otherFish):
        """
            Calculate the distance to another fish.
        """
        myX, myY = self.rect[0], self.rect[1]
        otherX, otherY = otherFish.rect[0], otherFish.rect[1]
        return sqrt((myX-otherX)**2 + (myY-otherY)**2)
    
    def swim(self, aquarium):
        """Using my xVel and yVel values, take a step, so long as we don't swim out of bounds."""
        # Keep fish in the window
        if self.rect[0]+self.vel[0] <= 0 or self.rect[0]+self.vel[0] >= aquarium.width:
            dx = 0
        else:
            dx = self.vel[0]
        if self.rect[1]+self.vel[1] <= 0 or self.rect[1]+self.vel[1] >= aquarium.height:
            dy = 0
        else:
            dy = self.vel[1]

        self.rect.move_ip(dx, dy)
