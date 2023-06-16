# System Imports
import unittest

# Library Imports
from scipy.spatial import KDTree
import numpy as np
# User Imports
from conceptMapping import ConceptMapper

'''
class test_single_direction_relations(unittest.TestCase):

    def setUp(self):
        self.CM = ConceptMapper()
        self.westEastList =     ["shed","shed","solar_panel","building","parking_lot","swimming_pool","parking_lot","tree","retaining_wall","tree","tree","sign","courtyard","building","tree","tree","tree","sign","vineyard","building"]
        self.southNorthList =   ["retaining_wall","sign","tree","tree","tree","tree","vineyard","parking_lot","tree","tree","sign","parking_lot","building","shed","building","solar_panel","shed","courtyard","building","swimming_pool"]
    
    def tearDown(self) -> None:
        del self.CM

    def test_singleDirection_westOf_originFirst(self):
        
        origin = "shed"
        relations = ["west_of"]
        destination = "building"

        self.assertTrue(self.CM.checkRelativeLocation(self.westEastList,
                                                        self.southNorthList, 
                                                        origin, 
                                                        relations, 
                                                        destination))

    def test_singleDirection_westOf_destinationFirst(self):
        origin = "building"
        relations = ["west_of"]
        destination = "shed"
        self.assertFalse(self.CM.checkRelativeLocation(self.westEastList,
                                                        self.southNorthList, 
                                                        origin, 
                                                        relations, 
                                                        destination))
        
    
    def test_singleDirection_eastOf_originFirst(self):
        
        origin = "shed"
        relations = ["east_of"]
        destination = "building"

        self.assertFalse(self.CM.checkRelativeLocation(self.westEastList,
                                                        self.southNorthList, 
                                                        origin, 
                                                        relations, 
                                                        destination))
        
    def test_singleDirection_eastOf_destinationFirst(self):
        
        origin = "building"
        relations = ["east_of"]
        destination = "shed"

        self.assertTrue(self.CM.checkRelativeLocation(self.westEastList,
                                                        self.southNorthList, 
                                                        origin, 
                                                        relations, 
                                                        destination))
        

    def test_singleDirection_southOf_originFirst(self):
        
        origin = "sign"
        relations = ["south_of"]
        destination = "vineyard"

        self.assertTrue(self.CM.checkRelativeLocation(self.westEastList,
                                                        self.southNorthList, 
                                                        origin, 
                                                        relations, 
                                                        destination))
        
    def test_singleDirection_southOf_destinationFirst(self):
        origin = "vineyard"
        relations = ["south_of"]
        destination = "sign"
        self.assertFalse(self.CM.checkRelativeLocation(self.westEastList,
                                                        self.southNorthList, 
                                                        origin, 
                                                        relations, 
                                                        destination))    
        

    def test_singleDirection_northOf_originFirst(self):
        
        origin = "sign"
        relations = ["north_of"]
        destination = "vineyard"

        self.assertFalse(self.CM.checkRelativeLocation(self.westEastList,
                                                        self.southNorthList, 
                                                        origin, 
                                                        relations, 
                                                        destination))
        
    def test_singleDirection_northOf_destinationFirst(self):
        
        origin = "vineyard"
        relations = ["north_of"]
        destination = "sign"

        self.assertTrue(self.CM.checkRelativeLocation(self.westEastList,
                                                        self.southNorthList, 
                                                        origin, 
                                                        relations, 
                                                        destination))
        

class multi_single_direction_relations(unittest.TestCase):
    def setUp(self):
        self.CM = ConceptMapper()
        self.westEastList =     ["shed","shed","solar_panel","building","parking_lot","swimming_pool","parking_lot","tree","retaining_wall","tree","tree","sign","courtyard","building","tree","tree","tree","sign","vineyard","building"]
        self.southNorthList =   ["retaining_wall","sign","tree","tree","tree","tree","vineyard","parking_lot","tree","tree","sign","parking_lot","building","shed","building","solar_panel","shed","courtyard","building","swimming_pool"]
    
    def tearDown(self) -> None:
        del self.CM

    def test_singleDirection_westOf_originFirst(self):
        
        origin = "shed"
        relations = ["west_of"]
        destination = "building"

        self.assertTrue(self.CM.checkRelativeLocation(self.westEastList,
                                                        self.southNorthList, 
                                                        origin, 
                                                        relations, 
                                                        destination))
'''


