from math import sqrt

from fish import Fish
from pygame.mixer import Sound


class Predator(Fish):
   
    def __init__(self, screen, spawn, size, color, id):
        super().__init___(screen, spawn, size, color, id)
        self.pred_id = id
        self.death_sound = Sound('chew.wav')
        self.MAX_SPEED = 4
        self.VISION = 500
        self.ZONE_OF_WALL = 5
        self.ZONE_OF_REPULSION = 100
        self.HUNGER_CONST = -10.0
        self.WALL_CONST = 2.0
        self.REPULSIVE_CONST = 40.0
        
    def __del__(self):
        self.death_sound.play()
        
    def calc_prey_forces(self, prey_list):
        """Calculate the force of running away from predators."""
        force_x, force_y = 0, 0
        if not prey_list:
            return force_x, force_y
        distances = [self.distance_to(f) for f in prey_list]
        sortedPrey = sorted(zip(prey_list, distances), key=lambda x: x[1])
        for fish, dist in sortedPrey:
            if self.behind_me(fish):
                continue
            dx = self.rect[0] - fish.rect[0]
            dy = self.rect[1] - fish.rect[1]
            r = sqrt(dx**2 + dy**2)
            if r > self.VISION or r == 0:
                continue
            else:
                force_x += self.HUNGER_CONST * (dx / r)
                force_y += self.HUNGER_CONST * (dy / r)
                break # after we find the closest fish
        return force_x, force_y


    def calc_predator_forces(self, predator_list):
        """Predator-Predator repulsion."""
        force_x, force_y = 0, 0
        if not predator_list:
            return force_x, force_y
        for fish in predator_list:
            if self.behind_me(fish):
                continue
            dx = self.rect[0] - fish.rect[0]
            dy = self.rect[1] - fish.rect[1]
            r = sqrt(dx**2 + dy**2)
            if r > self.ZONE_OF_REPULSION:
                continue
            if r == 0:
                force_x += (self.REPULSIVE_CONST / 1.) * (dx / 1.)
                force_y += (self.REPULSIVE_CONST / 1.) * (dy / 1.)    
            else:
                force_x += (self.REPULSIVE_CONST / r) * (dx / r)
                force_y += (self.REPULSIVE_CONST / r) * (dy / r)
        return force_x, force_y  

    def calc_wall_forces(self, w, h):
        """Calculate the inward force of a wall, which is very short range. Either 0 or CONST."""
        force_x, force_y = 0, 0
        if self.rect[0] < self.ZONE_OF_WALL:
            force_x += self.WALL_CONST
        elif self.rect[0]+self.rect[2] > (w - self.ZONE_OF_WALL):
            force_x -= self.WALL_CONST
        if self.rect[1] < self.ZONE_OF_WALL:
            force_y += self.WALL_CONST
        elif self.rect[1]+self.rect[3] > (h - self.ZONE_OF_WALL):
            force_y -= self.WALL_CONST
        return force_x, force_y

    def update_velocity(self, prey_list, predator_list, w, h):

        preyForces = self.calc_prey_forces(prey_list)

        # Check neighboring predators
        predator_list.remove(self)
        predatorForces = self.calc_predator_forces(predator_list)

        # Check the walls.
        wallForces = self.calc_wall_forces(w, h)

        # Calculate final speed for this step.
        allForces = [preyForces, wallForces, predatorForces]
        for force in allForces:
            self.vel[0] += force[0]
            self.vel[1] += force[1]

        # Ensure fish doesn't swim too fast.
        if self.vel[0] >= 0:
            self.vel[0] = min(self.MAX_SPEED, self.vel[0])
        else:
            self.vel[0] = max(-self.MAX_SPEED, self.vel[0])
        if self.vel[1] >= 0:
            self.vel[1] = min(self.MAX_SPEED, self.vel[1])
        else:
            self.vel[1] = max(-self.MAX_SPEED, self.vel[1])
        

    def swim(self, w, h):
        """Using my xVel and yVel values, take a step, so long as we don't swim out of bounds."""
        # Keep fish in the window
        if self.rect[0]+self.vel[0] <= 0 or self.rect[0]+self.vel[0] >= w:
            dx = 0
        else:
            dx = self.vel[0]
        if self.rect[1]+self.vel[1] <= 0 or self.rect[1]+self.vel[1] >= h:
            dy = 0
        else:
            dy = self.vel[1]

        self.rect.move_ip(dx, dy)

  