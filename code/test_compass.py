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


    # Rotate points by a given angle around the centroid
    
    # Rotate points around a centroid by a list of angles
      

# Main Function

if __name__ == '__main__':
    unittest.main()
