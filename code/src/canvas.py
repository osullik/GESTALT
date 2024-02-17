import itertools
import math
import copy
import numpy as np

class Point():
    def __init__(self, name:str, x:int, y:int, id:int=None):
        self._x = x
        self._y = y
        self._name = name
        self._id = id

    def __str__(self)->str:
        return self._name + "(" + str(self._x) + "," + str(self._y) + ")"
    
    def __eq__(self, other)->bool:
        return isinstance(other, Point) and self._name == other.get_name() and \
               self._x == other.get_x() and self._y == other.get_y()

    def __iter__(self):
        yield self._x 
        yield self._y

    def get_x(self) ->int:
        return self._x

    def get_y(self) ->int:
        return self._y
    
    def get_name(self)->str:
        return(self._name)

    def get_id(self)->int:
        return(self._id)


    # Assume angle is in degrees
    def rotate(self, origin, angle):
        angle_rad = math.radians(angle)

        ox, oy = (origin.get_x(), origin.get_y())
        px, py = (self._x, self._y)

        qx = ox + math.cos(angle_rad) * (px - ox) - math.sin(angle_rad) * (py - oy)
        qy = oy + math.sin(angle_rad) * (px - ox) + math.cos(angle_rad) * (py - oy)

        self._x, self._y = qx, qy


    def translate(self, xshift, yshift):
        self._x += xshift
        self._y += yshift

    
    def get_angle(self, origin, other):
        a = np.array([self._x, self._y])
        b = np.array([origin.get_x(), origin.get_y()])
        c = np.array([other.get_x(), other.get_y()])

        ba = a - b
        bc = c - b

        cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
        angle = np.degrees(np.arccos(cosine_angle))

        if self._x < origin.get_x():
            angle = 360 - angle

        return angle




class Canvas():
    '''
    The Canvas Object is the parent object to store the Points used by compass
    and is the target of the COMPASS operations.
    A single canvas represents a single location. 
    A canvas can have many points, each with a unique ID.
    No other attributes must be unique. 

    points is a collection ocontaining dict entries like {name: "", x:_, y:_}
    '''
    def __init__(self, points, center, BL, TL, TR, BR, name:str=None):
        self._name = name
        self._id_iter = itertools.count()

        self._points = [Point(**p, id=next(self._id_iter)) for p in points]
        self._BL = Point("BL", BL[0], BL[1])
        self._TL = Point("TL", TL[0], TL[1])
        self._TR = Point("TR", TR[0], TR[1])
        self._BR = Point("BR", BR[0], BR[1])
        self._center = Point("center", center[0], center[1])  # TODO error check center is actually center

        self._centroid = None
        self._ref_T = None
        self._ref_L = None
        self._ref_TL = None
        
        self.update_centroid()
        self.update_reference_points()

    def __repr__(self)->str:
        pts = ', '.join(f'{c!s}' for c in self._points)
        return f'{self.__class__.__name__}({pts})'

    def __eq__(self, other)->bool:
        return isinstance(other, Canvas) and \
               self.get_points() == other.get_points() and \
               self.get_center() == other.get_center() and \
               self.get_centroid() == other.get_centroid()
               # TODO: also check ref points and boudns

    def __iter__(self):
        for p in self._points:
            yield {'name':p.get_name(), 'x':p.get_x(), 'y':p.get_y()}   

    def get_centroid(self):
        return tuple(self._centroid)

    def get_center(self):
        return tuple(self._center)

    def get_points(self):
        return [tuple(p) for p in self._points]

    def get_reference_points(self):
        return {'T':tuple(self._ref_T), 'L':tuple(self._ref_L), 'TL':tuple(self._ref_TL)}

    def update_centroid(self):
        C_x = np.mean([p.get_x() for p in self._points])
        C_y = np.mean([p.get_y() for p in self._points])
        self._centroid = Point("centroid", x=C_x, y=C_y)

    def update_reference_points(self):
        self._ref_T = Point("north", self._center.get_x(), self._TL.get_y())
        self._ref_L = Point("west", self._TL.get_x(), self._center.get_y())
        self._ref_TL = Point("northwest", self._TL.get_x(), self._TL.get_y())

    def add_point(self, name, x, y):
        self._points += [Point(name, x, y, id=next(self._id_iter))]
        self.update_centroid()

    def remove_point(self, name, x, y):
        # Keep only points that have diff coord or diff name from args
        self._points = [p for p in self._points if p != Point(name, x, y)]
        self.update_centroid()

    # Assume always rotating about centroid of current points
    def rotate(self, angle):
        for p in self._points:
            p.rotate(self._centroid, angle)
