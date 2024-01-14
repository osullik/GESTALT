#Core Python Imports
import unittest
import math

# Libarary Imports

# User class imports

from compass import Compass
from compass import Point
from compass import Canvas

# Global Vars

# Classes

class test_Points(unittest.TestCase):
    def setUp(self):
        self.testPoint = Point(name="testPoint", x_coord=0, y_coord=0)
        pass 

    def tearDown(self) -> None:
        return super().tearDown()
    
    def test_pointCreation(self):
        self.assertEqual(str(type(self.testPoint)), "<class 'compass.Point'>")

    def test_getCoords(self):
        coords = (0,0)
        self.assertEqual(self.testPoint.get_coordinates(), coords)
    
    def test_getName(self):
        name = "testPoint"
        self.assertEqual(self.testPoint.getName(), name)

    def test_dumpTuple(self):
        tuple = ("testPoint", (0,0))
    
    def test_get_point_id(self):
        test_point_00 = Point(name="test_point_00", x_coord=5, y_coord=10)
        test_point_01 = Point(name="test_point_01", x_coord=10, y_coord=15)
        self.assertTrue(test_point_00.get_point_id() == float('inf'))
        self.assertTrue(test_point_00.get_point_id() == float('inf'))
        test_point_00._set_point_id(id=0)
        test_point_01._set_point_id(id=1)
        self.assertTrue(test_point_00.get_point_id() == 0)
        self.assertTrue(test_point_01.get_point_id() == 1)

    def test_check_point_equality(self):
        test_point_00 = Point(name="test_point_00", x_coord=5, y_coord=10)
        test_point_01 = Point(name="test_point_01", x_coord=10, y_coord=15)
        test_point_02 = Point(name="test_point_00", x_coord=5, y_coord=10)
        test_point_03 = Point(name="test_point_02", x_coord=12, y_coord=13)

        self.assertFalse(test_point_00.check_point_equality(test_point_01))
        self.assertTrue(test_point_00.check_point_equality(test_point_02))
        self.assertFalse(test_point_00.check_point_equality(test_point_03))



