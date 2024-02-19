import pytest
import math
from copy import copy
import numpy as np

from canvas import Point
from canvas import Canvas

class TestCanvas:
    @pytest.fixture
    def setup_canvas(self):
        pts_list = [{'name':'a','x':0,'y':0}, {'name':'b','x':0,'y':5}]
        test_canvas = Canvas(name="testCanvas", center=(5,5), points=pts_list, BL=(0,0), BR=(10,0), TL=(0,10), TR=(10,10))
        yield test_canvas
        del test_canvas

    @pytest.fixture
    def setup_canvas2(self):
        pts_list = [{'name':'a','x':5,'y':10}, {'name':'b','x':10,'y':10}, {'name':'c','x':1,'y':1}]
        test_canvas = Canvas(name="testCanvas2", center=(5,5), points=pts_list, BL=(0,0), BR=(10,0), TL=(0,10), TR=(10,10))
        yield test_canvas
        del test_canvas

    @pytest.fixture
    def setup_canvas3(self):
        pts_list = [{'name':'a','x':10,'y':0}, {'name':'b','x':10,'y':5}, {'name':'c','x':0,'y':0}]
        test_canvas = Canvas(name="testCanvas3", center=(5,5), points=pts_list, BL=(0,0), BR=(10,0), TL=(0,10), TR=(10,10))
        yield test_canvas
        del test_canvas

    @pytest.fixture
    def setup_canvas_matrix(self):
        matrix = np.array( [[ 0,"A"],
                            ["B",0 ]], dtype=object)
        test_canvas = Canvas(name="testCanvas3", center=(5,5), matrix=matrix, BL=(0,0), BR=(1,0), TL=(0,1), TR=(1,1))
        yield test_canvas
        del test_canvas

    def test_centroid(self, setup_canvas):
        assert setup_canvas.get_centroid() == (0,2.5)

    def test_center(self, setup_canvas):
        assert setup_canvas.get_center() == (5,5)

    def test_reference_points(self, setup_canvas):
        assert setup_canvas.get_reference_points()['T'] == (5,10)
        assert setup_canvas.get_reference_points()['L'] == (0,5)
        assert setup_canvas.get_reference_points()['TL'] == (0,10)

    def test_init_matrix(self, setup_canvas_matrix):
        assert (0,1) in setup_canvas_matrix.get_points()
        assert (1,0) in setup_canvas_matrix.get_points()
        assert ['B','A'] == setup_canvas_matrix.get_point_names_x_sorted()
        assert ['A','B'] == setup_canvas_matrix.get_point_names_y_sorted()

    def test_get_points_sorted_x(self, setup_canvas2):
        assert setup_canvas2.get_point_names_x_sorted() == ['b', 'a', 'c']

    def test_get_points_sorted_y(self, setup_canvas):
        assert setup_canvas.get_point_names_y_sorted() == ['b', 'a']

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

    # def test_rotate(self, setup_canvas2):
    #     pts_list = [{'name':'a','x':5,'y':0}, {'name':'b','x':0,'y':0}, {'name':'c','x':9,'y':9}]
    #     setup_canvas2.rotate(180)
    #     print(setup_canvas2.get_points())
    #     print(Canvas(name='testCanvas', center=(5,5), points=pts_list, BL=(0,0), BR=(10,0), TL=(0,10), TR=(10,10)).get_points())
    #     # TODO: check the GT given rotation about centroid not canvas center
    #     assert setup_canvas2 == Canvas(name='testCanvas', center=(5,5), points=pts_list, BL=(0,0), BR=(10,0), TL=(0,10), TR=(10,10))

    # def test_get_angles(self, setup_canvas3):
    #     print(setup_canvas3)
    #     print(setup_canvas3.get_angles_to_T_ref())
    #     print(setup_canvas3.get_angles_to_L_ref())
    #     print(setup_canvas3.get_angles_to_TL_ref())
    #     # TODO: determine GT angles for test case
    #     assert False

