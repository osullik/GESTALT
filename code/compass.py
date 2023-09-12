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

        cos_inverse_of_x = math.degrees(math.acos(x))

        if point[0] < centroid[0]:
            cos_inverse_of_x += 180

        return cos_inverse_of_x
    
    def getAllAngles(self, reference:tuple, centroid:tuple, points:list[tuple]):
        
        angles = []

        for point in points: 
            angles.append(self.getAngle(reference=reference, centroid=centroid, point=point))

        return angles
    
    def rotatePoint(self, centroid:tuple, point:tuple, angle:int):

        angle_rad = math.radians(angle)

        ox, oy = centroid
        px, py = point

        qx = ox + math.cos(angle_rad) * (px - ox) - math.sin(angle_rad) * (py - oy)
        qy = oy + math.sin(angle_rad) * (px - ox) + math.cos(angle_rad) * (py - oy)
        
        return (qx, qy)

    def rotateAllPoints(self, centroid:tuple, points:list[tuple], angle:int):
        
        rotatedPoints = []

        for point in points:
            rotatedPoints.append(self.rotatePoint(centroid=centroid, point=point, angle=angle))

        return(rotatedPoints)

# Main