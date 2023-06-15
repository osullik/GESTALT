# System Imports
import unittest

# Library Imports
from scipy.spatial import KDTree

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



def suite_direction_locations():
    print("\n\n===== Testing Single Direction Relations =====\n")
    suite = unittest.TestSuite()
    suite.addTest(test_single_direction_relations('test_singleDirection_northOf'))
    suite.addTest(test_single_direction_relations('test_multiDirection_southEastOf'))
    suite.addTest(test_single_direction_relations('test_noDirection'))
    suite.addTest(test_single_direction_relations('test_twoSearchTerms_succeess'))

    #suite.addTest(test_single_direction_relations('test_singleDirection_southOf_originFirst'))
    #suite.addTest(test_single_direction_relations('test_singleDirection_southOf_destinationFirst'))
    #suite.addTest(test_single_direction_relations('test_singleDirection_northOf_originFirst'))
    #suite.addTest(test_single_direction_relations('test_singleDirection_northOf_destinationFirst'))

    #Multi Direction Locations

    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite_direction_locations())