from math import pi, sqrt, cos, sin, atan2
from random import random

import pygame
from pygame import Color, Surface
from pygame.sprite import collide_circle, Sprite
from pygame.draw import line
# from pygame.locals import *


class Fish(Sprite):
    """
        Fish class
    """

    def __init___(self, rect=None, color=None):
        Sprite.__init__(self)
        self.count = 0
        self.count += 1  # we might want to move the counter un some other call
        self.fish_ID = self.count

        self.color = color if not self.color else Color(255, 0, 0)

        if rect:
            self.image = Surface([rect[2], rect[3]])
            self.image.fill(self.color)
            self.rect = rect
        else:
            self.image .Surface([20, 20])
            self.image.fill(self.color)
            self.rect = self.image.get_rect()

        self.deathSound = pygame.mixer.Sound('chew.wav')
        self.blindFOV = 0.5
        self.blindLeft = pi - self.blindFOV/2.
        self.blindRight = pi + self.blindFOV/2.
        initialDirection = random()*2.0*pi
        self.MAX_SPEED_X = 6.0
        self.MAX_SPEED_Y = 6.0
        self.xVel = self.MAX_SPEED_X*cos(initialDirection)
        self.yVel = self.MAX_SPEED_Y*sin(initialDirection)

    def __del__(self):
        if self.deathSound:
            self.deathSound.play()

    def draw_direction_line(self):
        """Given a fish sprite, draw a line of motion using xVel and yVel."""
        startX = self.rect[0]
        startY = self.rect[1]
        endX = (self.rect[0] + 2*self.xVel)
        endY = (self.rect[1] + 2*self.yVel)
        line(self.screen, Color(255, 0, 0), (startX, startY), (endX, endY), 3)

    def fish_collision(sprite1, sprite2):
        """
            Collision Detection.
        """
        
        return False if sprite1 == sprite2 else collide_circle(sprite1, sprite2)  # nota :E501 

    def orientation_from_components(dx, dy):
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
        return self.orientation_from_components(self.xVel, self.yVel)

    def behind_me(self, otherFish):
        """
            Return True if another fish is behind this fish. 
            Uses xVel, yVel and position.
        """
        theta1 = self.calc_orientation()
        theta2 = self.direction_to(otherFish)
        return abs(theta1-theta2) > self.blindLeft and abs(theta1-theta2) < self.blindRight

    def distance_to(self, otherFish):
        """
            Calculate the distance to another fish.
        """
        myX, myY = self.rect[0], self.rect[1]
        otherX, otherY = otherFish.rect[0], otherFish.rect[1]
        return sqrt((myX-otherX)**2 + (myY-otherY)**2)
