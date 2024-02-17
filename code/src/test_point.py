import pytest
import math
from copy import copy

from canvas import Point

class TestPoint:
    @pytest.fixture
    def setup_0_0(self):
        test_point = Point(name="testPoint", x=0, y=0, id=42)
        yield test_point
        del test_point

    @pytest.fixture
    def setup_5_0(self):
        test_point = Point(name="testPoint", x=5, y=0, id=42)
        yield test_point
        del test_point

    @pytest.fixture
    def setup_5_10(self):
        test_point = Point(name="testPoint", x=5, y=10, id=42)
        yield test_point
        del test_point


    def test_get_coords(self, setup_0_0):
        coords = (0,0)
        assert setup_0_0.get_x() == coords[0] and setup_0_0.get_y() == coords[1]

    def test_equals(self, setup_0_0):
        assert setup_0_0 == Point(name="testPoint", x=0, y=0, id=13)

    def test_rotate1(self, setup_0_0):
        setup_0_0.rotate(origin=Point('C', x=5, y=5), angle=225)
        answer = Point("testPoint", x=5, y=5+5*math.sqrt(2))
        assert pytest.approx(setup_0_0.get_x(), 0.0001) == answer.get_x()
        assert pytest.approx(setup_0_0.get_y(), 0.0001) == answer.get_y()

    def test_rotate2(self, setup_5_10):
        setup_5_10.rotate(origin=Point('C', x=5, y=5), angle=180)
        answer = Point("testPoint", 5, 0)
        assert pytest.approx(setup_5_10.get_x(), 0.0001) == answer.get_x()
        assert pytest.approx(setup_5_10.get_y(), 0.0001) == answer.get_y()

    def test_translate(self, setup_0_0):
        setup_0_0.translate(20, -15)
        assert setup_0_0 == Point("testPoint", 20, -15)

    def test_angle1(self, setup_5_0):
    #     #
    #     # 5     N
    #     # 4    |z\
    #     # 3    |  \   c
    #     # 2  p |   \
    #     # 1    |x  y\
    #     # 0     C --- P
    #     #         n
    #     #      012345
        C = Point('centroid',0,0)
        N = Point('north',0,5)
        P = setup_5_0
        x, y, z = 90, 45, 45

        assert pytest.approx(P.get_angle(origin=C, other=N), 0.0001) == x
        # assert pytest.approx(N.get_angle(origin=P, other=C), 0.0001) == y
        # assert pytest.approx(C.get_angle(origin=N, other=P), 0.0001) == z

        # assert pytest.approx(N.get_angle(origin=C, other=P), 0.0001) == 360 - x
        # assert pytest.approx(C.get_angle(origin=P, other=N), 0.0001) == 360 - y
        # assert pytest.approx(P.get_angle(origin=N, other=C), 0.0001) == 360 - z


    def test_angle2(self, setup_0_0):
    #     # Test we get external angle of rotation when required
    #     #
    #     # 5           N
    #     # 4         / |
    #     # 3        /  |
    #     # 2     c /   | p
    #     # 1      /    |
    #     # 0     P --- C
    #     #          n   (x)
    #     #        012345
        
        C = Point('centroid2',5,0)
        N = Point('north2',5,5)
        P = setup_0_0
        x = 270

        assert pytest.approx(P.get_angle(origin=C, other=N), 0.0001) == x
        # assert pytest.approx(N.get_angle(origin=C, other=P), 0.0001) == 360 - x

