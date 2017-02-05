import numpy as np
from math import radians, tan

def viewing_transform(fov, aspect, near, far):
    q = 1 / tan(radians(fov * 0.5))
    a = q / aspect
    b = (far + near) / (near - far)
    c = (2*near*far) / (near - far)
    return np.matrix([[a,  0,  0,  0],
                      [0,  q,  0,  0],
                      [0,  0,  b,  c],
                      [0,  0, -1,  0]])

