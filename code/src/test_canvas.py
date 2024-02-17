import pytest
import math
from copy import copy

from canvas import Point
from canvas import Canvas

class TestCanvas:
    @pytest.fixture
    def setup_canvas(self):
        test_canvas = Canvas(name="testCanvas", center=(0,0), points=[{'name':'a','x':0,'y':0}, {'name':'b','x':0,'y':5}])
        yield test_canvas
        del test_canvas

    def test_print(self, setup_canvas):
        print(setup_canvas)
        assert False
    




    