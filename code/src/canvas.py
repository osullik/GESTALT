import itertools

class Point():
    def __init__(self, name:str, x_coord:int, y_coord:int, id:int):
        self._x = x_coord
        self._y = y_coord
        self._name = name
        self._id = id

    def __str__(self)->str:
        return self._name + "(" + str(self._x) + "," + str(self._y) + ")"

    def get_x(self) ->int:
        return self._x

    def get_y(self) ->int:
        return self._y
    
    def get_name(self)->str:
        return(self._name)

    def get_id(self)->int:
        return(self._id)

    def __eq__(self, other)->bool:
        return isinstance(other, Point) and self._x == other.get_x() and self._y == other.get_y()


