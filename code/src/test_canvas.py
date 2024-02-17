import pytest
import math

from canvas import Point

class TestPoint:
    @pytest.fixture
    def setup_point(self):
        test_point = Point(name="testPoint", x_coord=0, y_coord=0, id=42)
        yield test_point
        del test_point

    def test_get_coords(self, setup_point):
        coords = (0,0)
        assert setup_point.get_x() == coords[0] and setup_point.get_y() == coords[1]

    def test_equals(self, setup_point):
        assert setup_point == Point(name="anotherTestPoint", x_coord=0, y_coord=0, id=13)

