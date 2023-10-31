#Author: Kent O'Sullivan
#Email: osullik@umd.edu

# System Imports
import sys
import os
import argparse
import json
import pickle
import datetime
import gc

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
from quadrantMapConverter import QuadrantMapConverter

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

        queriesDict = self.cm.createConceptMap(input_df=query,cm_type='query')

        dictWithSortOrders = {}

        for key in queriesDict.keys():
            cm = queriesDict[key][0]
            orderLists = queriesDict[key][1]
            lonList, latList = orderLists
            searchOrder = self.cm.getSearchOrder(longSortedList=lonList, latSortedList=latList)
            dictWithSortOrders[key] = {}
            dictWithSortOrders[key]['concept_map'] = cm
            dictWithSortOrders[key]['search_order'] = searchOrder
        
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
                res = self.cm.searchMatrix(matrix=searchLocs[loc], toFind=query_searchOrder.copy())
                if res == True:
                    results.append(loc)

        else:
            res = self.cm.searchMatrix(matrix=query_cm, toFind=query_searchOrder.copy())
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
        
        for loc in self._cm_dict.keys():

            for queryDict in queries:
                query = queryDict["PICTORIAL_QUERY"]['concept_map']
                searchOrder = queryDict["PICTORIAL_QUERY"]['search_order']
                
                result = self.cm.searchMatrix(self._cm_dict[loc],searchOrder.copy())   #Don't forget to take a copy of the list... 
                if result == True: 
                    results.append(loc)
                    result = False
                    break
        
        return (results)

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
        cm = self.ER.getConceptMapDict()[name] #BUG workaround - just return whole dict

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


        qm = self.ER.loadQueries(df)[name]

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
    
    argparser.add_argument("--searchMode",
                            help="Specify either object_object or location_object",
                            default="object_object",
                            required = False)
    
    times = {} #Dict to hold timing data for experiments
    results = {} #Dict to hold results for experiments


    flags = argparser.parse_args()

    if flags.cardinalityInvariant == True:
        expName = flags.experimentName+" cardinality_invariant"
    else:
        expName = flags.experimentName

    print("\n\n# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #")
    print("Starting Experiment -", expName)
    print("# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #\n\n")


    DL = CompassDataLoader(flags.experimentName)
    ER = CompassExperimentRunner()

    location_files, query_files, metadata_file = DL.getExperimentFiles(experimentName=flags.experimentName)

    with open(metadata_file,'r') as infile:
        metadata = json.load(infile)
    
    if metadata['parameters']['numQueryTerms'] >= 1000:
        recursionDepth = ((metadata['parameters']['numQueryTerms'])*2)
        sys.setrecursionlimit(recursionDepth)
        print("Query is likely to exceed max recursion depth, setting to ", recursionDepth)


    locations = []

    print("Loading in location files")
    for location_file in tqdm(location_files):
        DL.loadLocationCSVToConceptMap(location_file) #Loads to the dict in the class
    ER._cm_dict = DL.ER.getConceptMapDict()
    
    queries = {}
    print("Loading in query Files")
    for i in tqdm(range(0,len(query_files))):
        q_path = query_files[i].split("/")
        q_name = q_path[-1].split(".")[0]
        
        query_df = DL.loadCSV(query_files[i])
        if "predicted_location" not in query_df:
            query_df['predicted_location'] = q_name
        if "object_prob" not in query_df:
            query_df['object_prob'] = 1
        if "assignment_prob" not in query_df:
            query_df['assignment_prob'] = 1
        points = []
        
        for idx, row in query_df.iterrows():
            points.append(Point(name=row['name'], x_coord=row['longitude'], y_coord=row['latitude']))

        queryMapDict = ER.generateQueryMapDict(query=query_df)
        queryMap = queryMapDict[q_name]["concept_map"].copy()
        searchOrder = queryMapDict[q_name]["search_order"].copy()
        queries[i+1] = {} 
        queries[i+1]['name'] = q_name
        queries[i+1]["queryMap"] = queryMap.copy()
        queries[i+1]["searchOrder"] = searchOrder.copy()
        queries[i+1]["points"] = points.copy()
        queries[i+1]["dataframe"] = query_df #Allow us to generate the cocnept maps in the timed section of code. 
        

    

    print("\n#####_BEGINNING_SEARCH_#####\n")
    times['overall'] = {}
    times['queries'] = {}
    results['queries'] = {}

    times['overall']["start"] = datetime.datetime.now()

    if flags.searchMode == "object_object":

        if flags.cardinalityInvariant is False:
            for i in tqdm(range(1,len(queries)+1)):
                results['queries'][queries[i]['name']] = {}
                results['queries'][queries[i]['name']]["TP"] = 0
                results['queries'][queries[i]['name']]['FP'] = 0
                results['queries'][queries[i]['name']]['TN'] = 0
                results['queries'][queries[i]['name']]['FN'] = 0
                results['queries'][queries[i]['name']]['num_rotations'] = 1
                times['queries'][queries[i]['name']] = {}
                times['queries'][queries[i]['name']]['start'] = datetime.datetime.now()
                

                queryMapDict = ER.generateQueryMapDict(query=queries[i]["dataframe"])
                queryMap = queryMapDict[queries[i]['name']]["concept_map"].copy()
                searchOrder = queryMapDict[queries[i]['name']]["search_order"].copy()
                times['queries'][queries[i]['name']]['cm_complete'] = datetime.datetime.now()
                res = ER.gridSearchSingleQuery(query_searchOrder=queries[i]['searchOrder'])
                results['queries'][queries[i]['name']]['matches'] = res
                times['queries'][queries[i]['name']]["end  "] = datetime.datetime.now()

        #Generate All possible rotations
        else:
            for i in tqdm(range(1,len(queries)+1)):
                results['queries'][queries[i]['name']] = {}
                results['queries'][queries[i]['name']]["TP"] = 0
                results['queries'][queries[i]['name']]['FP'] = 0
                results['queries'][queries[i]['name']]['TN'] = 0
                results['queries'][queries[i]['name']]['FN'] = 0
                
                times['queries'][queries[i]['name']] = {}
                times['queries'][queries[i]['name']]['start'] = datetime.datetime.now()

                
                all_rotations = ER.getQueryMapConfigurations(points=queries[i]["points"])
                results['queries'][queries[i]['name']]['num_rotations'] = len(all_rotations)

                times['queries'][queries[i]['name']]['cm_complete'] = datetime.datetime.now()

                res = ER.gridSearchAllRotations(queries=all_rotations)
                results['queries'][queries[i]['name']]['matches'] = res
                times['queries'][queries[i]['name']]["end  "] = datetime.datetime.now()


    elif flags.searchMode == "location_object":

        print("Deleting Concept Maps")  #Workaround until refactoring (saves double memory alloc)
        del locations
        gc.collect()

        print("Building location quadrant maps...")
        QCM = QuadrantMapConverter()

        loc_quadrants = {}

        for location_file in tqdm(location_files):
            loc_path = location_file.split("/")
            loc_name = loc_path[-1].split(".")[0]
            df = pd.read_csv(location_file, sep=",")
            loc_quadrants[loc_name] = QCM.generateQuadrantMap(input_df=df)
            

        
        if flags.cardinalityInvariant is False:
            print("Running Queries...")
            for i in tqdm(range(1,len(queries)+1)):
                results['queries'][queries[i]['name']] = {}
                results['queries'][queries[i]['name']]["TP"] = 0
                results['queries'][queries[i]['name']]['FP'] = 0
                results['queries'][queries[i]['name']]['TN'] = 0
                results['queries'][queries[i]['name']]['FN'] = 0
                results['queries'][queries[i]['name']]['num_rotations'] = 1
                
                times['queries'][queries[i]['name']] = {}
                times['queries'][queries[i]['name']]['start'] = datetime.datetime.now()

                query_quadrant_dict = QCM.generateQuadrantMap(queries[i]['dataframe'])
                times['queries'][queries[i]['name']]['cm_complete'] = datetime.datetime.now()

                locationHitCounter = {}

                #print("\n##########")
                #print("REFS", loc_quadrants)
                #print("QUERY", query_quadrant_dict)
                #print("##########\n")

                for loc in loc_quadrants:
                    for quadrant in ['northwest', 'northeast','southwest','southeast']:
                        for item in query_quadrant_dict[quadrant]:
                            if str(item) in loc_quadrants[loc][quadrant]:
                                try:
                                    locationHitCounter[loc] +=1
                                except KeyError:
                                    locationHitCounter[loc] = 1
                                #print(loc,"True")
                            else:
                                pass
                                #print(loc,"False")
                            try: 
                                locationHitCounter[loc]
                            except KeyError:
                                locationHitCounter[loc] = 0
                res = []
                for l in locationHitCounter.keys():
                    if locationHitCounter[l] == metadata['parameters']['numQueryTerms']:
                        res.append(l)
                
                results['queries'][queries[i]['name']]['matches'] = res
                times['queries'][queries[i]['name']]["end  "] = datetime.datetime.now()


    else:
        exit("NO SEARCH MODE SELECTED")

    times['overall']["end  "] = datetime.datetime.now()
    times['overall']["total"] = times['overall']["end  "]-times['overall']["start"]

    print('Generating Accuracy Report...')

    #print(results)
    for queryNum in tqdm(metadata['queries']['query'].keys()):

        if metadata['queries']['query'][queryNum]['true_match'] in results['queries'][metadata['queries']['query'][queryNum]['name']]['matches']:
            results['queries'][metadata['queries']['query'][queryNum]['name']]["TP"] += 1
        else:
            results['queries'][metadata['queries']['query'][queryNum]['name']]["FN"] += 1

        for found in results['queries'][metadata['queries']['query'][queryNum]['name']]['matches']:
            if found != metadata['queries']['query'][queryNum]['true_match']:
                results['queries'][metadata['queries']['query'][queryNum]['name']]["FP"] += 1
            
            results['queries'][metadata['queries']['query'][queryNum]['name']]["TN"] = (metadata['locations']['num_locations'] - (results['queries'][metadata['queries']['query'][queryNum]['name']]["TP"] + results['queries'][metadata['queries']['query'][queryNum]['name']]["FP"] + results['queries'][metadata['queries']['query'][queryNum]['name']]["FN"]))
        
        if len(results['queries'][metadata['queries']['query'][queryNum]['name']]['matches']) == 0:
            results['queries'][metadata['queries']['query'][queryNum]['name']]["TN"] = (metadata['locations']['num_locations'] - (results['queries'][metadata['queries']['query'][queryNum]['name']]["TP"] + results['queries'][metadata['queries']['query'][queryNum]['name']]["FP"] + results['queries'][metadata['queries']['query'][queryNum]['name']]["FN"]))

    

    print("Finished Experiments")



    print("\n\n# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #")
    print("# Printing Timing Report:")
    print("#-------------------------------------------------------------")
    print("# EXPERIMENT:", expName)
    print("#-------------------------------------------------------------")
    for k,v in times['overall'].items():
        print("#",k,"\t",v)
    print("#-------------------------------------------------------------")
    for query in times['queries'].keys():
        times['queries'][query]['make_cm'] = times['queries'][query]["cm_complete"]-times['queries'][query]["start"]
        times['queries'][query]['search'] = times['queries'][query]["end  "]-times['queries'][query]["cm_complete"]
        times['queries'][query]['total'] = times['queries'][query]["end  "]-times['queries'][query]["start"]
        print("#",query,"Concept Mapping","\t",times['queries'][query]['make_cm'])
        print("#",query,"Searching      ","\t",times['queries'][query]['search'])
        print("#",query,"Total          ","\t",times['queries'][query]['total'])
    print("# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #\n")

    print("\n# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #")
    print("# Printing Accuracy Report:")
    print("#-------------------------------------------------------------")
    print("# EXPERIMENT:", expName)
    print("#-------------------------------------------------------------")
    for query in results['queries']:
        print(query,results['queries'][query])
    print("#-------------------------------------------------------------")
    
    print("# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #\n\n")

    experiment_results = {}
    experiment_results['times'] = times
    experiment_results['results'] = results

    #print(experiment_results)

    dataDirectory = ""
    for p in sys.path:
        if p.endswith("data"):
            dataDirectory = p
    
    assert dataDirectory in sys.path,"Unable to find the 'GESTALT/data' directory - does it exist?"

    experimentsDirectoryPath = os.path.join(dataDirectory, "experiments")
    assert  os.path.exists(experimentsDirectoryPath),"'data/experiments' does not exist." 

    experimentDirectoryPath = os.path.join(experimentsDirectoryPath, flags.experimentName)
    
    if os.path.exists(experimentDirectoryPath) == False:
        os.mkdir(experimentDirectoryPath)
    
    assert  os.path.exists(experimentDirectoryPath),"'data/experiments/'"+flags.experimentName+" does not exist." 

    if flags.searchMode == 'location_object':
        savePath = os.path.join(experimentDirectoryPath,flags.experimentName)+"location_"
    else:
        savePath = os.path.join(experimentDirectoryPath,flags.experimentName)

    if flags.cardinalityInvariant == True:
        savePath += "cardinality_invariant_results.pkl"
    else:
        savePath += "results.pkl"

    with open(savePath, "wb") as outfile:
        pickle.dump(experiment_results,outfile)
