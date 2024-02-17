import pytest
import math
from copy import copy

from canvas import Point
from canvas import Canvas

class TestCanvas:
    @pytest.fixture
    def setup_canvas(self):
        pts_list = [{'name':'a','x':0,'y':0}, {'name':'b','x':0,'y':5}]
        test_canvas = Canvas(name="testCanvas", center=(0,0), points=pts_list, BL=(0,0), BR=(10,0), TL=(0,10), TR=(10,10))
        yield test_canvas
        del test_canvas

    def test_centroid(self, setup_canvas):
        assert setup_canvas.get_centroid() == Point("expectedCentroid", x=0, y=2.5)

    def test_center(self, setup_canvas):
        assert setup_canvas.get_center() == Point("expectedCentroid", x=5, y=5)
    




    