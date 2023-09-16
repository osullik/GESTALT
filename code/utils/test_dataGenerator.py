#Author: Kent O'Sullivan
#Email: osullik@umd.edu

# System Imports
import sys
import os
import unittest
# Library Imports
import pandas as pd
import numpy as np

# User file imports

sys.path.insert(1, os.getcwd()+"/../")
sys.path.insert(1, os.getcwd()+"/../compass")
sys.path.insert(1, os.getcwd()+"/../gestalt")
sys.path.insert(1, os.getcwd()+"/../experiments")
sys.path.insert(1, os.getcwd()+"/../utils")

from compass import Point
from compass import Compass
from conceptMapping import ConceptMapper
from search import InvertedIndex
from exp_compass import CompassExperimentRunner, CompassDataLoader
from dataGenerator import DataGenerator

#Classes

class test_compass_experiments(unittest.TestCase):
    def setUp(self) -> None:
        self.compass = Compass()
        self.DL = CompassDataLoader()
        self.DG = DataGenerator()
        return super().setUp()
    
    def tearDown(self) -> None:
        return super().tearDown()

    def test_single_node(self):

        pt = (0,0)
        points = [pt]

        self.assertEqual(self.DG.generateMatrix(locationSize=0, numObjects=1, labels=['A']), points)


# Main Function

if __name__ == '__main__':
    unittest.main()
