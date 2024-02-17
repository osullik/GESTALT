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

    @pytest.fixture
    def setup_canvas2(self):
        pts_list = [{'name':'a','x':5,'y':10}, {'name':'b','x':10,'y':10}, {'name':'c','x':1,'y':1}]
        test_canvas = Canvas(name="testCanvas2", center=(5,5), points=pts_list, BL=(0,0), BR=(10,0), TL=(0,10), TR=(10,10))
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
    

    def test_rotate(self, setup_canvas2):
        pts_list = [{'name':'a','x':5,'y':0}, {'name':'b','x':0,'y':0}, {'name':'c','x':9,'y':9}]
        setup_canvas2.rotate(180)
        print(setup_canvas2.get_points())
        print(Canvas(name='testCanvas', center=(5,5), points=pts_list, BL=(0,0), BR=(10,0), TL=(0,10), TR=(10,10)).get_points())

        assert setup_canvas2 == Canvas(name='testCanvas', center=(5,5), points=pts_list, BL=(0,0), BR=(10,0), TL=(0,10), TR=(10,10))



 # def test_singleRotation_multiPoints(self):

    #     self.rotate_centroid    = Point('centroid',5 ,5 )

    #     self.rotate_P1          = Point("P1",5,10)
    #     self.rotate_P2          = Point("P2",10,10)
    #     self.rotate_P3          = Point("P3",1 , 1)

    #     self.roatate_angle      = 180

    #     #P1 and Angle used from last test (5,10) and 180 Deg respectively
    #     self.rotate_P1_prime    = Point("P1",5 ,0 )
    #     self.rotate_P2_prime    = Point("P2",0, 0 )
    #     self.rotate_P3_prime    = Point("P3",9 ,9 )

    #     # Test Each individually

    #     p1_prime = self.COMPASS.rotatePoint(centroid=self.rotate_centroid, point=self.rotate_P1, angle=self.roatate_angle)
    #     for i in range (0, len(p1_prime.get_coordinates())):
    #         self.assertAlmostEqual(p1_prime.get_coordinates()[i], self.rotate_P1_prime.get_coordinates()[i], places=2)
        
    #     p2_prime = self.COMPASS.rotatePoint(centroid=self.rotate_centroid, point=self.rotate_P2, angle=self.roatate_angle)
    #     for i in range (0, len(p2_prime.get_coordinates())):
    #         self.assertAlmostEqual(p2_prime.get_coordinates()[i], self.rotate_P2_prime.get_coordinates()[i], places=2)

    #     p3_prime = self.COMPASS.rotatePoint(centroid=self.rotate_centroid, point=self.rotate_P3, angle=self.roatate_angle)
    #     for i in range (0, len(p3_prime.get_coordinates())):
    #         self.assertAlmostEqual(p3_prime.get_coordinates()[i], self.rotate_P3_prime.get_coordinates()[i], places=2)

    #     #Test batch

    #     self.rotate_list = (self.rotate_P1, self.rotate_P2, self.rotate_P3)
    #     self.rotatedList = (self.rotate_P1_prime, self.rotate_P2_prime, self.rotate_P3_prime)

    #     self.returnedRotations = self.COMPASS.rotateAllPoints(centroid=self.rotate_centroid, points=self.rotate_list, angle=self.roatate_angle)

    #     for i in range(0, len(self.returnedRotations)):
    #         for j in range (0, 2):
    #             self.assertAlmostEqual(self.returnedRotations[i].get_coordinates()[j], self.rotatedList[i].get_coordinates()[j], places=2)



    