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

    def update_velocity(self, aquarium):
        """Update the fishes velocity based on forces from other fish."""
        # Stay near other fish, but not too close, and swim in same direction.
        prey_list = aquarium.prey_group.sprites()
        prey_list.remove(self)
        attractiveForces = self.get_flock_force(prey_list)
        repulsiveForces = self.get_repulsive_forces(prey_list)
        alignmentForces = self.get_alignment_forces(prey_list)

        # If a predator is within 20 pixels, run away
        predator_list = aquarium.predator_group.sprites()
        predatorForces = self.get_flee_predator_force(predator_list)

        # Check the walls.
        wallForces = self.calc_wall_forces(aquarium.width, aquarium.height)

        # get final speed for this step.
        allForces = [repulsiveForces, attractiveForces, alignmentForces, wallForces, predatorForces]
        for force in allForces:
            self.xVel += force[0]
            self.yVel += force[1]

        # Ensure fish doesn't swim too fast.
        if self.xVel >= 0:
            self.xVel = min(self.MAX_SPEED, self.xVel)
        else:
            self.xVel = max(-self.MAX_SPEED, self.xVel)
        if self.yVel >= 0:
            self.yVel = min(self.MAX_SPEED, self.yVel)
        else:
            self.yVel = max(-self.MAX_SPEED, self.yVel)
