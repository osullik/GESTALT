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
sys.path.insert(1, os.getcwd()+"/../../data")

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
        #Returns the current concept Map Dictionary from the class properites
        return(self._cm_dict)
    
    def getInvertedIndex(self):
        #Returns the current inverted index Dictionary from the class properites
        return(self._II)
          
    #Atomic Methods
        
    def loadLocations(self, objectsDataFrame:pd.DataFrame)->None:
        #Creates the dictionary of concept maps for all locations and saves to the class properties. 
        self._cm_dict.update(self.cm.createConceptMap(input_df=objectsDataFrame))

    def loadInvertedIndex(self, objectsDataFrame:pd.DataFrame)->None:
        #Creates the inverted index for all locations and saves to the class properties. 
        self._II = InvertedIndex(dataframe=objectsDataFrame)

    def generateQueryMap(self, query:pd.DataFrame)->tuple:
        # Generates a concept map (dict of Location:NP Array) and search order (list) for a given set of points. 
        queryMap = self.cm.createConceptMap(input_df=query)
        searchOrder = self.cm.getSearchOrder(queryMap['PICTORIAL_QUERY'])
        return((queryMap,searchOrder))
    
    def generateRotations(self, points:list[Point],alignToIntegerGrid:bool=False)->set:
        # Generates all unique rotations for a set of points
        # alignToIntegerGrid rounds all point positions to integers; intended for use in testing. 
        return(self.compass.generateRotations(points,alignToIntegerGrid))


    #Composite Methods
    
    def preprocessData(self, objectsDataFrame:pd.DataFrame)->None:
        '''
        PURPOSE:
            prepare the data structures in the class that the search operations will work against. 
        INPUT ARGS: 
            objectsDataFrame - pandas Dataframe - Contains all the object names lats, longs, assigned locations and confidence scores
        PROCESS:
            Feed the dataframe to the relevant constructors. 
        OUTPUT:
            none; creates the class properties _cm_dict to hold concept maps for locations and _II to hold the inverted index
        '''

        print("Loading location data to concept maps...\n")
        self.loadLocations(objectsDataFrame=objectsDataFrame)
        print("Loading location data to inverted index...\n")
        self.loadInvertedIndex(objectsDataFrame=objectsDataFrame)
        print("Pre-processing complete.\n")

    def getQueryMapConfigurations(self, points:list[Point],alignToIntegerGrid:bool=False)->list[tuple]:
        '''
        PURPOSE:
            Generates all possible query configurations for a set of points as concept maps
        INPUT ARGS: 
            points - list of compass.Point objects - all the points on the query canvas
            alignToIntegerGrid - boolean - when true, rounds the position of a point to the nearest whole number. Primarily for testing. 
        PROCESS:
            generate all the possible unique rotations for those points
            Convert those rotations to dataframes we can use to generate query concept maps
            Because of the dimensionality reduction from euclidian space to our concept map, we need to deduplicate again. 
        OUTPUT:
            allQueries - list of tuples of form ({"PICTORIAL_QUERY":concept map}, [searchOrder])
        
        '''
        
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
        '''
        PURPOSE:
            To feed each possible query configration into the gridSearch until we get a match
        INPUT ARGS:
            queries - list of tuples of form ({"PICTORIAL_QUERY":concept map}, [searchOrder])
        METHOD:
            Get each query & feed it into the search. 
        OUTPUT:
            returns true if a match is found, false otherwise
            
        '''

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

class CompassDataLoader():
    def __init__(self) -> None:
        self.ER = CompassExperimentRunner()
        pass

    def checkExperimentFilesExist(self, experimentName:str, locationFileName:str, queryFileName:str, experimentsDirectory:str="experiments")->bool:

        dataDirectory = ""
        for p in sys.path:
            if p.endswith("data"):
                dataDirectory = p

        assert((dataDirectory in sys.path),"Unable to find the 'GESTALT/data' directory - does it exist?")

        experimentsDirectoryPath = os.path.join(dataDirectory, experimentsDirectory)
        assert (os.path.exists(experimentsDirectoryPath),"'data/experiments' does not exist.")

        experimentDirectory = os.path.join(experimentsDirectoryPath, "experiment_"+experimentName)
        assert (os.path.exists(experimentDirectory),"'data/experiments/experiment_"+experimentName+"' does not exist.")
        
        locationPath = os.path.join(experimentDirectory,"locations",locationFileName)
        queryPath = os.path.join(experimentDirectory,"queries",queryFileName)

        if os.path.isfile(locationPath):
            if os.path.isfile(queryPath):
                return (True)
            else:
                print("FileNotFound:", queryFileName, "in experiment", experimentName)
                return (False)
        else:
            print("FileNotFound:", locationFileName, "in experiment", experimentName)
            return (False)
        
    def getExperimentFiles(self,experimentName:str, experimentsDirectory:str="experiments"):

        dataDirectory = ""
        for p in sys.path:
            if p.endswith("data"):
                dataDirectory = p
        assert((dataDirectory in sys.path),"Unable to find the 'GESTALT/data' directory - does it exist?")

        experimentsDirectoryPath = os.path.join(dataDirectory, experimentsDirectory)
        assert (os.path.exists(experimentsDirectoryPath),"'data/experiments' does not exist.")

        experimentDirectory = os.path.join(experimentsDirectoryPath, "experiment_"+experimentName)
        assert (os.path.exists(experimentDirectory),"'data/experiments/experiment_"+experimentName+"' does not exist.")

        locationPath = os.path.join(experimentDirectory,"locations")
        queryPath = os.path.join(experimentDirectory,"queries")

        locations = os.listdir(locationPath)
        queries = os.listdir(queryPath)

        returnLocations = []
        returnQueries = []

        for location in locations:
            returnLocations.append(os.path.join(locationPath,location))

        for query in queries:
            returnQueries.append(os.path.join(queryPath,query))
        
        return (returnLocations,returnQueries)
    
    def loadCSV(self,filePath:str)->pd.DataFrame:

        df = pd.read_csv(filePath, sep=",", header='infer')

        return df
    
    def loadCSVToConceptMap(self, filePath:str)->np.array:

        pathList = os.path.split(filePath)
        name = pathList[-1]
        name = name.split(".")[0]

        df = pd.read_csv(filePath, sep=",", header='infer')
        self.ER.loadLocations(df)
        cm = self.ER.getConceptMapDict()[name]

        return(cm)





#PREPROCESS:
    # Get the Locations

    # Generate Query Inverted Index and Concept Maps

#LIVE
# Get the Query Term

# Generate all rotations of Query Terms

# Search all locations for query term