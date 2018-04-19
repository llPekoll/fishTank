from math import sqrt

from fish import Fish
from pygame.mixer import Sound


class Predator(Fish):
   
    def __init__(self, screen, spawn, size, color, id):
        super().__init___(screen, spawn, size, color, id)
        self.pred_id = id
        self.death_sound = Sound('chew.wav')
        self.MAX_SPEED_X = 4
        self.MAX_SPEED_Y = 4
        self.VISION = 500
        self.ZONE_OF_WALL = 5
        self.ZONE_OF_REPULSION = 100
        self.HUNGER_CONST = -10.0
        self.WALL_CONST = 2.0
        self.REPULSIVE_CONST = 40.0
        
    def __del__(self):
        self.death_sound.play()
        
    def cal_prey_forces(self, prey_list):
        force_x, force_y = 0, 0
        
        if not prey_list:
            return force_x, force_y
         
        distances = [self.distance_to(f) for f in prey_list]
        sorted_prey = sorted(zip(prey_list, distances), key=lambda x: x[1])

        for prey, dist in sorted_prey:
            if self.behind_me(prey):
                continue
            
            a = self.rect[0] - prey.rect[0]
            b = self.rect[1] - prey.rect[1]
            c = sqrt(a**2 + b**2)
            
            if c > self.VISION or c == 0:
                continue
            else:
                force_x += self.HUNGER_CONST * (a/c)
                force_y += self.HUNGER_CONST * (b/c)
                break  # after we find the closest fish
        return force_x, force_y
        
