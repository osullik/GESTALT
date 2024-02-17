import pytest
import math
from copy import copy

from canvas import Point
from canvas import Canvas

class TestCanvas:
    @pytest.fixture
    def setup_canvas(self):
        pts_list = [{'name':'a','x':0,'y':0}, {'name':'b','x':0,'y':5}]
        test_canvas = Canvas(name="testCanvas", center=(5,5), points=pts_list, BL=(0,0), BR=(10,0), TL=(0,10), TR=(10,10))
        yield test_canvas
        del test_canvas

    def test_centroid(self, setup_canvas):
        assert setup_canvas.get_centroid() == (0,2.5)

    def test_center(self, setup_canvas):
        assert setup_canvas.get_center() == (5,5)

    def test_add_point(self, setup_canvas):
        pts_list = [{'name':'a','x':0,'y':0}, {'name':'b','x':0,'y':5}]
        new_pt = {'name':'c','x':4,'y':6}
        setup_canvas.add_point(**new_pt)
        pts_list.append(new_pt)
        assert setup_canvas == Canvas(name='testCanvas', center=(5,5), points=pts_list, BL=(0,0), BR=(10,0), TL=(0,10), TR=(10,10))
    
    def test_add_point(self, setup_canvas):
        pts_list = [{'name':'a','x':0,'y':0}]
        del_pt = {'name':'b','x':0,'y':5}
        setup_canvas.remove_point(**del_pt)
        assert setup_canvas == Canvas(name='testCanvas', center=(5,5), points=pts_list, BL=(0,0), BR=(10,0), TL=(0,10), TR=(10,10))
    

    def test_rotate(Self, setup_canvas):
        pass



    