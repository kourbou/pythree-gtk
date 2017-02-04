import numpy as np
import math

def viewing_transform(fov, aspect, near, far):
    """ Returns a numpy matrix that transforms points into image space """
    
    t = 1/math.tan(math.radians(fov)/2)
    a = -(far + near)/(far - near)
    b = -(2*far*near)/(far - near)
    r = aspect
    return np.matrix([[t,   0,   0,   0],
                      [0, r*t,   0,   0],
                      [0,   0,   a,  -1],
                      [0,   0,   b,   0]])
