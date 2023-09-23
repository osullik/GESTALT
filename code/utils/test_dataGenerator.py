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
from dataGenerator import DataGenerator, QuadrantMapConverter

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
        density = 1

        self.assertEqual(self.DG.generateMatrix(scaleFactor=0, edgeFactor=1)[0], points)
        self.assertEqual(self.DG.generateMatrix(scaleFactor=0, edgeFactor=1)[1], density)

    def test_multi_nodes(self):
        #Note: since it's probabalistic this might fail occasioanally
        pt1 = (0,0)
        pt2 = (0,1)
        pt3 = (1,0)

        points = [pt1,pt2,pt3]
        density = 2.0

        G = self.DG.generateMatrix(scaleFactor=1, edgeFactor=1)
        generatedGraph = G[0]
        generatedDensity = G[1]

        self.assertListEqual(generatedGraph,points)
        self.assertEqual(generatedDensity,density)


    def test_labelNodes(self):

        labelledNodes = {
                        "name":["I"],
                        "longitude":[0],
                        "latitude":[0]
                        }
        
        pt = (0,0)
        points = [pt]
        numClasses = 4

        self.assertDictEqual(self.DG.labelNodes(points=points,numClasses=numClasses, random_seed=3), labelledNodes)


    def test_multiLabelling(self):

        labelledNodes = {
                        "name":["I","I","L"],
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
        
        pointList = self.DG.generateMatrix(scaleFactor=3, edgeFactor=1)[0]
        labelledPoints = self.DG.labelNodes(points=pointList,numClasses=numClasses, random_seed=3, queryTerms=query)

        self.assertDictEqual(labelledPoints,new_loc)


class test_quadrant_converter(unittest.TestCase):
    
    def setUp(self) -> None:
        self.compass = Compass()
        self.QMC = QuadrantMapConverter()
        self.DG = DataGenerator()
        return super().setUp()
    
    def tearDown(self) -> None:
        return super().tearDown()

    def test_quadrantMapConverter(self):

        locDict = {}
        locDict['name'] = ["M","E","x","M","E","E","i",1,2,3,4]
        locDict['longitude'] = [0.0,0.0,0.0,1.0,1.0,2.0,2.0,0.9518585083675655,1.479820666192317,2.502881216432216,0.05267196621949655]
        locDict['latitude'] =  [0.0,1.0,2.0,0.0,2.0,0.0,1.0,2.1769169011838074,2.415680154384778,0.26211543695925243,3.34987632838584]

        quad_loc_df = pd.DataFrame(data=locDict)

        quad_dict_ans = {"northwest":["x","E",1,4],
                         "northeast":[2],
                         "southwest":["M","E","M"],
                         'southeast':["E","i",3]
                         }

        self.assertDictEqual(self.QMC.generateQuadrantMap(quad_loc_df),quad_dict_ans)

# Main Function

if __name__ == '__main__':
    unittest.main()
