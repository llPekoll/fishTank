from math import sqrt
from fish import Fish


class Prey(Fish):
    """
        Fish (prey)
    """
    def __init__(self, screen, spawn, size, color, id):
        super().__init___(screen, spawn, size, color, id)
        self.prey_ID = id
        self.xVel = 0
        self.yVel = 0
        self.color = color
        self.MAX_SPEED = 9 

        self.ZONE_OF_REPULSION = 50
        self.ZONE_OF_ALIGNMENT = 100
        self.ZONE_OF_ATTRACTION = 400
        self.ZONE_OF_WALL = 30
        self.ZONE_OF_FEAR = 80

        self.ATTRACTIVE_CONST = -11.0
        self.REPULSIVE_CONST = 12.0
        self.ALIGNMENT_CONST = 0.5
        self.WALL_CONST = 2.0
        self.FEAR_CONST = 4.0
       
    def get_flee_predator_force(self, predator_list):
        """
            flee from predator speed
        """
        force_x, force_y = 0, 0
        if not predator_list:
            return force_x, force_y
        
        for predator in predator_list:
            if self.behind_me(predator):
                continue
            a = self.rect[0] - predator.rect[0]
            b = self.rect[1] - predator.rect[1]
            c = sqrt(a**2 + b**2)
            if c > self.ZONE_OF_FEAR or c == 0:
                continue
            force_x += self.FEAR_CONST * (a/c)
            force_y += self.FEAR_CONST * (b/c)
        
        return force_x, force_y
    
    def get_flock_force(self, prey_list):
        """
            calculate the force of attration betwenn other fishes
        """
        force_x, force_y = 0, 0
        if not prey_list:
            return force_x, force_y
        for prey in prey_list:
            if prey.color != self.color:
                continue
            if self.behind_me(prey):
                continue
            a = self.rect[0] - prey.rect[0]
            b = self.rect[1] - prey.rect[1]
            c = sqrt(a**2 + b**2)
            if c> self.ZONE_OF_ATTRACTION or c <= self.ZONE_OF_REPULSION:
                continue
            force_x += (self.ATTRACTIVE_CONST / c) * (a / c)
            force_y += (self.ATTRACTIVE_CONST / c) * (b / c)
        return force_x, force_y

    def get_repulsive_forces(self, prey_list):
        """
            Calculate the repulsive force due to close by fish.
        """
        force_x, force_y = 0, 0
        if not prey_list:
            return force_x, force_y
        for fish in prey_list:
            if self.behind_me(fish):
                continue
            a = self.rect[0] - fish.rect[0]
            b = self.rect[1] - fish.rect[1]
            c = sqrt(a**2 + b**2)
            if c == 0 or c > self.ZONE_OF_REPULSION:
                continue
            force_x += (self.REPULSIVE_CONST / c) * (a / c)
            force_y += (self.REPULSIVE_CONST / c) * (b / c)
        return force_x, force_y        
     
    def get_alignment_forces(self, prey_list):
        """Calculate the alignment force due to other close fish. Fish like to
        swim in the same direction as other fish. Return the force in (x,y) directions."""
        force_x, force_y = 0, 0
        if not prey_list:
            return force_x, force_y
        for fish in prey_list:
            if fish.color != self.color:
                continue
            if self.behind_me(fish):
                continue
            dx = self.rect[0] - fish.rect[0]
            dy = self.rect[1] - fish.rect[1]
            r = sqrt(dx**2 + dy**2)
            if r < self.ZONE_OF_REPULSION or r > self.ZONE_OF_ALIGNMENT:
                continue
            force_x += fish.xVel * (self.ALIGNMENT_CONST / r)
            force_y += fish.yVel * (self.ALIGNMENT_CONST / r)
        return force_x, force_y                

    def calc_wall_forces(self, width, height):
        """Calculate the inward force of a wall, which is very short range. Either 0 or CONST."""
        force_x, force_y = 0, 0
        if self.rect[0] < self.ZONE_OF_WALL:
            force_x += self.WALL_CONST
        elif (self.rect[0]+self.rect[2]) > (width-self.ZONE_OF_WALL):
            force_x -= self.WALL_CONST
        if self.rect[1] < self.ZONE_OF_WALL:
            force_y += self.WALL_CONST
        elif (self.rect[1]+self.rect[3]) > (height-self.ZONE_OF_WALL):
            force_y -= self.WALL_CONST
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

