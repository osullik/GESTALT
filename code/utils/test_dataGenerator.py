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

    def test_generateQueryDistortions(self):

        query = {
                "name":["i","j"],
                "longitude":[4,6],
                "latitude":[4,6]
                }

        query_df = pd.DataFrame(data=query)

        distorted_query_rotated_ans = {
                "name":["i","j"],
                "longitude":[6,4],
                "latitude":[6,4]
                }
        
        distorted_query_expanded_ans = {
                "name":["i","j"],
                "longitude":[0,10],
                "latitude":[0,10]
                }
        
        distorted_query_pos_vert_shift_ans = {
                "name":["i","j"],
                "longitude":[4,6],
                "latitude":[8,10]
                }
        
        distorted_query_neg_vert_shift_ans = {
                "name":["i","j"],
                "longitude":[4,6],
                "latitude":[0,2]
                }
        
        distorted_query_pos_horiz_shift_ans = {
                "name":["i","j"],
                "longitude":[8,10],
                "latitude":[4,6]
                }
        
        distorted_query_neg_horiz_shift_ans = {
                "name":["i","j"],
                "longitude":[0,2],
                "latitude":[4,6]
                }

        distorted_query_rotated = self.DG.distortQuery(query_dict=query, canvas_size = 10, rotation_degrees=180, expansion=0, shift_vertical=0, shift_horizontal=0)

        distorted_query_expanded = self.DG.distortQuery(query_dict=query, canvas_size = 10, rotation_degrees=0, expansion=1, shift_vertical=0, shift_horizontal=0)

        distorted_query_pos_vert_shift = self.DG.distortQuery(query_dict=query, canvas_size = 10, rotation_degrees=0, expansion=0, shift_vertical=1, shift_horizontal=0)

        distorted_query_neg_vert_shift = self.DG.distortQuery(query_dict=query, canvas_size = 10, rotation_degrees=0, expansion=0, shift_vertical=-1, shift_horizontal=0)

        distorted_query_pos_horiz_shift = self.DG.distortQuery(query_dict=query, canvas_size = 10, rotation_degrees=0, expansion=0, shift_vertical=0, shift_horizontal=1)

        distorted_query_neg_horiz_shift = self.DG.distortQuery(query_dict=query, canvas_size = 10, rotation_degrees=0, expansion=0, shift_vertical=0, shift_horizontal=-1)


        #self.assertTrue(distorted_query_rotated.equals(pd.DataFrame(data=distorted_query_rotated_ans)))
        self.assertDictEqual(distorted_query_rotated,distorted_query_rotated_ans)
        self.assertDictEqual(distorted_query_expanded,distorted_query_expanded_ans)
        self.assertDictEqual(distorted_query_pos_vert_shift,distorted_query_pos_vert_shift_ans)
        self.assertDictEqual(distorted_query_neg_vert_shift,distorted_query_neg_vert_shift_ans)
        self.assertDictEqual(distorted_query_pos_horiz_shift,distorted_query_pos_horiz_shift_ans)
        self.assertDictEqual(distorted_query_neg_horiz_shift,distorted_query_neg_horiz_shift_ans)

    def test_insertQueryToLocation(self):
        #Non-deterministic test; will fail frequently 

        query = {
                "name":["0","1","2"],
                "longitude":[0,4,6],
                "latitude":[0,4,6]
                }
        
        new_loc = {
                "name":['i','i','I','i','i','i','L','I','L','I','p','I','i','I','i','i','0','1','2'],
                "longitude":[0, 0, 0, 0, 0, 1, 1, 1, 2, 3, 4, 4, 4, 5, 6, 6, 0, 4, 6],
                "latitude":[1, 2, 3, 4, 5, 0, 4, 6, 0, 0, 0, 1, 6, 0, 1, 4, 0, 4, 6]
                }
        
        numClasses = 4
        
        pointList = self.DG.generateMatrix(scaleFactor=3, edgeFactor=1)
        labelledPoints = self.DG.labelNodes(points=pointList,numClasses=numClasses, random_seed=3, queryTerms=query)

        self.assertDictEqual(labelledPoints,new_loc)



# Main Function

if __name__ == '__main__':
    unittest.main()
