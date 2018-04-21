from math import pi, atan2

from pygame.sprite import collide_circle


def fish_collision(sprite1, sprite2):
    return False if sprite1 is sprite2 else collide_circle(sprite1, sprite2)



def orientation_from_components(dx, dy):
        """Triangulation to return angle of orientation."""
        if float(dx) == 0:
            if float(dy) >= 0:
                orientation = pi / 2.
            else:
                orientation = 3.*pi / 2.
        else:
            orientation = atan2(float(dy), float(dx))
        return orientation