#Author: Kent O'Sullivan
#Email: osullik@umd.edu

# System Imports
import sys
import os
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

#Main Function

class CompassExperimentRunner():

    def __init__(self):
        self.compass = Compass()
        self.cm = ConceptMapper()
        self._cm_dict = {}
        self._II = None

    #Class methods
        
    def getConceptMapDict(self):
        return(self._cm_dict)
    
    def getInvertedIndex(self):
        return(self._II)
          
    #Atomic Methods
        
    def loadLocations(self, objectsDataFrame:pd.DataFrame)->None:
        self._cm_dict.update(self.cm.createConceptMap(input_df=objectsDataFrame))

    def loadInvertedIndex(self, objectsDataFrame:pd.DataFrame)->None:
        self._II = InvertedIndex(dataframe=objectsDataFrame)

    def generateQueryMap(self, query:pd.DataFrame)->tuple:
        queryMap = self.cm.createConceptMap(input_df=query)
        searchOrder = self.cm.getSearchOrder(queryMap['PICTORIAL_QUERY'])

        return((queryMap,searchOrder))
    
    def generateRotations(self, points:list[Point],alignToIntegerGrid:bool=False)->set:
        return(self.compass.generateRotations(points,alignToIntegerGrid))


    #Composite Methods
    
    def preprocessData(self, objectsDataFrame:pd.DataFrame)->None:
        print("Loading location data to concept maps...\n")
        self.loadLocations(objectsDataFrame=objectsDataFrame)
        print("Loading location data to inverted index...\n")
        self.loadInvertedIndex(objectsDataFrame=objectsDataFrame)
        print("Pre-processing complete.\n")

    def getQueryMapConfigurations(self, points:list[Point],alignToIntegerGrid:bool=False)->list[np.array]:
        
        rotations = self.generateRotations(points=points,alignToIntegerGrid=alignToIntegerGrid) 
        
        allRotations = []   

        for rotation in rotations:                          #Convert rotations into data frames. 
            pointNames = []
            pointLongitudes = []
            pointLatitudes = []
            pointPredictedLocs = []
            for point in rotation:
                pointNames.append(point[0])
                pointLongitudes.append(point[1][0])
                pointLatitudes.append(point[1][1])
                pointPredictedLocs.append("PICTORIAL_QUERY")
            
            rotation_dict = {"name":pointNames,
                            "longitude":pointLongitudes,
                            "latitude":pointLatitudes,
                            "predicted_location":pointPredictedLocs}
            rotation_df = pd.DataFrame(data=rotation_dict)
            allRotations.append(rotation_df)

        allQueries = []

        for rot in allRotations:                        #Append unique rotations to the list of possible rotations. 
            found = False
            if len(allQueries)==0:
                    allQueries.append(self.generateQueryMap(rot))
            for query in allQueries:
                if np.array_equal(self.generateQueryMap(rot)[0]["PICTORIAL_QUERY"], query[0]["PICTORIAL_QUERY"]) == True:
                    found = True
            if found == False:
                allQueries.append(self.generateQueryMap(rot))

        return(allQueries)
                
    def gridSearchAllRotations(self, queries:list):

        results = []
        
        for queryTuple in queries:
            query = queryTuple[0]["PICTORIAL_QUERY"]
            searchOrder = queryTuple[1]
            
            for loc in self._cm_dict.keys():
                result = self.cm.searchMatrix(self._cm_dict[loc],searchOrder.copy())   #Don't forget to take a copy of the list... 
                if result == True: 
                    results.append(self._cm_dict[loc])
                    result = False
                
        if len(results) ==0:                                            #Output. TODO: Use Popup window to output
            print('No Results Found')
            return False
        else:
            print("Found Following Matches to Query:")
            for res in results: 
                print(res)
            return True



#PREPROCESS:
    # Get the Locations

    # Generate Query Inverted Index and Concept Maps

#LIVE
# Get the Query Term

# Generate all rotations of Query Terms

# Search all locations for query term