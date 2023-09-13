#Core Python Imports
import unittest
import math

# Libarary Imports

# User class imports

from compass import Compass
from compass import Point

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
        self.assertEqual(self.testPoint.getCoordinates(), coords)
    
    def test_getName(self):
        name = "testPoint"
        self.assertEqual(self.testPoint.getName(), name)

class test_Compass(unittest.TestCase):

    def setUp(self):
        
        self.COMPASS = Compass()

        #Vars for test_centroid
        self.singlePoint_problem = [Point("a",5,5)]
        self.singlePoint_answer = Point("centroid",5,5)

        self.twoPointsX_problem = [Point("a",0,5), Point("b",10,5)]
        self.twoPointsX_answer = Point("centroid",5,5)

        self.twoPointsY_problem = [Point("a",5,0), Point("b",5,10)]
        self.twoPointsY_answer = Point("centroid",5,5)

        self.threePoints_problem = [Point("a",0,0), Point("b",0,9), Point("c",9,0)]
        self.threePoints_answer = Point("centroid", 4.5, 4.5)

        self.fourPoints_problem = [Point("a",0,0), Point("b",0,10), Point("c",10,0), Point("d",10,10)]
        self.fourPoints_answer = Point("centroid", 5,5)

        #Vars for test_angles
        self.referencePoint = Point("north", 5,10)
        self.singlePoint = Point("a", 5,5)
        self.singlePointCentrid = Point("centroid",5,5)
        self.singlePointAngle = 90

        

    def tearDown(self):
        pass

    #Get Centroid
    def test_Centroids(self):
        self.assertEqual(self.COMPASS.getCentroid(self.singlePoint_problem)[2].getName(), self.singlePoint_answer.getName())
        self.assertEqual(self.COMPASS.getCentroid(self.singlePoint_problem)[2].getCoordinates(), self.singlePoint_answer.getCoordinates())

        self.assertEqual(self.COMPASS.getCentroid(self.twoPointsX_problem)[2].getName(), self.twoPointsX_answer.getName())
        self.assertEqual(self.COMPASS.getCentroid(self.twoPointsX_problem)[2].getCoordinates(), self.twoPointsX_answer.getCoordinates())

        self.assertEqual(self.COMPASS.getCentroid(self.twoPointsY_problem)[2].getName(), self.twoPointsY_answer.getName())
        self.assertEqual(self.COMPASS.getCentroid(self.twoPointsY_problem)[2].getCoordinates(), self.twoPointsY_answer.getCoordinates())

        self.assertEqual(self.COMPASS.getCentroid(self.threePoints_problem)[2].getName(), self.threePoints_answer.getName())
        self.assertEqual(self.COMPASS.getCentroid(self.threePoints_problem)[2].getCoordinates(), self.threePoints_answer.getCoordinates())

        self.assertEqual(self.COMPASS.getCentroid(self.fourPoints_problem)[2].getName(), self.fourPoints_answer.getName())
        self.assertEqual(self.COMPASS.getCentroid(self.fourPoints_problem)[2].getCoordinates(), self.fourPoints_answer.getCoordinates())


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

        self.N = Point("north",0,5)
        self.C = Point("centroid",0,0)
        self.P = Point("P", 5,0)
        self.n = 5
        self.p = 5
        self.c = math.sqrt(50)

        self.assertEqual(self.COMPASS.getSideLength(self.C, self.N), self.p)
        self.assertEqual(self.COMPASS.getSideLength(self.N, self.P), self.c)
        self.assertEqual(self.COMPASS.getSideLength(self.C, self.P), self.n)

    def test_getReferencePoints(self):

        centroid    = Point("centroid",5 ,5 )
        boundingBox = [Point("BL",0,0), Point("TR",10,10)]
        northRef    = Point("north",5 ,10)
        westRef     = Point("west",0, 5 )
        norWestRef  = Point("northwest",0, 10)

        referenceList = [northRef, westRef, norWestRef]
        referencePointsList = self.COMPASS.getReferencePoints(boundingBox=boundingBox, centroid=centroid)

        for i in range(0, len(referenceList)):
            self.assertEqual(referencePointsList[i].getName(),referenceList[i].getName())
            self.assertEqual(referencePointsList[i].getCoordinates(), referenceList[i].getCoordinates())



    def test_angle(self):

        #
        # 5     N
        # 4    |z\
        # 3    |  \   c
        # 2  p |   \
        # 1    |x  y\
        # 0     C --- P
        #         n
        #      012345

        self.small_centroid = Point('centroid',0,0)
        self.small_point = Point('P',5,0)
        self.small_northReference = Point('north',0,5)
        self.small_x = 90
        self.small_y = 45
        self.small_z = 45

        self.assertEqual(self.COMPASS.getAngle(reference=self.small_northReference, centroid=self.small_centroid, point=self.small_point), self.small_x)

        # Test we get external angle of rotation when required

        #
        # 5           N
        # 4         / |
        # 3        /  |
        # 2     c /   | p
        # 1      /    |
        # 0     P --- C
        #          n   (x)
        #        012345

        self.small_centroid2 = Point('centroid2',5,0)
        self.small_point2 = Point('P2',0,0)
        self.small_northReference2 = Point('north2',5,5)
        self.small_x2 = 270

        self.assertEqual(self.COMPASS.getAngle(reference=self.small_northReference2, centroid=self.small_centroid2, point=self.small_point2), self.small_x2)


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


        self.multi_N  = Point('north', 5 ,5 )
        self.multi_C  = Point('centroid',5 ,0 )
        self.multi_P1 = Point('P1', 10,0 )
        self.multi_P2 = Point('P2', 10,5 )
        self.multi_P3 = Point('P3', 0 ,0 )

        self.multi_x1 = 90
        self.multi_x2 = 45
        self.multi_x3 = 270

        #Check each works individually
        self.assertAlmostEqual(self.COMPASS.getAngle(reference=self.multi_N, centroid=self.multi_C, point=self.multi_P1), self.multi_x1, places=2)
        self.assertAlmostEqual(self.COMPASS.getAngle(reference=self.multi_N, centroid=self.multi_C, point=self.multi_P2), self.multi_x2, places=2)
        self.assertAlmostEqual(self.COMPASS.getAngle(reference=self.multi_N, centroid=self.multi_C, point=self.multi_P3), self.multi_x3, places=2)

        #Check as a list:

        self.multi_point_list = [self.multi_P1, self.multi_P2, self.multi_P3]
        self.multi_angle_list = [self.multi_x1, self.multi_x2, self.multi_x3]

        returnedAngles = self.COMPASS.getAllAngles(reference=self.multi_N, centroid=self.multi_C, points=self.multi_point_list)

        for i in range(0, len(returnedAngles)):
            self.assertAlmostEqual(returnedAngles[i], self.multi_angle_list[i], places=2)

    def test_getAllAngles(self):

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

        self.multi_N  = Point('north', 5 ,10 )
        self.multi_W  = Point('west',  0 ,5 )
        self.multi_NW = Point('northwest', 0, 10)
        self.multi_refs = [self.multi_N, self.multi_W, self.multi_NW]
        self.multi_C  = Point('centroid',5 ,5 )
        self.multi_P1 = Point('P1',10,5 )

        self.angle_N_C_P1 = 90
        self.angle_W_C_P1 = 180
        self.angle_NW_C_P1 = 135

        self.angles = [self.angle_N_C_P1, self.angle_W_C_P1, self.angle_NW_C_P1]

        angles = self.COMPASS.getAnglesAllRefs(centroid = self.multi_C, references=self.multi_refs, point=self.multi_P1)

        for i in range (0, len(angles)):
            self.assertAlmostEqual(angles[i], self.angles[i], places=2)

    def test_getAllAnglesAllRefsAllPoints(self):

        #
        # 10  NW    N
        # 9  |\ \\ ||\
        # 8  | \ \\| |\
        # 7  |  \ \| \ \
        # 6  |   \ |  |\\
        # 5  W-----C-----P1
        # 4    \    \\ |
        # 3       \  \\ |
        # 2          \\\ |
        # 1            \\ | 
        # 0              P2
        #    0 123456789 10

        self.multi_N  = Point('north', 5 ,10 )
        self.multi_W  = Point('west',  0 ,5 )
        self.multi_NW = Point('northwest', 0, 10)
        self.multi_refs = [self.multi_N, self.multi_W, self.multi_NW]
        self.multi_C  = Point('centroid',5 ,5 )
        self.multi_P1 = Point('P1',10,5 )
        self.multi_P2 = Point('P2',10,0 )
        self.multi_points = [self.multi_P1, self.multi_P2]

        self.angle_N_C_P1 = 90
        self.angle_W_C_P1 = 180
        self.angle_NW_C_P1 = 135

        self.angle_N_C_P2 = 135
        self.angle_W_C_P2 = 225
        self.angle_NW_C_P2 = 180
        self.angles = [self.angle_N_C_P1, self.angle_W_C_P1, self.angle_NW_C_P1, self.angle_N_C_P2, self.angle_W_C_P2, self.angle_NW_C_P2]


        angles = self.COMPASS.getAnglesAllRefsAllPoints(centroid = self.multi_C, references=self.multi_refs, points=self.multi_points)


    def test_singleRotation(self):

        self.rotate_centroid    = Point('centroid',5 ,5 )
        self.rotate_P1          = Point('P1',5,10)
        self.roatate_angle      = 180
        self.rotate_P1_prime    = Point("P1`",5 ,0 )

        self.rotate_P2          =Point("P2", 0, 0)
        self.roatate_angle_P2   =225
        self.rotate_P2_prime    =Point("P2`",5, 5+5*math.sqrt(2))

        p1_prime = self.COMPASS.rotatePoint(centroid=self.rotate_centroid, point=self.rotate_P1, angle=self.roatate_angle)
        p2_prime = self.COMPASS.rotatePoint(centroid=self.rotate_centroid, point=self.rotate_P2, angle=self.roatate_angle_P2)


        for i in range (0, len(p1_prime.getCoordinates())):
            self.assertAlmostEqual(p1_prime.getCoordinates()[i], self.rotate_P1_prime.getCoordinates()[i], places=2)

        for i in range (0, len(p2_prime.getCoordinates())):
            self.assertAlmostEqual(p2_prime.getCoordinates()[i], self.rotate_P2_prime.getCoordinates()[i], places=2)

    def test_singleRotation_multiPoints(self):

        self.rotate_centroid    = Point('centroid',5 ,5 )

        self.rotate_P1          = Point("P1",5,10)
        self.rotate_P2          = Point("P2",10,10)
        self.rotate_P3          = Point("P3",1 , 1)

        self.roatate_angle      = 180

        #P1 and Angle used from last test (5,10) and 180 Deg respectively
        self.rotate_P1_prime    = Point("P1`",5 ,0 )
        self.rotate_P2_prime    = Point("P2`",0, 0 )
        self.rotate_P3_prime    = Point("P3`",9 ,9 )

        # Test Each individually

        p1_prime = self.COMPASS.rotatePoint(centroid=self.rotate_centroid, point=self.rotate_P1, angle=self.roatate_angle)
        for i in range (0, len(p1_prime.getCoordinates())):
            self.assertAlmostEqual(p1_prime.getCoordinates()[i], self.rotate_P1_prime.getCoordinates()[i], places=2)
        
        p2_prime = self.COMPASS.rotatePoint(centroid=self.rotate_centroid, point=self.rotate_P2, angle=self.roatate_angle)
        for i in range (0, len(p2_prime.getCoordinates())):
            self.assertAlmostEqual(p2_prime.getCoordinates()[i], self.rotate_P2_prime.getCoordinates()[i], places=2)

        p3_prime = self.COMPASS.rotatePoint(centroid=self.rotate_centroid, point=self.rotate_P3, angle=self.roatate_angle)
        for i in range (0, len(p3_prime.getCoordinates())):
            self.assertAlmostEqual(p3_prime.getCoordinates()[i], self.rotate_P3_prime.getCoordinates()[i], places=2)

        #Test batch

        self.rotate_list = (self.rotate_P1, self.rotate_P2, self.rotate_P3)
        self.rotatedList = (self.rotate_P1_prime, self.rotate_P2_prime, self.rotate_P3_prime)

        self.returnedRotations = self.COMPASS.rotateAllPoints(centroid=self.rotate_centroid, points=self.rotate_list, angle=self.roatate_angle)

        for i in range(0, len(self.returnedRotations)):
            for j in range (0, 2):
                self.assertAlmostEqual(self.returnedRotations[i].getCoordinates()[j], self.rotatedList[i].getCoordinates()[j], places=2)


    def test_multiRotation(self):

        self.multi_rotate_centroid    = Point('centroid',5 ,5 )
        self.multi_rotate_P1          = Point('P1',5 ,10)
        self.multi_roatate_angle_1    = 90
        self.multi_roatate_angle_2    = 90
        self.multi_rotate_P1_prime_1  = Point('P1`',0, 5 )
        self.multi_rotate_P1_prime_2  = Point('P1``',5 ,0 )

        #Test Individually
        p1_prime_1 = self.COMPASS.rotatePoint(centroid=self.multi_rotate_centroid, point=self.multi_rotate_P1, angle=self.multi_roatate_angle_1)

        for i in range (0, len(p1_prime_1.getCoordinates())):
            self.assertAlmostEqual(p1_prime_1.getCoordinates()[i], self.multi_rotate_P1_prime_1.getCoordinates()[i], places=2)

        p1_prime_2 = self.COMPASS.rotatePoint(centroid=self.multi_rotate_centroid, point=p1_prime_1, angle=self.multi_roatate_angle_2)
        for i in range (0, len(p1_prime_2.getCoordinates())):
            self.assertAlmostEqual(p1_prime_2.getCoordinates()[i], self.multi_rotate_P1_prime_2.getCoordinates()[i], places=2)

        
        #Test_batch

        self.multi_rotate_P2          = Point('P2',10 ,5)
        self.multi_rotate_P2_prime_1  = Point('P2`',5, 10 )
        self.multi_rotate_P2_prime_2  = Point('P2``',0 ,5 )


        self.multi_points_list = [self.multi_rotate_P1, self.multi_rotate_P2]
        self.multi_angles_list = [self.multi_roatate_angle_1, self.multi_roatate_angle_2]

        resultsList = [[self.multi_rotate_P1, self.multi_rotate_P2], [self.multi_rotate_P1_prime_1, self.multi_rotate_P2_prime_1], [self.multi_rotate_P1_prime_2, self.multi_rotate_P2_prime_2],]

        rotationSets = self.COMPASS.multiRotatePoints(centroid=self.multi_rotate_centroid, points=self.multi_points_list, angles=self.multi_angles_list, rotateFromBlank=False)

        for i in range(0, len(resultsList)):
            for j in range(0, len(resultsList[i])):
                for k in range(0, len(resultsList[i][j].getCoordinates())):
                    self.assertAlmostEqual(rotationSets[i][j].getCoordinates()[k], resultsList[i][j].getCoordinates()[k], places=2)


    def test_getAllRotations(self):

        point_a = Point("a", 0 ,0 )
        point_b = Point("b", 10, 10)
        twoPoints = [point_a, point_b]


        LL, TR, centroid = self.COMPASS.getCentroid(twoPoints)
        referencePoints = self.COMPASS.getReferencePoints(boundingBox=[LL,TR], centroid=centroid)
        
        angles = self.COMPASS.getAnglesAllRefsAllPoints(centroid=centroid, references=referencePoints, points=twoPoints)

        states = []
        #for angle in angles:
        #    states.append(self.COMPASS.rotateAllPoints(centroid=centroid, points=twoPoints, angle=angle))

        
        self.states = [[(0,0), (10,10)],[(5,10), (5,0)], [(0,5), (10,5)], [(0,10), (10,0)], [(5,0), (5,10)], [(10,5),(0,5)],[(10,0),(0,10)]]

        states = self.COMPASS.multiRotatePoints(centroid=centroid, points=twoPoints, angles=angles, rotateFromBlank=True)

        #print("BOUNDING BOX:", LL.getCoordinates(), TR.getCoordinates())
        #print("CENTROID:", centroid.getCoordinates())
        #print("NORTH", referencePoints[0].getCoordinates())
        #print("WEST", referencePoints[1].getCoordinates())
        #print("NORTHWEST", referencePoints[2].getCoordinates())
        #print("\n")
        for i in range(0, len(states)):
            for j in range(0,len(states[i])):
                #print("START STATE", self.states[0])
                #if i == 0:
                #    print("ROTATION: 0", )
                #else:
                #    print("ROATATION", angles[i])
                #print("AROUND CENTROID:", centroid.getCoordinates())
                #print("CALCULATED", states[i][j].getName(), states[i][j].getCoordinates())
                #print("MANUAL_CALCULATED_ANS", self.states[i][j])
                #print("\n")
                for k in range(0, len(states[i][j].getCoordinates())):
                    self.assertAlmostEqual(states[i][j].getCoordinates()[k], self.states[i][j][k])


      


    # Rotate points by a given angle around the centroid
    
    # Rotate points around a centroid by a list of angles
      

# Main Function

if __name__ == '__main__':
    unittest.main()
