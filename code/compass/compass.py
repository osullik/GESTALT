# Python Core Imports
import math

# Library Imports

# User Defined Class Imports

# Global Vars
INFINITY = float('inf')
NEG_INFINITY = float('-inf')

# Classes

class Point():
    def __init__(self, name:str, x_coord:int, y_coord:int, id:int=INFINITY):
        self._x = x_coord
        self._y = y_coord
        self._name = name
        self._id=id

    def getCoordinates(self) ->tuple:
        return(self._x, self._y)
    
    def getName(self)->str:
        return(self._name)
    
    def dumpTuple(self)->tuple:
        return((self._name, (self._x, self._y)))
    
    def updateCoordinates(self,x,y):
        self._x = x
        self._y = y

    def get_point_id(self)->int:
        return self._id
    
    def _set_point_id(self, id:int)->None:
        self._id = id

class Canvas():
    def __init__(self,canvas_name:str) -> None:
        self._name = canvas_name
        self._BL, self._TL, self._TR, self._BR = self.set_canvas_boundaries()
        self._member_points_by_id = {}
        self._member_points_by_name = {}
        self._id_counter = 0

    def get_name(self)->str:
        return self._name

    def update_name(self, canvas_name:str)->None:
        self._name = canvas_name
    
    def set_canvas_boundaries(self, bottom_left_corner:tuple[int]=(0,0), top_right_corner:tuple[int]=(100,100))->tuple:
        bottom_left_point = Point(name=self.get_name()+"_BL", 
                                 x_coord=bottom_left_corner[0],
                                 y_coord=bottom_left_corner[1])
        top_left_point = Point(name=self.get_name()+"_TL", 
                                 x_coord=bottom_left_corner[0],
                                 y_coord=top_right_corner[1])
        top_right_point = Point(name=self.get_name()+"_TR", 
                                 x_coord=top_right_corner[0],
                                 y_coord=top_right_corner[1])
        bottom_right_point = Point(name=self.get_name()+"_BR", 
                                 x_coord=top_right_corner[0],
                                 y_coord=bottom_left_corner[1])
        
        return(bottom_left_point, top_left_point, top_right_point, bottom_right_point)
        
    def get_canvas_boundaries(self):
        return (self._BL, self._TL, self._TR, self._BR)
    
    def generate_point_id(self)->int:
        next_id = self._id_counter
        self._id_counter +=1
        return next_id
    
    def add_member_point(self, member_point:Point)->None:
        if member_point.get_point_id() == INFINITY:
            id = self.generate_point_id()
            member_point._set_point_id(id)
            self._member_points_by_id[id] = member_point
            try:
                self._member_points_by_name[member_point.getName()].append(member_point.get_point_id())
            except KeyError:
                self._member_points_by_name[member_point.getName()] = [(member_point.get_point_id())]

    def get_member_points(self)->list:
        return self._member_points_by_id
    
    def get_member_point_name_list(self)->list[str]:
        return list(self._member_points_by_name.keys())
    
    def get_member_points_using_name(self, name:str):
        found_points = []
        for point_name in self.get_member_point_name_list():
            if point_name == name:
                for id in self._member_points_by_name[name]:
                    found_points.append(self._member_points_by_id[id])

        return found_points
    
    def get_member_point_using_id(self, id:int)->Point:
        try:
            return self._member_points_by_id[id]
        except KeyError:
            print(f"Key: '{id}' not found")
            return None
                
    


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

        min_x = INFINITY; max_x = NEG_INFINITY
        min_y = INFINITY; max_y = NEG_INFINITY

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
        NW = Point("northwest",boundingBox[0].getCoordinates()[0], boundingBox[1].getCoordinates()[1])

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
        #print("##########")
        #print("Name", point.getName(), "C", c, "P", p, "N", n)
        #print("CENTROID", centroid.getCoordinates())
        #print("POINT", point.getCoordinates())
        #print("REFERENCE", reference.getCoordinates())
        
        try:
            x = (((pow(p,2)) + (pow(n,2)) - (pow(c,2)))/(2*(p)*(n)))
        except ZeroDivisionError as e:
            return 0 ### Unsure if this is the best way to handle it. 

        try:
            cos_inverse_of_x = math.degrees(math.acos(x))                   #Convert from radians to degrees readability 
        except ValueError as ve:  # -1.0000000002 case
            x = round(x,4)
            cos_inverse_of_x = math.degrees(math.acos(x))
            

        if point.getCoordinates()[0] < centroid.getCoordinates()[0]:
            cos_inverse_of_x = 360 - cos_inverse_of_x

        #print(point.getName(), centroid.getName(), reference.getName(), cos_inverse_of_x)
        #print(point.getCoordinates(), centroid.getCoordinates(), reference.getCoordinates(), cos_inverse_of_x)
        #print("ANGLE:", cos_inverse_of_x)
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
    
    def getAnglesAllRefs(self, centroid:Point, references:list[Point], point:Point):
        angles = []
        for reference in references:
            #print("REFERENCE_POINT", reference.getName())
            angles.append(self.getAngle(reference=reference, centroid=centroid, point=point))

        return angles
    
    def getAnglesAllRefsAllPoints(self, centroid:Point, references:list[Point], points:list[Point]):
        angles = []

        #print("ANGLES ARE:")
        for point in points:
            pointAngles = self.getAnglesAllRefs(centroid=centroid, references=references, point=point)
            angles.extend(pointAngles)
            
        
        return angles
    
    def rotatePoint(self, centroid:Point, point:Point, angle:int, alignToIntegerGrid:bool=False):
        '''
        PURPOSE:
            given a point and an implicit canvas, rotate that point counter-clockwise around the canvas by a given angle.
        INPUT ARGS:
            centroid - point object - the pivot
            point - point object - the point to rotate around the pivot
            angle - int - angle in degrees to rotate the point around the pivot
            alignToIntegerGrid - boolean - tells the function whether or not to force alignment to discrete integer positions.
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

        if alignToIntegerGrid == True:
            qx = round(qx)
            qy = round(qy)

        return Point(point.getName(),qx, qy)

    def rotateAllPoints(self, centroid:Point, points:list[Point], angle:int, alignToIntegerGrid:bool=False):
        '''
        PURPOSE:
            apply a rotation to all points on a canvas
        INPUT ARGS:
            centroid - point object - the pivot point
            points - list of point objects - the points on the 'canvas' to move around the pivot
            angle - int - angle in degrees to rotate all the points arounf the pivot by
            alignToIntegerGrid - boolean - tells the function whether or not to force alignment to discrete integer positions.
        METHOD:
            feed each point in turn to the rotatePoint method and save the whole canvasState to a list
        OUTPUT:
            rotatedPoints - list of point objects - the new state of the canvas after rotatations have been applied
        '''
        
        rotatedPoints = []

        for point in points:
            rotatedPoint = self.rotatePoint(centroid=centroid, point=point, angle=angle, alignToIntegerGrid=alignToIntegerGrid)
            rotatedPoints.append(rotatedPoint)

        return(rotatedPoints.copy())
    
    def multiRotatePoints(self, centroid:Point, points:list[Point], angles:list[int],rotateFromBlank:bool=True, aligntoIntegerGrid:bool=False):
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
            angle = int(angle)

            if rotateFromBlank == False:
                canvas = self.rotateAllPoints(centroid=centroid, points=canvas, angle=angle, alignToIntegerGrid=aligntoIntegerGrid).copy()
            else:
                canvas = self.rotateAllPoints(centroid=centroid, points=points, angle=angle, alignToIntegerGrid=aligntoIntegerGrid).copy()
                
            canvasList.append(canvas)

        return canvasList.copy()
    
    def getUniqueStates(self, states:list[list[Point]])->list:
        '''
        PURPOSE:
            Deduplicate states created in the rotation so that there are fewer queries run through GESTALT's recursive grid search. 
        INPUT ARGS:
            states - list lists of of Point objects - the states generated by rotating the query points around the axis. 
        PROCESS:
            Dump the points to plain tuples
            Convert the list of tuples for a state into a frozenset (using a set makes them order-invariant for the points)
            Take the set of all uniquePoint frozensets. 
        OUTPUT
            UniqueStates - set of Frozensets - the unique possible rotations out of all the rotations. 
        '''
        uniqueStates = set()
        for state in states:
            points = []
            for point in state:
                points.append(point.dumpTuple())
            pointSet = frozenset(points)
            uniqueStates.add(pointSet)

        return uniqueStates    
    

    def generateRotations(self,points:list[Point], alignToIntegerGrid:bool=False):

        LL, TR, centroid = self.getCentroid(points)
        referencePoints = self.getReferencePoints(boundingBox=[LL,TR], centroid=centroid)
        angles = self.getAnglesAllRefsAllPoints(centroid=centroid, references=referencePoints, points=points)
        states = self.multiRotatePoints(centroid=centroid, points=points, angles=angles, rotateFromBlank=True, aligntoIntegerGrid=alignToIntegerGrid)
        uniqueStates = self.getUniqueStates(states=states)

        return uniqueStates



# Main