class test_Canvas(unittest.TestCase):
    def setUp(self) -> None:
        self.canvas_name = "test_canvas"
        self.test_canvas = Canvas(canvas_name=self.canvas_name)
        self.test_point_00 = Point(name="test_point_00", x_coord=5, y_coord=10)
        self.test_point_01 = Point(name="test_point_01", x_coord=10, y_coord=15)
        return super().setUp()
    
    def tearDown(self) -> None:
        return super().tearDown()
    
    def test_canvas_exists(self):
        self.assertTrue(self.test_canvas)
    
    def test_canvas_has_name(self):
        self.assertEqual(self.test_canvas.get_name(), self.canvas_name)
    
    def test_update_canvas_name(self):
        self.assertEqual(self.test_canvas.get_name(), self.canvas_name)
        
        new_name = "new_test_canvas"
        self.test_canvas.update_name(canvas_name=new_name)
        self.assertEqual(self.test_canvas.get_name(), new_name)
    
    def test_get_canvas_boundaries(self):
        BL = Point("test_canvas_BL", 0, 0)
        TL = Point("test_canvas_TL", 0, 100)
        TR = Point("test_canvas_TR", 100, 100)
        BR = Point("test_canvas_BR", 100, 0)
        
        test_BL, test_TL, test_TR, test_BR = self.test_canvas.get_canvas_boundaries()

        reference_points = [BL, TL, TR, BR]
        test_points = [test_BL, test_TL, test_TR, test_BR]

        for i, point in enumerate(reference_points):
            self.assertTupleEqual(point.dumpTuple(), test_points[i].dumpTuple())

    def test_get_canvas_reference_points(self):
        test_canvas = Canvas("Ref_point_canvas")
        n = Point("north_ref", 50,100)
        w = Point("west_ref",0,50)
        nw = Point('northwest_ref',0,100)
        N,W,NW = test_canvas.get_canvas_reference_points()
        self.assertTrue(N.check_point_equality(n))
        self.assertTrue(W.check_point_equality(w))
        self.assertTrue(NW.check_point_equality(nw))
    
    def test_set_canvas_reference_points(self):
        n = Point("north_ref", 6,12)
        w = Point("west_ref",0,6)
        nw = Point('northwest_ref',0,12)
        test_canvas = Canvas("Ref_point_canvas")
        test_point_00 = Point("a", 1,1)
        test_point_01 = Point("b", 11,11)
        test_canvas.add_member_point(test_point_00)
        test_canvas.add_member_point(test_point_01)
        BL,TR = test_canvas.get_points_bounding_box()
        test_canvas.set_canvas_boundaries(bottom_left_corner=BL,top_right_corner=TR)
        test_canvas.set_canvas_reference_points()
        N,W,NW = test_canvas.get_canvas_reference_points()
        self.assertTrue(N.check_point_equality(n))
        self.assertTrue(W.check_point_equality(w))
        self.assertTrue(NW.check_point_equality(nw))

    def test_add_point_to_canvas(self):
        self.assertEqual(len(self.test_canvas._member_points_by_id), 0)
        self.test_canvas.add_member_point(member_point=self.test_point_00)
        self.assertEqual(len(self.test_canvas._member_points_by_id), 1)

    def test_get_points_from_canvas(self):
        self.assertEqual(len(self.test_canvas._member_points_by_id), 0)
        self.test_canvas.add_member_point(member_point=self.test_point_00)
        self.assertEqual(len(self.test_canvas._member_points_by_id), 1)
        member_points = self.test_canvas.get_member_points()
        self.assertEqual(len(member_points), 1)
        self.assertTupleEqual(member_points[0].dumpTuple(), self.test_point_00.dumpTuple())

    def test_get_member_points_using_name(self):
        self.assertEqual(len(self.test_canvas._member_points_by_id), 0)
        self.test_canvas.add_member_point(member_point=self.test_point_00)
        self.test_canvas.add_member_point(member_point=self.test_point_01)
        self.assertEqual(len(self.test_canvas._member_points_by_id), 2)
        self.assertEqual(self.test_canvas.get_member_points_using_name(name='test_point_01')[0].dumpTuple(), self.test_point_01.dumpTuple())
        #Test that multiple points of the same name are returned
        test_point_01a = Point(name="test_point_01", x_coord=12, y_coord=17)
        self.test_canvas.add_member_point(member_point=test_point_01a)
        point_list = self.test_canvas.get_member_points_using_name(name='test_point_01')
        self.assertTrue(len(point_list)==2)
        self.assertListEqual([point_list[0].dumpTuple(), point_list[1].dumpTuple()],[self.test_point_01.dumpTuple(), test_point_01a.dumpTuple()])

    def test_get_member_point_using_id(self):
        self.assertEqual(len(self.test_canvas._member_points_by_id), 0)
        self.test_canvas.add_member_point(member_point=self.test_point_00)
        self.test_canvas.add_member_point(member_point=self.test_point_01)
        self.assertEqual(len(self.test_canvas._member_points_by_id), 2)
        self.assertEqual(self.test_canvas.get_member_point_using_id(id=1).dumpTuple(), self.test_point_01.dumpTuple())

    def test_remove_point_from_canvas_by_id(self):
        self.assertEqual(len(self.test_canvas._member_points_by_id), 0)
        self.test_canvas.add_member_point(member_point=self.test_point_00)
        self.test_canvas.add_member_point(member_point=self.test_point_01)
        self.assertEqual(len(self.test_canvas._member_points_by_id), 2)
        
        self.test_canvas.remove_member_point_from_canvas_by_id(member_point_id=0)
        self.assertEqual(len(self.test_canvas._member_points_by_id), 1)
        self.assertEqual(len(self.test_canvas._member_points_by_name), 1)
        
        test_point_01a = Point(name="test_point_01", x_coord=12, y_coord=17)
        self.test_canvas.add_member_point(member_point=test_point_01a)
        self.assertEqual(len(self.test_canvas._member_points_by_name), 1)
        self.assertEqual(len(self.test_canvas._member_points_by_name['test_point_01']), 2)
        self.assertEqual(len(self.test_canvas._member_points_by_id), 2)
       
        self.test_canvas.remove_member_point_from_canvas_by_id(member_point_id=2)
        self.assertEqual(len(self.test_canvas._member_points_by_name), 1)
        self.assertEqual(len(self.test_canvas._member_points_by_name['test_point_01']), 1)
        self.assertEqual(len(self.test_canvas._member_points_by_id), 1)
        
    def test_remove_point_from_canvas_by_name(self):
        self.assertEqual(len(self.test_canvas._member_points_by_id), 0)
        self.test_canvas.add_member_point(member_point=self.test_point_00)
        self.test_canvas.add_member_point(member_point=self.test_point_01)
        self.assertEqual(len(self.test_canvas._member_points_by_id), 2)
        
        self.test_canvas.remove_member_point_from_canvas_by_name(member_point_name='test_point_00')
        self.assertEqual(len(self.test_canvas._member_points_by_id), 1)
        self.assertEqual(len(self.test_canvas._member_points_by_name), 1)
        
        test_point_01a = Point(name="test_point_01", x_coord=12, y_coord=17)
        self.test_canvas.add_member_point(member_point=test_point_01a)
        self.assertEqual(len(self.test_canvas._member_points_by_name), 1)
        self.assertEqual(len(self.test_canvas._member_points_by_name['test_point_01']), 2)
        self.assertEqual(len(self.test_canvas._member_points_by_id), 2)
       
        self.test_canvas.remove_member_point_from_canvas_by_name(member_point_name='test_point_01')
        self.assertEqual(len(self.test_canvas._member_points_by_name), 0)
        self.assertEqual(self.test_canvas.get_member_points_using_name(name='test_point_01'), [])
        self.assertEqual(len(self.test_canvas._member_points_by_id), 0)
        
    def test_get_points_bounding_box(self):

        #Null Bounding Box
        LL = (0,0)
        TR = (0,0)
        self.assertListEqual(self.test_canvas.get_points_bounding_box(),[LL,TR])

        #Single Point Bounding Box
        test_point_00 = Point("test_point_00",5,5)
        self.test_canvas.add_member_point(test_point_00)
        LL = (4,4)
        TR = (6,6)
        self.assertListEqual(self.test_canvas.get_points_bounding_box(),[LL,TR])

        #Multi Point Bounding Box
        test_point_01 = Point("test_point_01",10,10)
        self.test_canvas.add_member_point(test_point_01)
        LL = (4,4)
        TR = (11,11)
        self.assertListEqual(self.test_canvas.get_points_bounding_box(),[LL,TR])


