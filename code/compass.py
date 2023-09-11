# Python Core Imports
import math

# Library Imports

# User Defined Class Imports

# Global Vars

# Classes

class Compass():
    def __init__(self):
        pass

    def getCentroid(self, pointList):
        
        x = 0
        y = 0
        numTuples = 0

        for point in pointList:
            x += point[0]
            y += point[1]
            numTuples += 1

        return ((x/numTuples), (y/numTuples))
    
    def getSideLength(self, point1, point2):

        return math.dist(point1, point2)

    
    def getAngle(self, reference:tuple, centroid:tuple, point:tuple):

        # Cosine Rule ->  a^2 = b^2 + c^2 - 2bc cos(x)
        # cos(x) = ((b^2 + c^2 - a^2) / 2bc)     
        
        #       
        #      N
        #     |z\
        #     |  \   c
        #   p |   \
        #     |x  y\
        #      C --- P
        #         n
        #         
        
        #c = side opposite the centroid
        #p = side opposite the point
        #n = side opposite the reference
        #x = angel we are trying to find 

        c = self.getSideLength(point1=point, point2=reference)
        p = self.getSideLength(point1=centroid, point2=reference)
        n = self.getSideLength(point1=centroid, point2=point)

        x = (((pow(p,2)) + (pow(n,2)) - (pow(c,2)))/(2*(p)*(n)))

        cos_inverse_of_x = math.acos(x)

        return math.degrees(cos_inverse_of_x)




# Main