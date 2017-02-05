import numpy as np
import math


'''

Scale tranforms:

                   [a  0  0  0]
    [x  y  z  1] * [0  b  0  0] = [ax  by  cz  1]
                   [0  0  c  0]
                   [0  0  0  1]

Translate transforms:

                   [1  0  0  0]
    [x  y  z  1] * [0  1  0  0] = [x+a y+b z+c 1]
                   [0  0  1  0]
                   [a  b  c  1]
'''
# Where ax, by and cz are units
def scale_transform(ax, by, cz):
    return np.matrix([[ax,  0,  0,  0],
                      [ 0, by,  0,  0],
                      [ 0,  0, cz,  0],
                      [ 0,  0,  0,  1]])

# Where ax, by and cz are units
def translate_transform(ax, by, cz):
    return np.matrix([[ 1,  0,  0, ax],
                      [ 0,  1,  0, by],
                      [ 0,  0,  1, cz],
                      [ 0,  0,  0,  1]])

# Where ax, by, and cz are angles in degrees
def rotate_transform(ax, by, cz):
    axf = math.radians(ax)
    byf = math.radians(by)
    czf = math.radians(cz)

    matx = np.matrix([[1,             0,             0, 0],
                      [0, math.cos(axf),-math.sin(axf), 0],
                      [0, math.sin(axf), math.cos(axf), 0],
                      [0,             0,             0, 1]])

    maty = np.matrix([[ math.cos(byf), 0, math.sin(byf), 0],
                      [             0, 1,             0, 0],
                      [-math.sin(byf), 0, math.cos(byf), 0],
                      [             0, 0,             0, 1]])
    
    matz = np.matrix([[math.cos(czf),-math.sin(czf), 0, 0],
                      [math.sin(czf), math.cos(czf), 0, 0],
                      [            0,             0, 1, 0],
                      [            0,             0, 0, 1]])

    return matx * maty * matz
