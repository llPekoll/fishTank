import sys
from random import random

import pygame
from pygame.locals import *
import physics

from predator import Predator as pred
from prey import Prey


class Aquarium:

    def __init__(self, width=1900, height=1080):

        pygame.init()
        self.font = pygame.font.Font(None, 30)
        self.clock = pygame.time.Clock()

        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Fish Tank')

        self.predator_group = pygame.sprite.Group()
        self.prey_group = pygame.sprite.Group()


        self.PREY_NB = 25
        self.PREDATOR_NB = 2
        self.blue = (0, 0, 255)
        self.green =(0, 255, 0)
        self.red = (255, 0, 0)
        self.white = (255, 255, 255)

    def populate_fish_tank(self):

        self.predator_group = pygame.sprite.Group()
        self.prey_group = pygame.sprite.Group()

        for i in range(self.PREDATOR_NB):
            rect_pos = [random()*self.width, random()*self.height]
            rect_size = [30, 30]
            self.predator_group.add(
                pred(self.screen, rect_pos, rect_size,  self.green, i))

        for i in range(self.PREY_NB):
            rect_pos = [random()*self.width, random()*self.height]
            rect_size = [10, 10]
            self.prey_group.add(
                Prey(self.screen, rect_pos, rect_size,  self.red, i))

    def main_loop(self):

        self.populate_fish_tank()
       
        while True:

            self.screen.fill((0, 0, 255))
            self.predator_group.draw(self.screen)
            self.prey_group.draw(self.screen)
         
            for predator in self.predator_group.sprites():
                predator.update_velocity(self.prey_group, self.predator_group, self.width, self.height)
            for prey in self.prey_group.sprites():
                prey.update_velocity(self.prey_group, self.predator_group, self.width, self.height)

            # Move fish                
            for predator in self.predator_group.sprites():
                predator.draw_direction_line(self.screen)
                predator.swim(self.width,self.height)                
            for prey in self.prey_group.sprites():
                prey.draw_direction_line(self.screen)
                prey.swim(self.width,self.height)

            # Check for all colisions among predators and fish
            spriteHitList = pygame.sprite.groupcollide(self.predator_group, self.prey_group, False, True, collided=physics.fish_collision)


            fps = self.font.render(
                str(int(self.clock.get_fps())) + " fps", True, pygame.Color('white'))
            self.screen.blit(fps, (50, 50))
            
            pygame.display.flip()
       
            self.clock.tick(60)


def main():
    aquarium = Aquarium()
    aquarium.main_loop()

if __name__ == "__main__":
    main()
