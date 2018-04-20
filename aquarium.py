import sys
from random import random

import pygame
from pygame.locals import *

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


        self.PREY_NB = 13
        self.PREDATOR_NB = 1
        self.blue = pygame.Color(0, 0, 255)
        self.green = pygame.Color(0, 255, 0)
        self.red = pygame.Color(255, 0, 0)

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

       
        while True:

            event = pygame.event.poll()
            if event.type == pygame.QUIT:
                break

            self.screen.fill((0, 0, 255))
            self.predator_group.draw(self.screen)
            self.prey_group.draw(self.screen)

            for predator in self.predator_group.sprites():
                predator.update_velocity(aquarium=self)
            for prey in self.prey_group.sprites():
                prey.update_velocity(aquarium=self)

            # Move fish                
            for predator in self.predator_group.sprites():
                predator.swim(aquarium=self)                
            for prey in self.prey_group.sprites():
                prey.swim(aquarium=self)

            # Draw direction arrows
            for predator in self.predator_group.sprites():
                self.draw_direction_line(predator)
            for fish in self.prey_group.sprites():
                self.draw_direction_line(fish)

            # Check for all colisions among predators and fish
            # spriteHitList = pygame.sprite.groupcollide(self.predator_group, self.prey_group, False, True, collided=fish.fish_collision)


            fps = self.font.render(
                str(int(self.clock.get_fps())), True, pygame.Color('white'))
            self.screen.blit(fps, (50, 50))
            self.populate_fish_tank()
       
            pygame.display.flip()
       
            self.clock.tick(60)


def main():
    aquarium = Aquarium()
    aquarium.main_loop()


if __name__ == "__main__":
    main()