class test_single_direction_relations(unittest.TestCase):
    def setUp(self):
        self.CM = ConceptMapper()
        self.locationDict = {"northwest":["solar_panel","shed","building","swimming_pool"],
                            "northeast":["building","courtyard","building"],
                            "southwest":["shed","parking_lot","parking_lot"],
                            "southeast":["retaining_wall","tree","tree","tree","sign","tree","tree","tree","sign","vineyard",]
                        }
    def tearDown(self) -> None:
        del self.CM


    def test_singleDirection_northOf(self):
        
        searchTerm = "courtyard"
        northSouthRelation = "north_of"
        eastWestRelation = None

        self.assertTrue(self.CM.checkRelativeLocation(self.locationDict,
                                                        eastWestRelation,
                                                        northSouthRelation,
                                                        searchTerm))
        
    
    def test_multiDirection_southEastOf(self):
        
        searchTerm = "courtyard"
        northSouthRelation = "north_of"
        eastWestRelation = "east_of"

        self.assertTrue(self.CM.checkRelativeLocation(self.locationDict,
                                                        eastWestRelation,
                                                        northSouthRelation,
                                                        searchTerm))
        
    def test_noDirection(self):
        
        searchTerm = "courtyard"
        northSouthRelation = None
        eastWestRelation = None

        self.assertFalse(self.CM.checkRelativeLocation(self.locationDict,
                                                        eastWestRelation,
                                                        northSouthRelation,
                                                        searchTerm))
        

    def test_twoSearchTerms_succeess(self):
        
        searchTerm1 = "courtyard"
        northSouthRelation1 = "north_of"
        eastWestRelation1 = "east_of"

        searchTerm2 = "vineyard"
        northSouthRelation2 = "south_of"
        eastWestRelation2 = None


        term1Result = self.CM.checkRelativeLocation(self.locationDict,
                                                        eastWestRelation1,
                                                        northSouthRelation1,
                                                        searchTerm1)
        
        term2Result = self.CM.checkRelativeLocation(self.locationDict,
                                                        eastWestRelation2,
                                                        northSouthRelation2,
                                                        searchTerm2)

        self.assertTrue(term1Result == term2Result == True)

class test_recursive_grid_search(unittest.TestCase):

    def setUp(self):
        self.CM = ConceptMapper()

        self.trivialMatrix = np.array([["A"]],
                                     dtype=object)

        self.twoByTwoMatrix = np.array( [[ 0,"A"],
                                        ["B",0 ]],
                                        dtype=object)

        self.threeByThreeMatrix = np.array( [[ 0, "A", 0],
                                             ["B", 0, "C"],
                                             [ 0,  0,  0]],
                                            dtype=object)
        
        self.fourByFourMatrix = np.array(   [[ 0, "A", 0, 0],
                                             ["B", 0, "C",0],
                                             [ 0, "D", 0, 0],
                                             [ 0,  0,  0, 0]],
                                            dtype=object)
        
        self.sixBySixMatrix = np.array( [[ 0, "A", 0,  0,  0,  0 ],
                                         [ 0,  0, "F","B","D", 0 ],
                                         [ 0,  0, "B", 0, "E","C"],
                                         [ 0, "C", 0, "D","D", 0 ],
                                         [ 0,  0,  0,  0,  0,  0 ],
                                         ["A", 0,  0,  0,  0,  0 ]],
                                        dtype=object)
    def tearDown(self) -> None:
        del self.CM
        del self.trivialMatrix
        del self.twoByTwoMatrix
        del self.threeByThreeMatrix
        del self.fourByFourMatrix
        del self.sixBySixMatrix

    def test_trivial_matrix_baseCase_success(self):

        matrix = self.trivialMatrix
        searchList = ["A"]

        match = self.CM.searchMatrix(matrix, searchList)
        
        self.assertTrue(match)

    def test_trivial_matrix_baseCase_failure(self):

        matrix = self.trivialMatrix
        searchList = ["B"]

        match = self.CM.searchMatrix(matrix, searchList)
        
        self.assertFalse(match)

    def test_twoByTwo_matrix_Success(self):
        print("\n=== 2 x 2 SUCCESS ===\n")

        matrix = self.twoByTwoMatrix
        searchList = ["A","B"]

        match = self.CM.searchMatrix(matrix, searchList)
        
        self.assertTrue(match)
        print ("\n = = = = = = = = = \n")

    def test_twoByTwo_matrix_failure(self):
        print ("\n = = = = = = = = = \n")


        matrix = self.twoByTwoMatrix
        searchList = ["B","A"]

        match = self.CM.searchMatrix(matrix, searchList)
        
        self.assertFalse(match)


    def test_threeByThree_matrix_Success(self):
        matrix = self.threeByThreeMatrix
        searchList = ["A","C"]

        match = self.CM.searchMatrix(matrix, searchList)
        
        self.assertTrue(match)

    def test_fourByFour_matrix_Success(self):
        print("\n=== 4 x 4 SUCCESS ===\n")
        matrix = self.fourByFourMatrix
        toFind = ["C","D"]

        match = self.CM.searchMatrix(matrix, toFind)
        
        self.assertTrue(match)


    def test_fourByFour_matrix_Fail(self):
        print ("\n = = = = = = = = = \n")

        matrix = self.fourByFourMatrix
        toFind = ["C","D"]

        match = self.CM.searchMatrix(matrix, toFind)
        
        self.assertFalse(match)

    def test_sixBySix_matrix_Success(self):
        print("\n=== 6 x 6 SUCCESS ===\n")
        matrix = self.sixBySixMatrix
        toFind = ["A","C","F","B","D"]

        match = self.CM.searchMatrix(matrix, toFind)
        
        self.assertTrue(match)


    ### Test the ability to get the new edge term

