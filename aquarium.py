import sys
from random import random

import pygame
from pygame.locals import *

import predator 



blueColor = pygame.Color(0, 0, 255)


class Aquarium:

    def __init__(self, width=800, height=600):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Fish Tank')

    def main_loop(self):
        fpsClock = pygame.time.Clock()
        
        while True:
            self.screen.fill(blueColor)

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
