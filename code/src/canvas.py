import itertools
import math
import copy
import numpy as np

class Point():
    def __init__(self, name:str, x_coord:int, y_coord:int, id:int=None):
        self._x = x_coord
        self._y = y_coord
        self._name = name
        self._id = id

    def __str__(self)->str:
        return self._name + "(" + str(self._x) + "," + str(self._y) + ")"
    
    def __eq__(self, other)->bool:
        return isinstance(other, Point) and self._x == other.get_x() and self._y == other.get_y()

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




