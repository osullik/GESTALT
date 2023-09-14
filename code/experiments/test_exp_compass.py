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
sys.path.insert(1, os.getcwd()+"/../generator")

from compass import Point
from compass import Compass
from conceptMapping import ConceptMapper
from search import InvertedIndex
from exp_compass import CompassExperimentRunner


#Classes

class test_compass_experiments(unittest.TestCase):

    def setUp(self):
        self.compass = Compass()
        self.conceptmapper = ConceptMapper()
        self.ER = CompassExperimentRunner()

        self.singleLoc_dict = {"name" : ["A","B"],
                                "longitude" : [0,10],
                                "latitude" : [0,10],
                                "predicted_location" : ["1","1"],
                                "object_prob":  [1,1],
                                "assignment_prob":[1,1]
        }

        self.singleLoc_df = pd.DataFrame(data=self.singleLoc_dict)
        self.singleLoc_conceptMap = np.array([
                                                [ 0 ,"B"],
                                                ["A", 0 ]
    
                                            ], dtype=object)
    
        self.ii_singleLoc_ans = {"A":{"1"},
                        "B":{"1"}}
    
        self.ii_singleLoc_counter_ans = {"A":1,
                                         "B":1}
    
        self.query_singleLoc = {"name": ["A","B"],
                                "longitude":[10,0],
                                "latitude":[10,0],
                                "predicted_location":["PICTORIAL_QUERY", "PICTORIAL_QUERY"]
                                }
        
        self.query_singleLoc_df = pd.DataFrame(data=self.query_singleLoc)

        self.queryMap_singleLoc_ans = np.array([
                                                [ 0 ,"A"],
                                                ["B", 0 ]
    
                                            ], dtype=object)
        self.queryOrder_singleLoc_ans = ["A","B"]

    def tearDown(self):
        pass

    def test_objectsExist(self):
        #Check to see that it can find, and create the appropriate objects
        self.assertEqual(str(type(self.compass)), "<class 'compass.Compass'>")
        self.assertEqual(str(type(self.conceptmapper)), "<class 'conceptMapping.ConceptMapper'>")

    def test_createConceptMap(self):

        #Create a simple concept Map with a single location and two objects

        self.singleLoc_conceptMap_answer = {"1": self.singleLoc_conceptMap} #Manually created answer to test against               
    
        self.ER.loadLocations(objectsDataFrame=self.singleLoc_df)
        singleLoc_conceptMap = self.ER.getConceptMapDict()

        self.assertTrue(np.array_equal(                                     #Pass test when the returned concept maps are the same
                                    singleLoc_conceptMap["1"], 
                                    self.singleLoc_conceptMap_answer["1"]))


    def test_createInvertedIndex(self):
        self.ER.loadInvertedIndex(objectsDataFrame=self.singleLoc_df)
        ii_obj = self.ER.getInvertedIndex()
        ii = ii_obj.getIndex()
        ii_counter = ii_obj.getIndexCounter()

        self.assertDictEqual(ii, self.ii_singleLoc_ans)
        self.assertDictEqual(ii_counter, self.ii_singleLoc_counter_ans)


    def test_getQueryTerm(self):

        queryMap, searchOrder = self.ER.generateQueryMap(query=self.query_singleLoc_df)
        self.assertTrue(np.array_equal(queryMap["PICTORIAL_QUERY"], self.queryMap_singleLoc_ans))
        self.assertEqual(searchOrder, self.queryOrder_singleLoc_ans)

    def test_generateRotations(self):

        point_a = Point("b", 0 ,0 )
        point_b = Point("a", 10, 10)
        test_points = [point_a, point_b]

        rotations = self.ER.generateRotations(points=test_points,alignToIntegerGrid=True)

        uniqueRotations = set((
                                    frozenset((('b',(0,0)),('a',(10,10)))),
                                    frozenset((('a',(5,12)),('b',(5,-2)))),
                                    frozenset((('a',(-2,5)),('b',(12,5)))),
                                    frozenset((('a',(0,10)),('b',(10,0)))),
                                    frozenset((('a',(5,-2)),('b',(5,12)))),
                                    frozenset((('a',(12,5)),('b',(-2,5)))),
                                    frozenset((('a',(10,0)),('b',(0,10))))     
                            ))
    
        self.assertSetEqual(rotations, uniqueRotations)

    def test_generateRotatedQueryMaps(self):
        np.set_printoptions(precision=3)
        point_a = Point("B", 0 ,0 )
        point_b = Point("A", 10, 10)
        test_points = [point_a, point_b]

        uniqueRotations = set((
                                    frozenset((('B',(0,0)),('A',(10,10)))),
                                    frozenset((('A',(5,12)),('B',(5,-2)))),
                                    frozenset((('A',(-2,5)),('B',(12,5)))),
                                    frozenset((('A',(0,10)),('B',(10,0)))),
                                    frozenset((('A',(5,-2)),('B',(5,12)))),
                                    frozenset((('A',(12,5)),('B',(-2,5)))),
                                    frozenset((('A',(10,0)),('B',(0,10))))     
                            ))

    
        possibleConfigurations = [ np.array([
                                            [ 0 ,"B"],
                                            ["A", 0 ]
                                            ], dtype=object),
                                    np.array([
                                            ["A", 0 ],
                                            [ 0, "B"]
                                            ], dtype=object),
                                    np.array([
                                            [ 0 ,"A"],
                                            ["B", 0 ]
                                            ], dtype=object),
                                    np.array([
                                            ["B", 0 ],
                                            [ 0, "A"]
                                            ], dtype=object)
                                ]

        queryMapConfigurations = self.ER.getQueryMapConfigurations(points=test_points,alignToIntegerGrid=True)

        #print("\n")
        #for i in range (0, len(queryMapConfigurations)):
        #    print("Query Map")
        #    print(queryMapConfigurations[i][0]["PICTORIAL_QUERY"])
        #print('\n')
        #for i in range(0, len(possibleConfigurations)):
        #    print("Answer:")
        #    print(possibleConfigurations[i])

        self.assertEqual(len(possibleConfigurations),len(queryMapConfigurations))

    def test_gridSearchByRotatedQueries(self):
        self.ER.preprocessData(objectsDataFrame=self.singleLoc_df)

        np.set_printoptions(precision=3)
        point_a = Point("B", 0 ,0 )
        point_b = Point("A", 10, 10)
        test_points = [point_a, point_b]

        uniqueRotations = set((
                                    frozenset((('B',(0,0)),('A',(10,10)))),
                                    frozenset((('A',(5,12)),('B',(5,-2)))),
                                    frozenset((('A',(-2,5)),('B',(12,5)))),
                                    frozenset((('A',(0,10)),('B',(10,0)))),
                                    frozenset((('A',(5,-2)),('B',(5,12)))),
                                    frozenset((('A',(12,5)),('B',(-2,5)))),
                                    frozenset((('A',(10,0)),('B',(0,10))))     
                            ))

    
        possibleConfigurations = [ np.array([
                                            [ 0 ,"B"],
                                            ["A", 0 ]
                                            ], dtype=object),
                                    np.array([
                                            ["A", 0 ],
                                            [ 0, "B"]
                                            ], dtype=object),
                                    np.array([
                                            [ 0 ,"A"],
                                            ["B", 0 ]
                                            ], dtype=object),
                                    np.array([
                                            ["B", 0 ],
                                            [ 0, "A"]
                                            ], dtype=object)
                                ]

        queryMapConfigurations = self.ER.getQueryMapConfigurations(points=test_points,alignToIntegerGrid=True)

        self.assertEqual(len(possibleConfigurations),len(queryMapConfigurations))

        self.assertTrue(self.ER.gridSearchAllRotations(queries=queryMapConfigurations))
        


#Test Suites:

def suite_allTest():
    suite = unittest.TestSuite()
    suite.addTest(test_compass_experiments("test_objectsExist"))
    suite.addTest(test_compass_experiments("test_createConceptMap"))
    suite.addTest(test_compass_experiments("test_createInvertedIndex"))
    suite.addTest(test_compass_experiments("test_getQueryTerm"))
    suite.addTest(test_compass_experiments("test_generateRotations"))
    suite.addTest(test_compass_experiments("test_generateRotatedQueryMaps"))
    suite.addTest(test_compass_experiments("test_gridSearchByRotatedQueries"))
    return suite
#Main Function

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite_allTest())