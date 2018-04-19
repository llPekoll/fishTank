import sys
from random import random

import pygame
from pygame.locals import *

from predator import Predator as pred
from prey import Prey 


class Aquarium:

    def __init__(self, width=800, height=600):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Fish Tank')
        self.PREY_NUMBER = 13
        self.PREDATOR_NB = 1
        self.blue = pygame.Color(0, 0, 255)
        self.green = pygame.Color(0, 255, 0)
        self.red = pygame.Color(255, 0, 0)

    def populate_fish_tank(self):
        
        self.predator_group = pygame.sprite.Group()
        for i in range(self.PREDATOR_NB):
            rect_pos = [random()*self.width, random()*self.height]
            rect_size = [30, 30]
            self.predator_group.add(pred(rect_pos, rect_size,  self.green, i))
           
    def main_loop(self):
        
        fpsClock = pygame.time.Clock()

        self.populate_fish_tank()
        
        while True:
            self.screen.fill()

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.event.post(pygame.event.Event(QUIT)) # Create an event


        pygame.display.update()
        fpsClock.tick(60)

        


def main():
    aquarium = Aquarium()
    aquarium.main_loop()


if __name__ == "__main__":
    main()