class test_get_terms(unittest.TestCase):

    def setUp(self):
        self.CM = ConceptMapper()

        self.trivialMatrix =[["A"]]

        self.twoByTwoMatrix =[[ 0,"A"],
                                        ["B",0 ]]

        self.threeByThreeMatrix = [[ 0, "A", 0],
                                             ["B", 0, "C"],
                                             [ 0,  0,  0]]
        
        self.fourByFourMatrix = [[ 0, "A", 0, 0],
                                             ["B", 0, "C",0],
                                             [ 0, "D",  0,0],
                                             [ 0,  0,  0, 0]]
        
        self.sixBySixMatrix = [[ 0, "A", 0,  0,  0,  0 ],
                                [ 0,  0, "F","B","D", 0 ],
                                [ 0,  0, "B", 0, "E","C"],
                                [ 0, "C", 0, "D","D", 0 ],
                                [ 0,  0,  0,  0,  0,  0 ],
                                ["A", 0,  0,  0,  0,  0 ]]
    def tearDown(self) -> None:
        del self.CM
        del self.trivialMatrix
        del self.twoByTwoMatrix
        del self.threeByThreeMatrix
        del self.fourByFourMatrix
        del self.sixBySixMatrix
    
    def test_getTrivialList(self):
        inputMatrix = np.array([["A"]])
        searchList = self.CM.getSearchOrder(inputMatrix)
        self.assertEqual(searchList,["A"])

    def test_get1Item_1Row(self):
        inputMatrix = np.array([[ 0, "A"]],
                                dtype=object)
        searchList = self.CM.getSearchOrder(inputMatrix)
        
        self.assertEqual(searchList,["A"])
    
    def test_get1Item_1Column(self):
        inputMatrix = np.array([[ 0 ],
                                ["A"]],
                                dtype=object)

        searchList = self.CM.getSearchOrder(inputMatrix)
        self.assertEqual(searchList,["A"])

    def test_get1Item_1Matrix(self):
        inputMatrix = np.array([[ 0, "A"],
                                [ 0 , 0 ]],
                                dtype=object)
        searchList = self.CM.getSearchOrder(inputMatrix)
        self.assertEqual(searchList,["A"])

    def test_get2Item_1Row(self):
        inputMatrix = np.array([[ "A", "B"]],
                                dtype=object)
        searchList = self.CM.getSearchOrder(inputMatrix)
        
        self.assertEqual(searchList,["A","B"])
    
    def test_get2Item_1Column(self):
        inputMatrix = np.array([[ "A" ],
                                ["B"]],
                                dtype=object)

        searchList = self.CM.getSearchOrder(inputMatrix)
        self.assertEqual(searchList,["A","B"])

    def test_get2Item_1Matrix(self):
        inputMatrix = np.array([[ 0, "A"],
                                [ "B" , 0 ]],
                                dtype=object)
        searchList = self.CM.getSearchOrder(inputMatrix)
        self.assertEqual(searchList,["A","B"])






def suite_direction_locations():
    print("\n\n===== Testing Single Direction Relations =====\n")
    suite = unittest.TestSuite()
    suite.addTest(test_single_direction_relations('test_singleDirection_northOf'))
    suite.addTest(test_single_direction_relations('test_multiDirection_southEastOf'))
    suite.addTest(test_single_direction_relations('test_noDirection'))
    suite.addTest(test_single_direction_relations('test_twoSearchTerms_succeess'))
    return suite

def suite_recursive_grid_search():
    print("\n\n===== Testing Recursive Grid Search =====\n")
    suite = unittest.TestSuite()
    suite.addTest(test_recursive_grid_search('test_trivial_matrix_baseCase_success'))
    suite.addTest(test_recursive_grid_search("test_trivial_matrix_baseCase_failure"))
    suite.addTest(test_recursive_grid_search("test_twoByTwo_matrix_Success"))
    suite.addTest(test_recursive_grid_search("test_twoByTwo_matrix_failure"))
    suite.addTest(test_recursive_grid_search("test_threeByThree_matrix_Success"))
    suite.addTest(test_recursive_grid_search("test_fourByFour_matrix_Success"))
    suite.addTest(test_recursive_grid_search("test_sixBySix_matrix_Success"))
    #suite.addTest(test_recursive_grid_search('test_fourByFour_matrix_Fail'))
    return suite

def suite_get_terms():
    print("\n\n===== Testing Getting Boundary Terms =====\n")
    suite = unittest.TestSuite()
    suite.addTest(test_get_terms('test_getTrivialList'))
    suite.addTest(test_get_terms('test_get1Item_1Row'))
    suite.addTest(test_get_terms('test_get1Item_1Column'))
    suite.addTest(test_get_terms('test_get1Item_1Matrix'))
    suite.addTest(test_get_terms('test_get2Item_1Row'))
    suite.addTest(test_get_terms('test_get2Item_1Column'))
    suite.addTest(test_get_terms('test_get2Item_1Matrix'))

    return suite


    #Multi Direction Locations

    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    #runner.run(suite_direction_locations())
    runner.run(suite_get_terms())
    runner.run(suite_recursive_grid_search())
