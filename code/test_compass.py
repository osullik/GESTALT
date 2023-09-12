#Core Python Imports
import unittest
import math

# Libarary Imports

# User class imports

from compass import Compass

# Global Vars

# Classes

class test_Compass(unittest.TestCase):

    def setUp(self):
        
        self.COMPASS = Compass()

        #Vars for test_centroid
        self.singlePoint_problem = [(5,5)]
        self.singlePoint_answer = (5,5)

        self.twoPointsX_problem = [(0,5), (10,5)]
        self.twoPointsX_answer = (5,5)

        self.twoPointsY_problem = [(5,0), (5,10)]
        self.twoPointsY_answer = (5,5)

        self.threePoints_problem = [(0,0), (0,9), (9,0)]
        self.threePoints_answer = (3,3)

        self.fourPoints_problem = [(0,0), (0,10), (10,0), (10,10)]
        self.fourPoints_answer = (5,5)

        #Vars for test_angles
        self.referencePoint = (5,10)
        self.singlePoint = (5,5)
        self.singlePointCentrid = (5,5)
        self.singlePointAngle = 90

        

    def tearDown(self):
        pass

    #Get Centroid
    def test_Centroids(self):

        self.assertEqual(self.COMPASS.getCentroid(self.singlePoint_problem), self.singlePoint_answer)
        self.assertEqual(self.COMPASS.getCentroid(self.twoPointsX_problem), self.twoPointsX_answer)
        self.assertEqual(self.COMPASS.getCentroid(self.twoPointsY_problem), self.twoPointsY_answer)
        self.assertEqual(self.COMPASS.getCentroid(self.threePoints_problem), self.threePoints_answer)
        self.assertEqual(self.COMPASS.getCentroid(self.fourPoints_problem), self.fourPoints_answer)

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

        self.N = (0,5)
        self.C = (0,0)
        self.P = (5,0)
        self.n = 5
        self.p = 5
        self.c = math.sqrt(50)

        self.assertEqual(self.COMPASS.getSideLength(self.C, self.N), self.p)
        self.assertEqual(self.COMPASS.getSideLength(self.N, self.P), self.c)
        self.assertEqual(self.COMPASS.getSideLength(self.C, self.P), self.n)


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

        self.small_centroid = (0,0)
        self.small_point = (5,0)
        self.small_northReference = (0,5)
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

        self.small_centroid2 = (5,0)
        self.small_point2 = (0,0)
        self.small_northReference2 = (5,5)
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


        self.multi_N  = (5 ,5 )
        self.multi_C  = (5 ,0 )
        self.multi_P1 = (10,0 )
        self.multi_P2 = (10,5 )
        self.multi_P3 = (0 ,0 )

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

    def test_singleRotation(self):

        self.rotate_centroid    = (5 ,5 )
        self.rotate_P1          = (5,10)
        self.roatate_angle      = 180
        self.rotate_P1_prime    = (5 ,0 )

        p1_prime = self.COMPASS.rotatePoint(centroid=self.rotate_centroid, point=self.rotate_P1, angle=self.roatate_angle)

        for i in range (0, len(p1_prime)):
            self.assertAlmostEqual(p1_prime[i], self.rotate_P1_prime[i], places=2)

    def test_singleRotation_multiPoints(self):

        self.rotate_centroid    = (5 ,5 )

        self.rotate_P1          = (5,10)
        self.rotate_P2          = (10,10)
        self.rotate_P3          = (1 , 1)

        self.roatate_angle      = 180

        #P1 and Angle used from last test (5,10) and 180 Deg respectively
        self.rotate_P1_prime    = (5 ,0 )
        self.rotate_P2_prime    = (0, 0 )
        self.rotate_P3_prime    = (9 ,9 )

        # Test Each individually

        p1_prime = self.COMPASS.rotatePoint(centroid=self.rotate_centroid, point=self.rotate_P1, angle=self.roatate_angle)
        for i in range (0, len(p1_prime)):
            self.assertAlmostEqual(p1_prime[i], self.rotate_P1_prime[i], places=2)
        
        p2_prime = self.COMPASS.rotatePoint(centroid=self.rotate_centroid, point=self.rotate_P2, angle=self.roatate_angle)
        for i in range (0, len(p2_prime)):
            self.assertAlmostEqual(p2_prime[i], self.rotate_P2_prime[i], places=2)

        p3_prime = self.COMPASS.rotatePoint(centroid=self.rotate_centroid, point=self.rotate_P3, angle=self.roatate_angle)
        for i in range (0, len(p3_prime)):
            self.assertAlmostEqual(p3_prime[i], self.rotate_P3_prime[i], places=2)


        self.rotate_list = (self.rotate_P1, self.rotate_P2, self.rotate_P3)
        self.rotatedList = (self.rotate_P1_prime, self.rotate_P2_prime, self.rotate_P3_prime)

        self.returnedRotations = self.COMPASS.rotateAllPoints(centroid=self.rotate_centroid, points=self.rotate_list, angle=self.roatate_angle)

        for i in range(0, len(self.returnedRotations)):
            for j in range (0, 2):
                self.assertAlmostEqual(self.returnedRotations[i][j], self.rotatedList[i][j], places=2)


        



        

    # Rotate points by a given angle around the centroid
    
    # Rotate points around a centroid by a list of angles
      

# Main Function

if __name__ == '__main__':
    unittest.main()
