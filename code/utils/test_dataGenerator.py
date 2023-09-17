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

        self.assertEqual(self.DG.generateMatrix(scaleFactor=0, edgeFactor=1), points)

    def test_multi_nodes(self):
        #Note: since it's probabalistic this might fail occasioanally
        pt1 = (0,0)
        pt2 = (0,1)
        pt3 = (1,0)

        points = [pt1,pt2,pt3]

        generatedGraph = self.DG.generateMatrix(scaleFactor=1, edgeFactor=1)

        self.assertListEqual(generatedGraph,points)


    def test_labelNodes(self):

        labelledNodes = {
                        "name":["i"],
                        "longitude":[0],
                        "latitude":[0]
                        }
        
        pt = (0,0)
        points = [pt]
        numClasses = 4

        self.assertDictEqual(self.DG.labelNodes(points=points,numClasses=numClasses, random_seed=3), labelledNodes)


    def test_multiLabelling(self):

        labelledNodes = {
                        "name":["i","i","I"],
                        "longitude":[0,0,1],
                        "latitude":[0,1,0]
                        }

        pt1 = (0,0)
        pt2 = (0,1)
        pt3 = (1,0)

        points = [pt1,pt2,pt3]
        numClasses = 4

        self.assertDictEqual(self.DG.labelNodes(points=points,numClasses=numClasses, random_seed=3), labelledNodes)


    def test_save_location(self):

        experiment = "test1"
        saveType = "location"
        loc1 = "location_1"

        loc1_labels = {
                        "name":["i"],
                        "longitude":[0],
                        "latitude":[0]
                        }
        
        saveLocation = self.DG.saveToFile(experiment_name=experiment, saveType=saveType, number=1, data=loc1_labels)

        self.assertTrue(saveLocation.endswith("/data/experiments/test1/location/location1.csv"))
        
        self.assertTrue(os.path.isfile(saveLocation))




# Main Function

if __name__ == '__main__':
    unittest.main()
