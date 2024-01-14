# Python Core Imports
import math
import gc

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

    def get_coordinates(self) ->tuple:
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

    def check_point_equality(self, comparison_point)->bool:
        if self._x == comparison_point._x and self._y == comparison_point._y:
            return True
        else:
            return False


class Canvas():
    '''
    The Canvas Object is the parent object to store the Points used by compass
    and is the target of the COMPASS operations.
    A single canvas represents a single location. 
    A canvas can have many points, each with a unique ID.
    No other attributes must be unique. 
    '''
    def __init__(self,canvas_name:str) -> None:
        self._name = canvas_name
        self._BL, self._TL, self._TR, self._BR, self._canvas_centroid = self.generate_canvas_boundaries()
        self.north_ref, self.west_ref, self.north_west_ref = self.generate_canvas_reference_points()
        self._member_points_by_id = {}
        self._member_points_by_name = {}
        self._id_counter = 0             #Counter always increases, no re-use of IDs.

    def get_name(self)->str:
        return self._name

    def update_name(self, canvas_name:str)->None:
        self._name = canvas_name
    
    def set_canvas_boundaries(self, bottom_left_corner:tuple[int], top_right_corner:tuple[int])->None:
        self._BL, self._TL, self._TR, self._BR, self._canvas_centroid = self.generate_canvas_boundaries(bottom_left_corner, top_right_corner)

    def generate_canvas_boundaries(self, bottom_left_corner:tuple[int]=(0,0), top_right_corner:tuple[int]=(100,100))->tuple:
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
        
        canvas_centroid = Point("centroid",((bottom_left_corner[0]+top_right_corner[0])/2),
                                ((bottom_left_corner[1]+top_right_corner[1])/2))
        
        return(bottom_left_point, top_left_point, top_right_point, bottom_right_point, canvas_centroid)
    
    def generate_canvas_reference_points(self):
        N = Point("north",self.get_canvas_centroid().get_coordinates()[0], self._TR.get_coordinates()[1])
        W = Point("west", self._BL.get_coordinates()[0], self.get_canvas_centroid().get_coordinates()[1])
        NW = Point("northwest", self._TL.get_coordinates()[0], self._TL.get_coordinates()[1])

        return(N,W,NW)
    
    def set_canvas_reference_points(self):
        N,W,NW = self.generate_canvas_reference_points()
        self.north_ref = N
        self.west_ref = W
        self.north_west_ref = NW

    def get_canvas_reference_points(self):
        return(self.north_ref, self.west_ref, self.north_west_ref)
    
    def get_canvas_centroid(self):
        return self._canvas_centroid
        
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
        try:
            for point_name in self.get_member_point_name_list():
                if point_name == name:
                    for id in self._member_points_by_name[name]:
                        found_points.append(self._member_points_by_id[id])
        except KeyError:
            print(f"Key: '{name}' not found")
            return None

        return found_points
    
    def get_member_point_using_id(self, id:int)->Point:
        try:
            return self._member_points_by_id[id]
        except KeyError:
            print(f"Key: '{id}' not found")
            return None
        
    def remove_member_point_from_canvas_by_id(self, member_point_id:int)->None:
        num_deleted = 0
        if self.get_member_point_using_id(member_point_id) == None:
            print(f"Deleted {num_deleted} points")
            return
        else:
            point_name = self._member_points_by_id[member_point_id].getName()
            if len(self._member_points_by_name[point_name]) == 1:
                del(self._member_points_by_name[point_name])
            else:
                self._member_points_by_name[point_name].remove(member_point_id)
            del(self._member_points_by_id[member_point_id])
            num_deleted +=1
            print(f"Deleted {num_deleted} points")
        gc.collect()
        return
        
    def remove_member_point_from_canvas_by_name(self, member_point_name:str)->None:
        num_deleted=0
        if self.get_member_points_using_name(member_point_name) == None:
            print(f"Deleted {num_deleted} points")
            return
        else:
            for pt in self.get_member_points_using_name(member_point_name):
                del(self._member_points_by_id[pt.get_point_id()])
            del(self._member_points_by_name[member_point_name])
        gc.collect()
    
    def get_points_bounding_box(self)->list[tuple]:
        
        points_dict = self.get_member_points()
        if len(points_dict.keys()) == 0:
            return([(0,0), (0,0)])
        
        min_x = INFINITY
        max_x = NEG_INFINITY
        min_y = INFINITY
        max_y = NEG_INFINITY

        for point in points_dict.keys():
            x,y = points_dict[point].get_coordinates()
            if x < min_x:
                min_x = x 
            if x > max_x:
                max_x = x

            if y < min_y:
                min_y = y 
            if y > max_y:
                max_y = y 

        #Ensure points not on bounding box boundary.
        min_x = min_x-1
        max_x = max_x+1
        min_y = min_y-1
        max_y = max_y+1

        return([(min_x,min_y),(max_x,max_y)])


