# Python Core Imports
import math

# Library Imports

# User Defined Class Imports

# Global Vars

# Classes

class Point():
    def __init__(self, name:str, x_coord:int, y_coord:int):
        self._x = x_coord
        self._y = y_coord
        self._name = name

    def getCoordinates(self) ->tuple:
        return(self._x, self._y)
    
    def getName(self)->str:
        return(self._name)

class Compass():
    def __init__(self):
        pass

    def getCentroid(self, pointList):
        '''
            PURPOSE: 
                Gets the centroid of the bounding box that contains a cluster of objects
                    nb - bounding box used to get geometric centre, and reduce impact of centroids in skewed distribution.
            INPUT ARGS:
                pointsList - list of Point Objects
            OUTPUT:
                Tuple of Point objects of form ((LowerLeftPoint),(TopRightPoint),(centroid))
        '''

        if len(pointList) == 1:

            return (Point("LL", pointList[0].getCoordinates()[0], pointList[0].getCoordinates()[1]),
                    Point("TR", pointList[0].getCoordinates()[0], pointList[0].getCoordinates()[1]),
                    Point("centroid", pointList[0].getCoordinates()[0], pointList[0].getCoordinates()[1]))

        min_x = 3*10**8; max_x = 0
        min_y = 3*10**8; max_y = 0

        for point in pointList:
            x,y = point.getCoordinates()
            if x < min_x:
                min_x = x 
            elif x > max_x:
                max_x = x
            else:
                pass

            if y < min_y:
                min_y = y 
            elif y > max_y:
                max_y = y 
            else:
                pass 

        return ((Point("LL",min_x, min_y)), 
                (Point("TR",max_x,max_y)), 
                (Point("centroid",((min_x+max_x)/2),((min_y+max_y)/2))))

    
    def getSideLength(self, point1, point2):
        #Gets the euclidian distance between two points

        return math.dist(point1.getCoordinates(), point2.getCoordinates())
    
    def getReferencePoints(self, boundingBox:list[Point], centroid:Point):
        '''
        PURPOSE:
            Get the three reference points required to calculate angles for rotations. 
        INPUT ARGS:
            boundingBox - list of Points, specifically the bottom Left and Top Right corners of a bounding Box
            centroid - point object - centre of a bounding box
        PROCESS:
            North is the x of the centroid and y of top of bounding box
            West is the X of the left of the bounding box and y of centroid
            NorthWest is the Top Left of the Bounding Box.
        OUTPUT:
            list of points objects
        '''

        N = Point("north",centroid.getCoordinates()[0], boundingBox[1].getCoordinates()[1])
        W = Point("west", boundingBox[0].getCoordinates()[0], centroid.getCoordinates()[1])
        NW = Point("northwest",boundingBox[0].getCoordinates()[1], boundingBox[1].getCoordinates()[0])

        return([N,W,NW])


    
    def getAngle(self, reference:Point, centroid:Point, point:Point):
        '''
            PURPOSE:
                Gets the angle between a 'true north' reference point, the centroid of the object cluster and a specific point
            INPUT ARGS:
                reference - point object - includes the (x,y) includes coordinates of a reference point that will be used to derive a rotation angle
                centroid - point object - includes the (x,y) includes coordinates of the centroid of the bounding box containing of objects in the query term. 
                point - point object - includes the (x,y) coordinates of the point we are finding the angle too
            PROCESS:
                Create a triangle from reference to centroid to point. 
                Use cosine rule to determine angle [clockwise] from reference to centroid to point
            OUTPUT:
                cos_inverse_of_x - Int - the Angle of Reference, Centroid, Point 
        '''
        #Gets the angle between a "True North" reference point

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

        cos_inverse_of_x = math.degrees(math.acos(x))                   #Convert from radians to degrees readability 

        if point.getCoordinates()[0] < centroid.getCoordinates()[0]:
            cos_inverse_of_x += 180

        return cos_inverse_of_x
    
    def getAllAngles(self, reference:Point, centroid:Point, points:list[Point]):
        '''
        PURPOSE:
            Gets the angles from of every point from the line of reference point - centroid
        INPUT ARGS:
            reference - point object - point on the edge of the bounding box we will use to generate rotation angles
            centroid - point object - centre of the bounding box that we will rotate around
            points - list of point objects - each point we want to measure the angle to relative to the line centroid-reference
        METHOD:
            Feed each list item into the getAngle function in turn & append to list of angles
        OUTPUT:
            angles - list of ints, the angle associated with each list item in points from the given reference point - centroid line.
        '''
        
        angles = []

        for point in points: 
            angles.append(self.getAngle(reference=reference, centroid=centroid, point=point))

        return angles
    
    def rotatePoint(self, centroid:Point, point:Point, angle:int):
        '''
        PURPOSE:
            given a point and an implicit canvas, rotate that point counter-clockwise around the canvas by a given angle.
        INPUT ARGS:
            centroid - point object - the pivot
            point - point object - the point to rotate around the pivot
            angle - int - angle in degrees to rotate the point around the pivot
        PROCESS:
            Convert degrees to radians
            Apply math transformation to the point to get it to the new location
        OUTPUT:
            pointPrime - point object - the new location of a given point. 
        '''
        #Note: Rotates counter-clockwise

        angle_rad = math.radians(angle)

        ox, oy = centroid.getCoordinates()
        px, py = point.getCoordinates()

        qx = ox + math.cos(angle_rad) * (px - ox) - math.sin(angle_rad) * (py - oy)
        qy = oy + math.sin(angle_rad) * (px - ox) + math.cos(angle_rad) * (py - oy)
        
        return Point(point.getName()+"`",qx, qy)

    def rotateAllPoints(self, centroid:Point, points:list[Point], angle:int):
        '''
        PURPOSE:
            apply a rotation to all points on a canvas
        INPUT ARGS:
            centroid - point object - the pivot point
            points - list of point objects - the points on the 'canvas' to move around the pivot
            angle - int - angle in degrees to rotate all the points arounf the pivot by
        METHOD:
            feed each point in turn to the rotatePoint method and save the whole canvasState to a list
        OUTPUT:
            rotatedPoints - list of point objects - the new state of the canvas after rotatations have been applied
        '''
        
        rotatedPoints = []

        for point in points:
            rotatedPoints.append(self.rotatePoint(centroid=centroid, point=point, angle=angle))

        return(rotatedPoints)
    
    def multiRotatePoints(self, centroid:Point, points:list[Point], angles:list[int]):
        '''
        PURPOSE:
            apply a whole canvas rotation multiple times, updating the canvas state each time
        INPUT ARGS:
            centroid - point object - the pivot point
            points - list of point objects - the points on the 'canvas' to move around the pivot
            angles - list of ints - the angles to apply to the rotation, in order. 
        PROCESS:
            for each angle, feed the canvas to the rotateAllPoints function
            update the state of the canvas each iteration
        '''

        canvas = points
        canvasList = []

        canvasList.append(canvas)

        for angle in angles:
            canvas = self.rotateAllPoints(centroid=centroid, points=canvas, angle=angle)
            canvasList.append(canvas)

        return canvasList
    



# Main