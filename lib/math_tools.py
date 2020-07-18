import random
from pygame import transform, Surface

def clamp(val, minval, maxval):
    return max(min(val, maxval), minval)


def random_step_int(value, magnitude, minval, maxval):
    step_direction = random.randint(-1, 1)
    magnitude = random.randint(0,magnitude)

    return clamp(value+step_direction*magnitude, minval, maxval)

def random_step_float(value, magnitude, minval, maxval):
    step_direction = random.randint(-1, 1)
    magnitude = random.random()*magnitude

    return clamp(value+step_direction*magnitude, minval, maxval)

def scale_percentage(surface: Surface, scale_amount: float):
    return transform.smoothscale(surface, (int(surface.get_width()*scale_amount), int(surface.get_height()*scale_amount)))