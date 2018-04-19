from math import pi, sqrt, cos, sin, atan2
from random import random

import pygame
from pygame import Color, Surface
from pygame.sprite import collide_circle, Sprite
from pygame.draw import line, rect
# from pygame.locals import *


class Fish(Sprite):
  
    def __init___(self, spawn, size, color, id):
        Sprite.__init__(self)
      
        self.image = pygame.Surface(size)
        self.image.fill(color)
        self.rect = self.image.get_rect()

    #    self.death_sound = pygame.mixer.Sound('chew.wav')
        self.blindFOV = 0.5
        self.blindLeft = pi - self.blindFOV/2.
        self.blindRight = pi + self.blindFOV/2.
        initialDirection = random()*2.0*pi

        self.MAX_SPEED = 6
        self.vel = [1,2]
        self.vel[0] = self.MAX_SPEED*cos(initialDirection)
        self.vel[1] = self.MAX_SPEED*sin(initialDirection)
        self.load_sprites(spawn, size, color)

    # def __del__(self):
    #    self.death_sound.play()

    def load_sprites(self, spawn, size, color):
        pygame.Rect(spawn, size, color=color)

    def draw_direction_line(self):
        """Given a fish sprite, draw a line of motion using xVel and yVel."""
        endX = (self.rect[0] + 2*self.Vel[0])
        endY = (self.rect[1] + 2*self.Vel[1])
        screen = pygame.display.get_surface()
        line(screen, Color(255, 0, 0),
             (self.rect[0], self.rect[1]), (endX, endY), 3)

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
