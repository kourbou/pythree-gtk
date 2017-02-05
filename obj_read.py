from numpy import matrix as mat
import itertools
import math

class ObjReader(object):
    def __init__(self, path):
        self.edges = []
        self.vertices = []

        with open(path) as f:
            self.text = f.readlines()
        
        # New line cleanup.
        self.text = [x.strip() for x in self.text]
        k = [] # Edges
        
        maxX = -math.inf
        maxY = -math.inf
        maxZ = -math.inf
        minX = math.inf
        minY = math.inf
        minZ = math.inf


        for line in self.text:
            data = line.split()
            if not data:
                continue
            
            if data[0] == 'v':
                xf, yf, zf = float(data[1]), float(data[2]), float(data[3])

                maxX = max(xf, maxX)
                maxY = max(yf, maxY)
                maxZ = max(zf, maxZ)
                
                minX = min(xf, minX)
                minY = min(yf, minY)
                minZ = min(zf, minZ)

                self.vertices.append(mat([[xf], [yf], [zf], [1.]]))
            elif data[0] == 'f':
                k.append([int(data[1].split('/')[0])-1, int(data[2].split('/')[0])-1])
                k.append([int(data[2].split('/')[0])-1, int(data[3].split('/')[0])-1])
                k.append([int(data[1].split('/')[0])-1, int(data[3].split('/')[0])-1])
            else:
                print('Unknown Data: %s' % data)
        
        # Sort edges and the vertices indexes
        for l in k:
            l.sort()
        k.sort() 
        k = [k[i] for i in range(len(k)) if i == 0 or k[i] != k[i-1]]
        # Delete duplicate edges
        self.edges = [k[i] for i in range(len(k)) if i == 0 or k[i] != k[i-1]]

        # Set object center
        self.origin = [(maxX + minX)/2, (maxY + minY)/2, (maxZ + minZ)/2]

        print('Origin: %s' % self.origin)
