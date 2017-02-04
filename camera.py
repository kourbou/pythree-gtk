import numpy as np
import math

'''
Viewing Tranform:
    You need:
        - P, camera postition (Px, Py, Pz)
        - Direction camera is pointing
        - Up direction (if camera is tilted)
        - Angle alpha, FOV Viewing Angle
        - Two other values, near (n) and far (f)
        - The aspect ratio of our screen (r)

         Frustum             Cube

              /|
             / |
         |  /  |           
         | *   |          *---|-----
         |/|   |          |   |    |
 z <-----|-|---|------ -> ----|----|
         |\|   |          |   |    |
         | \   |          ----|-----
         |  \  |
             \ |
              \|
         <--> n
         <-----> f

The first step is to transform the whole view so that the camera is at
the origin and it's pointing towards -z.

There's a pyramid coming out the camera, known as the Viewing Pyramid.
Inside the pyramid are the things we care about. Start by transferring
to 'image space' (cube 1 -1 1 -1). We add two planes, one near and one
far. Turning a square frustum into a cube. Matrix that looks something
like this:
               Matrix M
            [t  0   0   0]
[x y z 1] * [0  rt  0   0] = [tx ty az+b -z]
            [0  0   a  -1]
            [0  0   b   0]

Notice we're going to have to divide by -z because of the w dimension,
hence why things far from us appear smaller. Also (0,0,-n) and (0,0,-f)
should come out the same through the matrix. So we can solve this:
    
    [0 0 -n 1] * M = [0 0 -an+b n]  -- 3D --> (0 0 (-an+b)/n)
    [0 0 -f 1] * M = [0 0 -af+b f]  -- 3D --> (0 0 (-af+b)/f)

But because of the way we defined the cube earlier:

    (0 0 (-an+b)/n) = (0  0  1)
    (0 0 (-af+b)/f) = (0  0 -1)

Solve with system of equations:

    a = (f+n)/(f-n) and b=(2nf)/(f-n)

So we can put those values in our matrix. Now we need to determine t.
We can find it by using that '*' point which corresponds to (0, d,-n)
d = n*tan(alpha/2) so we're going to do [0 n*tan(alpha/2) -n 1] * M:

    [0 n*tan(alpha/2) -n 1] * M = [0 t*n*tan(alpha/2) ... n]

    [0 t*n*tan(alpha/2) ... n] -- 3D --> (0 t*tan(alpha/2) 1)

But we know that point corresponds to (0 1 1), therefore:

    t*tan(alpha/2) = 1
    t = 1/(tan(alpha/2))

We also need to multiply by our aspect ratio for the y values.
So if our aspect ratio is r our final matrix is:

    [1/(tan(alpha/2))  0                 0            0]
    [0                 r/(tan(alpha/2))  0            0]
    [0                 0                 (f+n)/(f-n) -1]
    [0                 0                 (2nf)/(f-n)  0]

Remember to always redivide by the W component to get back to 3D:
(x y z) -- 4D --> [x y z 1] * M = [x' y' z' w] -- 3D --> (x'/w y'/w z'/w)

The function below returns a matrix where FOV is in degrees and the 
aspect ratio is w/h. We still need to do clipping and checking what
is visible and what isn't.

'''

def viewing_transform(fov, aspect, near, far):
    """ Returns a numpy matrix that transforms points into image space """
    fovf = fov * math.pi / 180
    
    t = 1/math.tan(fovf * math.pi / 360)
    a = (far + near)/(far - near)
    b = (2*near*far)/(far-near)
    r = aspect
    return np.matrix([[t,   0,   0,   0],
                      [0, r*t,   0,   0],
                      [0,   0,   a,  -1],
                      [0,   0,   b,   0]])
