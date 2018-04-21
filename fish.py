from math import pi, sqrt, cos, sin, atan2
from random import random

import pygame
from pygame import Color, Surface
from pygame.sprite import collide_circle, Sprite
from pygame.draw import line, rect
# from pygame.locals import *
import physics

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
        
    def draw_fish(self, screen, spawn, size, color):
        self.rect = rect(screen, (90, 2, 90), (spawn, size))
        self.draw_direction_line(screen)

    def draw_direction_line(self,screen):
        endX = (self.rect[0] + 4 * self.vel[0])
        endY = (self.rect[1] + 4 * self.vel[1])
        ret = line(screen, Color(0, 0, 0),
             (self.rect[0], self.rect[1]), (endX, endY))
        
    def calc_orientation(self):
        """
            Based on xVel, yVel, which way am I facing? 
        """
        
        return physics.orientation_from_components(self.vel[0], self.vel[1])

    def behind_me(self, otherFish):
        """
            Return True if another fish is behind this fish. 
            Uses xVel, yVel and position.
        """
        theta1 = self.calc_orientation()
        theta2 = self.direction_to(otherFish)
        return abs(theta1-theta2) > self.blindLeft and abs(theta1-theta2) < self.blindRight

    def direction_to(self, otherFish):
        """
            Use the two coordinates to determine direction to other fish.
        """
        dx = otherFish.rect[0] - self.rect[0]
        dy = otherFish.rect[1] - self.rect[1]
        return physics.orientation_from_components(dx, dy)

    def distance_to(self, otherFish):
        """
            Calculate the distance to another fish.
        """
        myX, myY = self.rect[0], self.rect[1]
        otherX, otherY = otherFish.rect[0], otherFish.rect[1]
        return sqrt((myX-otherX)**2 + (myY-otherY)**2)

    def swim(self, w, h):
        """
            Using my xVel and yVel values, take a step, so long as we don't swim out of bounds.
        """

        # Keep fish in the window
        dx = 0 if (self.rect[0]+self.vel[0] <
                   0 or self.rect[0]+self.vel[0] > w) else self.vel[0]
        dy = 0 if (self.rect[1]+self.vel[1] <
                   0 or self.rect[1]+self.vel[1] > h) else self.vel[1]

        self.rect.move_ip(dx, dy)