class Compass():
    def __init__(self):
        pass

    def get_points_centroid(self, canvas:Canvas):
        '''
            PURPOSE: 
                Gets the centroid of the bounding box that contains a cluster of objects
                    nb - bounding box used to get geometric centre, and reduce impact of centroids in skewed distribution.
            INPUT ARGS:
                canvas - a canvas object containing the points
            OUTPUT:
                Tuple of Point objects of form ((LowerLeftPoint),(TopRightPoint),(centroid))
        '''

        points_dict = canvas.get_member_points()
        if len(points_dict) == 1:

            return (Point("centroid", points_dict[0].get_coordinates()[0], points_dict[0].get_coordinates()[1]))

        min_x = INFINITY; max_x = NEG_INFINITY
        min_y = INFINITY; max_y = NEG_INFINITY

        for point in points_dict.keys():
            x,y = points_dict[point].get_coordinates()
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

        return (Point("centroid",((min_x+max_x)/2),((min_y+max_y)/2)))

    
    def getSideLength(self, point1, point2):
        #Gets the euclidian distance between two points

        return math.dist(point1.get_coordinates(), point2.get_coordinates())
    
    def getReferencePoints(self, canvas:Canvas):
        #Reference points are the North, West, and NorthWest boundaries of the Canvas used to calculate the rotation angles
        N = Point("north",canvas.get_canvas_centroid().get_coordinates()[0], canvas._TR.get_coordinates()[1])
        W = Point("west", canvas._BL.get_coordinates()[0], canvas.get_canvas_centroid().get_coordinates()[1])
        NW = canvas._TL

        return([N,W,NW])

    def getAngle(self, canvas:Canvas, reference:str, point:Point):
        # Gets the angle between a 'true north' reference point, the centroid of the object cluster and a specific point
            
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

        if reference == 'north':
            ref = canvas.north_ref
        elif reference == 'west':
            ref = canvas.west_ref
        elif reference == 'northwest':
            ref = canvas.north_west_ref
        else:
            exit("invalid reference, choose from 'north', 'west' or 'northwest'") 

        c = self.getSideLength(point1=point, point2=ref)
        p = self.getSideLength(point1=canvas.get_canvas_centroid(), point2=ref)
        n = self.getSideLength(point1=canvas.get_canvas_centroid(), point2=point)
        
        try:
            x = (((pow(p,2)) + (pow(n,2)) - (pow(c,2)))/(2*(p)*(n)))
        except ZeroDivisionError as e:
            return 0 ### Unsure if this is the best way to handle it. 

        try:
            cos_inverse_of_x = math.degrees(math.acos(x))                   #Convert from radians to degrees readability 
        except ValueError as ve:  # -1.0000000002 case
            x = round(x,4)
            cos_inverse_of_x = math.degrees(math.acos(x))
            

        if point.get_coordinates()[0] < canvas.get_canvas_centroid().get_coordinates()[0]:
            cos_inverse_of_x = 360 - cos_inverse_of_x

        return cos_inverse_of_x
    
    def getAllAngles(self, canvas:Canvas, reference:str):
        angles = []
        points = canvas.get_member_points()

        for point in points.keys(): 
            angles.append(self.getAngle(canvas=canvas, reference=reference, point=points[point]))

        return angles
    
    def getAnglesAllRefs(self, centroid:Point, references:list[Point], point:Point):
        angles = []
        for reference in references:
            angles.append(self.getAngle(reference=reference, centroid=centroid, point=point))

        return angles
    
    def getAnglesAllRefsAllPoints(self, centroid:Point, references:list[Point], points:dict):
        angles = []

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

        ox, oy = centroid.get_coordinates()
        px, py = point.get_coordinates()

        qx = ox + math.cos(angle_rad) * (px - ox) - math.sin(angle_rad) * (py - oy)
        qy = oy + math.sin(angle_rad) * (px - ox) + math.cos(angle_rad) * (py - oy)

        if alignToIntegerGrid == True:
            qx = round(qx)
            qy = round(qy)

        return Point(point.getName(),qx, qy)

    def rotateAllPoints(self, centroid:Point, points:dict, angle:int, alignToIntegerGrid:bool=False):
        #apply a rotation to all points on a canvas
 
        rotatedPoints = []

        for point in points:
            rotatedPoint = self.rotatePoint(centroid=centroid, point=point, angle=angle, alignToIntegerGrid=alignToIntegerGrid)
            rotatedPoints.append(rotatedPoint)

        return(rotatedPoints.copy())
    
    def multiRotatePoints(self, centroid:Point, points:dict, angles:list[int],rotateFromBlank:bool=True, aligntoIntegerGrid:bool=False):
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
    

    def generateRotations(self,canvas:Canvas, alignToIntegerGrid:bool=False):

        centroid = self.getCentroid(canvas=canvas)
        referencePoints = self.getReferencePoints(canvas)
        angles = self.getAnglesAllRefsAllPoints(centroid=centroid, references=referencePoints, points=canvas.get_member_points())
        states = self.multiRotatePoints(centroid=centroid, points=canvas.get_member_points(), angles=angles, rotateFromBlank=True, aligntoIntegerGrid=alignToIntegerGrid)
        uniqueStates = self.getUniqueStates(states=states)

        return uniqueStates



# Main