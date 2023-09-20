#Author: Kent O'Sullivan
#Email: osullik@umd.edu

# System Imports
import sys
import os
import argparse
import json
import datetime

# Library Imports
import pandas as pd
import numpy as np
from tqdm import tqdm

# User file imports

sys.path.insert(1, os.getcwd()+"/../")
sys.path.insert(1, os.getcwd()+"/../compass")
sys.path.insert(1, os.getcwd()+"/../gestalt")
sys.path.insert(1, os.getcwd()+"/../utils")
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
        #NOTE - this does not return anything, just updates the class property. 
        self._cm_dict.update(self.cm.createConceptMap(input_df=objectsDataFrame))

    def loadQueries(self, queryObjectsDataFrame:pd.DataFrame)->None:
        #Creates the dictionary of concept maps for all locations and saves to the class properties. 
        return(self.cm.createConceptMap(input_df=queryObjectsDataFrame,cm_type='query'))

    def loadInvertedIndex(self, objectsDataFrame:pd.DataFrame)->None:
        #Creates the inverted index for all locations and saves to the class properties. 
        self._II = InvertedIndex(dataframe=objectsDataFrame)

    def generateQueryMapDict(self, query:pd.DataFrame)->tuple:
        # Generates a concept map (dict of Location:NP Array) and search order (list) for a given set of points. 
        #print("DF ON BEING PASSED INTO GENERATE_DICT")
        #print(query)
        queriesDict = self.cm.createConceptMap(input_df=query,cm_type='query')

        #print("QUERIESDICT AFTER MAKING THE FIRST CONCEPT MAP")
        #print(queriesDict)

        #print("QUERIES DICT")
        #print(queriesDict)

        dictWithSortOrders = {}

        #for i in range (1, len(queriesDict.keys())+1):
        #    cm = queriesDict[i]['']

        for key in queriesDict.keys():
            #print("KEY IS", key)
            #print(queriesDict[key])
            cm = queriesDict[key][0]
            orderLists = queriesDict[key][1]
            lonList, latList = orderLists
            #print("QUERY:", key)
            #print("INPUR TO SEARCHORDER\nLON:\n",lonList, "\nLAT:\n", latList )
            searchOrder = self.cm.getSearchOrder(longSortedList=lonList, latSortedList=latList)
            #print("OUTPUT FROM SEARCHORDER\n", searchOrder)
            dictWithSortOrders[key] = {}
            dictWithSortOrders[key]['concept_map'] = cm
            dictWithSortOrders[key]['search_order'] = searchOrder

        #print("DICT WITH SORT ORDERS")
        #print(dictWithSortOrders)
        
        return dictWithSortOrders


        #lonLists, latLists = orderLists
        #searchOrder = self.cm.getSearchOrder(longSortedList=lonList, latSortedList=latList)
        #return((queryMap,searchOrder))
    
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
                pointNames.append(str(point[0]))
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
                    allQueries.append(self.generateQueryMapDict(rot))
            for query in allQueries:
                if np.array_equal(self.generateQueryMapDict(rot)["PICTORIAL_QUERY"]["concept_map"], query["PICTORIAL_QUERY"]["concept_map"]) == True:
                    found = True
            if found == False:
                allQueries.append(self.generateQueryMapDict(rot))

        return(allQueries)
    
    def gridSearchSingleQuery(self, query_searchOrder=list, query_cm:np.ndarray=None)->bool:
        results = []
        if query_cm is None:
            searchLocs = self.getConceptMapDict()
            for loc in searchLocs.keys():
                #print("SEARCHING in Matrix:",loc, "\n", searchLocs[loc])
                #print("SEARCHING FOR QUERY ORDER:", query_searchOrder)
                res = self.cm.searchMatrix(matrix=searchLocs[loc], toFind=query_searchOrder.copy())
                #[print("RES IS"), res, type(res)]
                if res == True:
                    results.append(loc)

        else:
            #print("SEARCHING FOR PATTERN:\n", query_cm)
            #print("SEARCHING FOR QUERY ORDER:", query_searchOrder)
            res = self.cm.searchMatrix(matrix=query_cm, toFind=query_searchOrder.copy())
            #print("RESULT:", res)
            return [res]
        
        return results
                
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
        
        for queryDict in queries:
            #print("MYSTERY QUERY", queryDict)
            query = queryDict["PICTORIAL_QUERY"]['concept_map']
            searchOrder = queryDict["PICTORIAL_QUERY"]['search_order']
            
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
    def __init__(self,experiment_name="test") -> None:
        self.ER = CompassExperimentRunner()
        self.experiment_name = experiment_name
        self._ignoreFiles = [".DS_Store"]       #Used to blacklist directory files we want to ignore. 
        pass

    def checkExperimentFilesExist(self, experimentName:str, locationFileName:str, queryFileName:str, experimentsDirectory:str="experiments")->bool:

        dataDirectory = ""
        for p in sys.path:
            if p.endswith("data"):
                dataDirectory = p

        assert (dataDirectory in sys.path),"Unable to find the 'GESTALT/data' directory - does it exist?"

        experimentsDirectoryPath = os.path.join(dataDirectory, experimentsDirectory)
        assert os.path.exists(experimentsDirectoryPath),"'data/experiments' does not exist."

        experimentDirectory = os.path.join(experimentsDirectoryPath, experimentName)
        assert os.path.exists(experimentDirectory),"'data/experiments/"+experimentName+"' does not exist."
        
        locationPath = os.path.join(experimentDirectory,"location",locationFileName)
        queryPath = os.path.join(experimentDirectory,"query",queryFileName)

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
        assert(dataDirectory in sys.path),"Unable to find the 'GESTALT/data' directory - does it exist?"

        experimentsDirectoryPath = os.path.join(dataDirectory, experimentsDirectory)
        assert os.path.exists(experimentsDirectoryPath),"'data/experiments' does not exist."

        experimentDirectory = os.path.join(experimentsDirectoryPath, experimentName)
        assert os.path.exists(experimentDirectory),"'data/experiments/"+experimentName+"' does not exist."

        locationPath = os.path.join(experimentDirectory,"location")
        queryPath = os.path.join(experimentDirectory,"query")

        locations = os.listdir(locationPath)
        queries = os.listdir(queryPath)

        returnLocations = []
        returnQueries = []

        for location in locations:
            if location not in self._ignoreFiles:
                returnLocations.append(os.path.join(locationPath,location))

        for query in queries:
            if query not in self._ignoreFiles:
                returnQueries.append(os.path.join(queryPath,query))

        metadataPath = locationPath = os.path.join(experimentDirectory,experimentName+".json")
        
        return (returnLocations,returnQueries,metadataPath)
    
    def loadCSV(self,filePath:str)->pd.DataFrame:

        df = pd.read_csv(filePath, sep=",", header='infer')

        return df
    
    def loadLocationCSVToConceptMap(self, filePath:str)->np.array:

        pathList = os.path.split(filePath)
        name = pathList[-1]
        name = name.split(".")[0]

        df = pd.read_csv(filePath, sep=",", header='infer')

        #print(df)

        if "predicted_location" not in df:
            df['predicted_location'] = name
        if "object_prob" not in df:
            df['object_prob'] = 1
        if "assignment_prob" not in df:
            df['assignment_prob'] = 1

        #print(df)

        self.ER.loadLocations(df)
        #print(self.ER.getConceptMapDict())
        cm = self.ER.getConceptMapDict()[name] #BUG workaround - just return whole dict
        #cm = self.ER.getConceptMapDict()

        return(cm)


    def loadQueryCSVToConceptMap(self, filePath:str)->np.array:

        pathList = os.path.split(filePath)
        name = pathList[-1]
        name = name.split(".")[0]

        df = pd.read_csv(filePath, sep=",", header='infer',dtype=object)

        #print(df)

        if "predicted_location" not in df:
            df['predicted_location'] = "PICTORIAL_QUERY"
        if "object_prob" not in df:
            df['object_prob'] = 1
        if "assignment_prob" not in df:
            df['assignment_prob'] = 1

        #print(df)

        qm = self.ER.loadQueries(df)[name]

        #cm = self.ER.getConceptMapDict()

        return(qm)