class test_Compass(unittest.TestCase):

    def setUp(self):
        self.canvas_name = "test_canvas"
        self.test_canvas_00 = Canvas(canvas_name=self.canvas_name)
        self.test_point_00 = Point(name="a", x_coord=5, y_coord=5)
        self.test_point_01 = Point(name="b", x_coord=0, y_coord=5)
        self.test_point_02 = Point(name='c', x_coord=10,y_coord=5)
        self.test_point_03 = Point(name='d', x_coord=5,y_coord=0)
        self.test_point_04 = Point(name='e', x_coord=5,y_coord=10)
        self.test_point_05 = Point(name='f', x_coord=0,y_coord=0)
        self.test_point_06 = Point(name='g', x_coord=0,y_coord=9)
        self.test_point_07 = Point(name='h', x_coord=9,y_coord=0)
        self.test_point_08 = Point(name='i', x_coord=0,y_coord=10)
        self.test_point_09 = Point(name='j', x_coord=10,y_coord=0)
        self.test_point_10 = Point(name='k', x_coord=10,y_coord=10)

        self.COMPASS = Compass()

        #Vars for test_angles
        self.referencePoint = Point("north", 5,10)
        self.singlePoint = Point("a", 5,5)
        self.singlePointCentrid = Point("centroid",5,5)
        self.singlePointAngle = 90

    def tearDown(self) -> None:
        return super().tearDown()

    #Get Centroid
    def test_Centroids(self):
        #Single Point
        singlePoint_answer = Point("centroid",5,5)
        self.test_canvas_00.add_member_point(member_point=self.test_point_00)
        centroid = self.COMPASS.get_points_centroid(canvas=self.test_canvas_00)
        self.assertTrue(centroid.check_point_equality(singlePoint_answer))
        
        #Two Points (x axis)
        twoPointsX_answer = Point("centroid",5,5)
        self.test_canvas_00.remove_member_point_from_canvas_by_name(member_point_name='a')
        self.test_canvas_00.add_member_point(member_point=self.test_point_01)
        self.test_canvas_00.add_member_point(member_point=self.test_point_02)
        centroid = self.COMPASS.get_points_centroid(canvas=self.test_canvas_00)
        self.assertTrue(centroid.check_point_equality(twoPointsX_answer))

        #Two Points (y axis)
        twoPointsY_answer = Point("centroid",5,5)
        self.test_canvas_00.remove_member_point_from_canvas_by_name(member_point_name='b')
        self.test_canvas_00.remove_member_point_from_canvas_by_name(member_point_name='c')
        self.test_canvas_00.add_member_point(member_point=self.test_point_03)
        self.test_canvas_00.add_member_point(member_point=self.test_point_04)
        centroid = self.COMPASS.get_points_centroid(canvas=self.test_canvas_00)
        self.assertTrue(centroid.check_point_equality(twoPointsY_answer))

        #Three Points
        threePoints_answer = Point("centroid", 4.5, 4.5)
        self.test_canvas_00.remove_member_point_from_canvas_by_name(member_point_name='d')
        self.test_canvas_00.remove_member_point_from_canvas_by_name(member_point_name='e')
        self.test_canvas_00.add_member_point(member_point=self.test_point_05)
        self.test_canvas_00.add_member_point(member_point=self.test_point_06)
        self.test_canvas_00.add_member_point(member_point=self.test_point_07)
        centroid = self.COMPASS.get_points_centroid(canvas=self.test_canvas_00)
        self.assertTrue(centroid.check_point_equality(threePoints_answer))

        #Four Points:
        fourPoints_answer = Point("centroid", 5,5)
        self.test_canvas_00.remove_member_point_from_canvas_by_name(member_point_name='g')
        self.test_canvas_00.remove_member_point_from_canvas_by_name(member_point_name='h')
        self.test_canvas_00.add_member_point(member_point=self.test_point_08)
        self.test_canvas_00.add_member_point(member_point=self.test_point_09)
        self.test_canvas_00.add_member_point(member_point=self.test_point_10)
        centroid = self.COMPASS.get_points_centroid(canvas=self.test_canvas_00)
        self.assertTrue(centroid.check_point_equality(fourPoints_answer))


    #Get angle between each point, the centroid and the north point. 
    #
    #       N\
    #        \z\ 
    #         \  \
    #          \   \
    #           \    \
    #            \   y P
    #             \x / 
    #              C
    #
    #       Look for angle x [NCP]          
    #

    def test_getSideLength(self):

        #
        # 5     N
        # 4    |z \
        # 3    |   \   c
        # 2  p |    \
        # 1    |x   y\
        # 0     C --- P
        #         n
        #       012345

        N = Point("north",0,5)
        C = Point("centroid",0,0)
        P = Point("P", 5,0)
        n = 5
        p = 5
        c = math.sqrt(50)

        self.assertEqual(self.COMPASS.getSideLength(C, N), p)
        self.assertEqual(self.COMPASS.getSideLength(N, P), c)
        self.assertEqual(self.COMPASS.getSideLength(C, P), n)

    def test_getReferencePoints(self):

        test_canvas = Canvas(canvas_name="test_reference_points_canvas")
        test_point_00 = Point("a",1,1)
        test_point_01 = Point("b",11,11)
        test_canvas.add_member_point(test_point_00)
        test_canvas.add_member_point(test_point_01)
        BL,TR = test_canvas.get_points_bounding_box()
        test_canvas.set_canvas_boundaries(bottom_left_corner=BL, top_right_corner=TR)
        northRef    = Point("north",6 ,12)
        westRef     = Point("west",0, 6 )
        norWestRef  = Point("northwest",0, 12)

        referenceList = [northRef, westRef, norWestRef]
        referencePointsList = self.COMPASS.getReferencePoints(canvas=test_canvas)

        for i, ref in enumerate(referenceList):
            self.assertTrue(referencePointsList[i].check_point_equality(referenceList[i]))

    def test_angle(self):

    #     #
    #     # 5     N
    #     # 4    |z\
    #     # 3    |  \   c
    #     # 2  p |   \
    #     # 1    |x  y\
    #     # 0     C --- P
    #     #         n
    #     #      012345

        test_angle_canvas = Canvas("test_angle_canvas")
        small_point = Point('P',5,0)
        test_angle_canvas.add_member_point(small_point)
        test_angle_canvas._canvas_centroid = Point('centroid',0,0)
        test_angle_canvas.north_ref = Point('north',0,5)
        small_x = 90
        small_y = 45
        small_z = 45

        self.assertEqual(self.COMPASS.getAngle(canvas=test_angle_canvas, reference='north', point=small_point), small_x)

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

        test_angle_canvas2 = Canvas("test_angle_canvas2")
        small_point2 = Point('P2',0,0)
        test_angle_canvas2.add_member_point(small_point)
        test_angle_canvas2._canvas_centroid = Point('centroid2',5,0)
        test_angle_canvas2.north_ref = Point('north2',5,5)
        small_x2 = 270

        self.assertEqual(self.COMPASS.getAngle(canvas=test_angle_canvas2, reference='north',point=small_point2), small_x2)


    # get the angles for all points

    def test_getMultipleAngles(self):

        #
        # 5       / N --- P2
        # 4      /  | \x2  |
        # 3   c2/   |  \c1 |
        # 2    /  p |   \  |
        # 1   /     |x1  \ |
        # 0  P3 --- C --- P1
        #       n2  x3 n1
        #    0 123456789 10


        # multi_N  = Point('north', 5 ,5)
        # multi_C  = Point('centroid',5 ,0)
        test_multi_angle_canvas = Canvas("test_multi_angle")
        multi_P1 = Point('P1', 10,0 )
        multi_P2 = Point('P2', 10,5 )
        multi_P3 = Point('P3', 0 ,0 )
        test_multi_angle_canvas.add_member_point(multi_P1)
        test_multi_angle_canvas.add_member_point(multi_P2)
        test_multi_angle_canvas.add_member_point(multi_P3)
        BL, TR = test_multi_angle_canvas.get_points_bounding_box()
        test_multi_angle_canvas.set_canvas_boundaries(bottom_left_corner=BL, top_right_corner=TR)
        test_multi_angle_canvas.set_canvas_reference_points()
        test_multi_angle_canvas._canvas_centroid = Point("centroid",5,0)

        multi_x1 = 90
        multi_x2 = 45
        multi_x3 = 270

        #Check each works individually
        self.assertAlmostEqual(self.COMPASS.getAngle(canvas=test_multi_angle_canvas, reference='north', point=multi_P1), multi_x1, places=2)
        self.assertAlmostEqual(self.COMPASS.getAngle(canvas=test_multi_angle_canvas, reference='north', point=multi_P2), multi_x2, places=2)
        self.assertAlmostEqual(self.COMPASS.getAngle(canvas=test_multi_angle_canvas, reference='north', point=multi_P3),multi_x3, places=2)

        #Check as a list:

        multi_point_list = [multi_P1, multi_P2, multi_P3]
        multi_angle_list = [multi_x1, multi_x2, multi_x3]

        returnedAngles = self.COMPASS.getAllAngles(canvas=test_multi_angle_canvas, reference='north')

        for i in range(0, len(returnedAngles)):
            self.assertAlmostEqual(returnedAngles[i], multi_angle_list[i], places=2)

    def test_getAllAngles(self):
        #TODO: Extend the angles calculation to use the Canvas for the centroid and references
        #
        # 10  NW    N
        # 9  |\ \  | \
        # 8  | \  \|  \
        # 7  |  \  | \ \
        # 6  |   \ |   \\
        # 5  W-----C-----P1
        # 4
        # 3
        # 2
        # 1
        # 0   
        #    0 123456789 10

        canvas_all_angles_all_refs = Canvas(canvas_name="all_angles_all_refs")

        multi_N  = Point('north', 5 ,10 )
        multi_W  = Point('west',  0 ,5 )
        multi_NW = Point('northwest', 0, 10)
        multi_refs = [multi_N, multi_W, multi_NW]
        multi_C  = Point('centroid',5 ,5 )
        multi_P1 = Point('P1',10,5 )

        angle_N_C_P1 = 90
        angle_W_C_P1 = 180
        angle_NW_C_P1 = 135

        angles = [angle_N_C_P1, angle_W_C_P1, angle_NW_C_P1]

        angles = self.COMPASS.getAnglesAllRefs(centroid = multi_C, references=multi_refs, point=multi_P1)

        for i in range (0, len(angles)):
            self.assertAlmostEqual(angles[i], angles[i], places=2)

    # def test_getAllAnglesAllRefsAllPoints(self):

    #     #
    #     # 10  NW    N
    #     # 9  |\ \\ ||\
    #     # 8  | \ \\| |\
    #     # 7  |  \ \| \ \
    #     # 6  |   \ |  |\\
    #     # 5  W-----C-----P1
    #     # 4    \    \\ |
    #     # 3       \  \\ |
    #     # 2          \\\ |
    #     # 1            \\ | 
    #     # 0              P2
    #     #    0 123456789 10

    #     self.multi_N  = Point('north', 5 ,10 )
    #     self.multi_W  = Point('west',  0 ,5 )
    #     self.multi_NW = Point('northwest', 0, 10)
    #     self.multi_refs = [self.multi_N, self.multi_W, self.multi_NW]
    #     self.multi_C  = Point('centroid',5 ,5 )
    #     self.multi_P1 = Point('P1',10,5 )
    #     self.multi_P2 = Point('P2',10,0 )
    #     self.multi_points = [self.multi_P1, self.multi_P2]

    #     self.angle_N_C_P1 = 90
    #     self.angle_W_C_P1 = 180
    #     self.angle_NW_C_P1 = 135

    #     self.angle_N_C_P2 = 135
    #     self.angle_W_C_P2 = 225
    #     self.angle_NW_C_P2 = 180
    #     self.angles = [self.angle_N_C_P1, self.angle_W_C_P1, self.angle_NW_C_P1, self.angle_N_C_P2, self.angle_W_C_P2, self.angle_NW_C_P2]


    #     angles = self.COMPASS.getAnglesAllRefsAllPoints(centroid = self.multi_C, references=self.multi_refs, points=self.multi_points)


    # def test_singleRotation(self):

    #     self.rotate_centroid    = Point('centroid',5 ,5 )
    #     self.rotate_P1          = Point('P1',5,10)
    #     self.roatate_angle      = 180
    #     self.rotate_P1_prime    = Point("P1",5 ,0 )

    #     self.rotate_P2          =Point("P2", 0, 0)
    #     self.roatate_angle_P2   =225
    #     self.rotate_P2_prime    =Point("P2",5, 5+5*math.sqrt(2))

    #     p1_prime = self.COMPASS.rotatePoint(centroid=self.rotate_centroid, point=self.rotate_P1, angle=self.roatate_angle)
    #     p2_prime = self.COMPASS.rotatePoint(centroid=self.rotate_centroid, point=self.rotate_P2, angle=self.roatate_angle_P2)


    #     for i in range (0, len(p1_prime.get_coordinates())):
    #         self.assertAlmostEqual(p1_prime.get_coordinates()[i], self.rotate_P1_prime.get_coordinates()[i], places=2)

    #     for i in range (0, len(p2_prime.get_coordinates())):
    #         self.assertAlmostEqual(p2_prime.get_coordinates()[i], self.rotate_P2_prime.get_coordinates()[i], places=2)

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


    # def test_multiRotation(self):

    #     self.multi_rotate_centroid    = Point('centroid',5 ,5 )
    #     self.multi_rotate_P1          = Point('P1',5 ,10)
    #     self.multi_roatate_angle_1    = 90
    #     self.multi_roatate_angle_2    = 90
    #     self.multi_rotate_P1_prime_1  = Point('P1',0, 5 )
    #     self.multi_rotate_P1_prime_2  = Point('P1',5 ,0 )

    #     #Test Individually
    #     p1_prime_1 = self.COMPASS.rotatePoint(centroid=self.multi_rotate_centroid, point=self.multi_rotate_P1, angle=self.multi_roatate_angle_1)

    #     for i in range (0, len(p1_prime_1.get_coordinates())):
    #         self.assertAlmostEqual(p1_prime_1.get_coordinates()[i], self.multi_rotate_P1_prime_1.get_coordinates()[i], places=2)

    #     p1_prime_2 = self.COMPASS.rotatePoint(centroid=self.multi_rotate_centroid, point=p1_prime_1, angle=self.multi_roatate_angle_2)
    #     for i in range (0, len(p1_prime_2.get_coordinates())):
    #         self.assertAlmostEqual(p1_prime_2.get_coordinates()[i], self.multi_rotate_P1_prime_2.get_coordinates()[i], places=2)

        
    #     #Test_batch

    #     self.multi_rotate_P2          = Point('P2',10 ,5)
    #     self.multi_rotate_P2_prime_1  = Point('P2',5, 10 )
    #     self.multi_rotate_P2_prime_2  = Point('P2',0 ,5 )


    #     self.multi_points_list = [self.multi_rotate_P1, self.multi_rotate_P2]
    #     self.multi_angles_list = [self.multi_roatate_angle_1, self.multi_roatate_angle_2]

    #     resultsList = [[self.multi_rotate_P1, self.multi_rotate_P2], [self.multi_rotate_P1_prime_1, self.multi_rotate_P2_prime_1], [self.multi_rotate_P1_prime_2, self.multi_rotate_P2_prime_2],]

    #     rotationSets = self.COMPASS.multiRotatePoints(centroid=self.multi_rotate_centroid, points=self.multi_points_list, angles=self.multi_angles_list, rotateFromBlank=False)

    #     for i in range(0, len(resultsList)):
    #         for j in range(0, len(resultsList[i])):
    #             for k in range(0, len(resultsList[i][j].get_coordinates())):
    #                 self.assertAlmostEqual(rotationSets[i][j].get_coordinates()[k], resultsList[i][j].get_coordinates()[k], places=2)


    # def test_getAllRotations(self):

    #     point_a = Point("a", 0 ,0 )
    #     point_b = Point("b", 10, 10)
    #     test_canvas = Canvas(canvas_name="test_canvas")
    #     test_canvas.add_member_point(point_a)
    #     test_canvas.add_member_point(point_b)


    #     LL, TR, centroid = self.COMPASS.getCentroid(test_canvas)
    #     referencePoints = self.COMPASS.getReferencePoints(canvas=test_canvas)
        
    #     angles = self.COMPASS.getAnglesAllRefsAllPoints(centroid=centroid, references=referencePoints, points=test_canvas.get_member_points())

    #     states = []

    #     self.states = [[(0,0), (10,10)],[(5,12), (5,-2)], [(-2,5), (12,5)], [(0,10), (10,0)], [(5,-2), (5,12)], [(12,5),(-2,5)],[(10,0),(0,10)]]                  

    #     states = self.COMPASS.multiRotatePoints(centroid=centroid, points=test_canvas.get_member_points(), angles=angles, rotateFromBlank=True)

    #     for i in range(0, len(states)):
    #         for j in range(0,len(states[i])):
                
    #             for k in range(0, len(states[i][j].get_coordinates())):
    #                 self.assertAlmostEqual(round(states[i][j].get_coordinates()[k]), round(self.states[i][j][k]),places=0)

    # def test_uniqueStates(self):

    #     self.duplicatedStates = [
    #                             [Point('a',0,0),Point('b',10,10)],
    #                             [Point('a',0,0),Point('b',10,10)],
    #                             [Point('a',0,0),Point('b',10,10)],
    #                             [Point('a',5,12),Point('b',5,-2)],
    #                             [Point('a',-2,5),Point('b',12,5)],
    #                             [Point('a',0,10),Point('b',10,0)],
    #                             [Point('a',5,-2),Point('b',5,12)],
    #                             [Point('a',5,-2),Point('b',5,12)],
    #                             [Point('a',12,5),Point('b',-2,5)],
    #                             [Point('a',12,5),Point('b',-2,5)],
    #                             [Point('a',10,0),Point('b',0,10)] 
    #                             ]

    #     self.uniqueStates = set((
    #                                 frozenset((('a',(0,0)),('b',(10,10)))),
    #                                 frozenset((('a',(5,12)),('b',(5,-2)))),
    #                                 frozenset((('a',(-2,5)),('b',(12,5)))),
    #                                 frozenset((('a',(0,10)),('b',(10,0)))),
    #                                 frozenset((('a',(5,-2)),('b',(5,12)))),
    #                                 frozenset((('a',(12,5)),('b',(-2,5)))),
    #                                 frozenset((('a',(10,0)),('b',(0,10))))     
    #                         ))
    
    #     uniqueStates = self.COMPASS.getUniqueStates(states=self.duplicatedStates)

    #     self.assertSetEqual(uniqueStates, self.uniqueStates)
        
    
    # def test_generateRotations(self):

    #     point_a = Point("a", 0 ,0 )
    #     point_b = Point("b", 10, 10)
    #     test_canvas = Canvas(canvas_name="test_canvas")
    #     test_canvas.add_member_point(point_a)
    #     test_canvas.add_member_point(point_b)

    #     self.uniqueRotations = set((
    #                                 frozenset((('a',(0,0)),('b',(10,10)))),
    #                                 frozenset((('a',(5,12)),('b',(5,-2)))),
    #                                 frozenset((('a',(-2,5)),('b',(12,5)))),
    #                                 frozenset((('a',(0,10)),('b',(10,0)))),
    #                                 frozenset((('a',(5,-2)),('b',(5,12)))),
    #                                 frozenset((('a',(12,5)),('b',(-2,5)))),
    #                                 frozenset((('a',(10,0)),('b',(0,10))))     
    #                         ))
        
    #     rotatedStates = self.COMPASS.generateRotations(canvas=test_canvas, alignToIntegerGrid=True)



# Main Function

if __name__ == '__main__':
    unittest.main()