if __name__ == "__main__":

    argparser = argparse.ArgumentParser()									# initialize the argParser

    #General Params
    argparser.add_argument("--experimentName",
                            help="The name of the experiment we are running",
                            type = str,
                            required = False) 
    
    argparser.add_argument("--cardinalityInvariant",
                            help="Add this flag to run the cardinality invariant version of the code",
                            action="store_true",
                            required = False)
    
    times = {} #Dict to hold timing data for experiments
    results = {} #Dict to hold results for experiments


    flags = argparser.parse_args()

    DL = CompassDataLoader(flags.experimentName)
    ER = CompassExperimentRunner()

    location_files, query_files, metadata_file = DL.getExperimentFiles(experimentName=flags.experimentName)

    locations = []

    for location_file in tqdm(location_files):
        DL.loadLocationCSVToConceptMap(location_file) #Loads to the dict in the class
    ER._cm_dict = DL.ER.getConceptMapDict()
    
    #print(locations)
    #for loc in ER.getConceptMapDict():
        #print("LOC", loc)
        #print(ER.getConceptMapDict()[loc]) 
        #print("\n")

    queries = {}
    for i in tqdm(range(0,len(query_files))):
        q_path = query_files[i].split("/")
        q_name = q_path[-1].split(".")[0]
        print("QUERY NAME", q_name)
        
        query_df = DL.loadCSV(query_files[i])
        if "predicted_location" not in query_df:
            query_df['predicted_location'] = q_name
        if "object_prob" not in query_df:
            query_df['object_prob'] = 1
        if "assignment_prob" not in query_df:
            query_df['assignment_prob'] = 1
        points = []

        #print("QUERYDF",i+1," on initial load")
       #print(query_df)
        
        for idx, row in query_df.iterrows():
            points.append(Point(name=row['name'], x_coord=row['longitude'], y_coord=row['latitude']))

        queryMapDict = ER.generateQueryMapDict(query=query_df)
        #print("QUERYMAPDICT ON FIRST LOAD IS:")
        #print(queryMapDict)
        queryMap = queryMapDict[q_name]["concept_map"].copy()
        searchOrder = queryMapDict[q_name]["search_order"].copy()
        #print("FOR QUERY:",i+1,"GENERATED:\n", queryMap,"\nORDER:", searchOrder)
        queries[i+1] = {} 
        queries[i+1]['name'] = q_name
        queries[i+1]["queryMap"] = queryMap.copy()
        queries[i+1]["searchOrder"] = searchOrder.copy()
        queries[i+1]["points"] = points.copy()
        

    #print(queries)


    with open(metadata_file,'r') as infile:
        metadata = json.load(infile)

    

    print("\n#####_BEGINNING_SEARCH_#####\n")
    times['overall'] = {}
    times['queries'] = {}
    results['queries'] = {}

    times['overall']["start"] = datetime.datetime.now()

    if flags.cardinalityInvariant is False:

        for i in range(1,len(queries)+1):
            results['queries'][queries[i]['name']] = {}
            results['queries'][queries[i]['name']]["TP"] = 0
            results['queries'][queries[i]['name']]['FP'] = 0
            results['queries'][queries[i]['name']]['TN'] = 0
            results['queries'][queries[i]['name']]['FN'] = 0
            times['queries'][queries[i]['name']] = {}
            times['queries'][queries[i]['name']]['start'] = datetime.datetime.now()
            
            print("Searching...")
            #print("RUNNING QUERY:", queries[i]['name'])
            res = ER.gridSearchSingleQuery(query_searchOrder=queries[i]['searchOrder'])
            #print("FOUND LOCATIONS MATCHING QUERIES:", res)
            results['queries'][queries[i]['name']]['matches'] = res

            times['queries'][queries[i]['name']]["end  "] = datetime.datetime.now()
        
        #res = ER.gridSearchAllRotations(queries=queries)
        #res = ER.gridSearchAllRotations(queries=(queries[i]["rotations"]))
            #print(res)

            #Generate All possible rotations

    times['overall']["end  "] = datetime.datetime.now()
    times['overall']["total"] = times['overall']["end  "]-times['overall']["start"]

    print('Generating Accuracy Report...')

    #print(results)

    for queryNum in metadata['queries']['query'].keys():
        #print(metadata['queries']['query'][queryNum]['true_match'])
        #print(results['queries'][metadata['queries']['query'][queryNum]['name']]['matches'])

        if metadata['queries']['query'][queryNum]['true_match'] in results['queries'][metadata['queries']['query'][queryNum]['name']]['matches']:
            results['queries'][metadata['queries']['query'][queryNum]['name']]["TP"] += 1
        else:
            results['queries'][metadata['queries']['query'][queryNum]['name']]["FN"] += 1

        for found in results['queries'][metadata['queries']['query'][queryNum]['name']]['matches']:
            #print("FOUND", found)
            if found != metadata['queries']['query'][queryNum]['true_match']:
                results['queries'][metadata['queries']['query'][queryNum]['name']]["FP"] += 1
            
            #print("num_locations is ", metadata['locations']['num_locations'])
            results['queries'][metadata['queries']['query'][queryNum]['name']]["TN"] = (metadata['locations']['num_locations'] - (results['queries'][metadata['queries']['query'][queryNum]['name']]["TP"] + results['queries'][metadata['queries']['query'][queryNum]['name']]["FP"] + results['queries'][metadata['queries']['query'][queryNum]['name']]["FN"]))
        
        if len(results['queries'][metadata['queries']['query'][queryNum]['name']]['matches']) == 0:
            results['queries'][metadata['queries']['query'][queryNum]['name']]["TN"] = (metadata['locations']['num_locations'] - (results['queries'][metadata['queries']['query'][queryNum]['name']]["TP"] + results['queries'][metadata['queries']['query'][queryNum]['name']]["FP"] + results['queries'][metadata['queries']['query'][queryNum]['name']]["FN"]))

        #results['queries'][metadata['queries']['query'][queryNum]['name']]["accuracy"] = 

        '''
        for res in results['queries'][queries[i]['name']]['matches']:
            for i in range(1,len(metadata["locations"])):
                print("CHECK:")
                print("IS THIS:", res)
                print("IN HERE", metadata["locations"]["location"][str(i)]['true_match'])
                if res in metadata["locations"]["location"][str(i)]['true_match']:
                    results['queries'][queries[i]['name']]["TP"] += 1
                else:
                    results['queries'][queries[i]['name']]["FP"] += 1
        
        for i in range (1,len(metadata['locations'])):
            for opt in metadata["locations"]["location"][str(i)]['true_match']:
                if opt not in res:
                    results['queries'][queries[q]['name']]["FN"] += 1
                else:
                    results['queries'][queries[q]['name']]["TN"] = (len(metadata["locations"])-(results['queries'][queries[i]['name']]["TP"]+results['queries'][queries[i]['name']]["FP"]+results['queries'][queries[i]['name']]["FN"]))
        '''




    print("Finished Experiments")

    print("\n\n# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #")
    print("# Printing Timing Report:")
    print("#-------------------------------------------------------------")
    print("# EXPERIMENT:", flags.experimentName)
    print("#-------------------------------------------------------------")
    for k,v in times['overall'].items():
        print("#",k,"\t",v)
    print("#-------------------------------------------------------------")
    for query in times['queries'].keys():
        times['queries'][query]['total'] = times['queries'][query]["end  "]-times['queries'][query]["start"]
        print("#",query,"\t",times['queries'][query]['total'])
    print("# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #\n")

    print("\n# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #")
    print("# Printing Accuracy Report:")
    print("#-------------------------------------------------------------")
    print("# EXPERIMENT:", flags.experimentName)
    print("#-------------------------------------------------------------")
    for query in results['queries']:
        print(results['queries'][query])
    print("#-------------------------------------------------------------")
    
    print("# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #\n\n")

    #json_formatted_str = json.dumps(metadata, indent=2)

    #print(json_formatted_str)