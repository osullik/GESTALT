#VARIABLES

import argparse, pickle, json, time, sys, os

import pandas as pd
# User file imports

sys.path.insert(1, os.getcwd()+"/../")
sys.path.insert(1, os.getcwd()+"/../compass")
sys.path.insert(1, os.getcwd()+"/../gestalt")
sys.path.insert(1, os.getcwd()+"/../utils")
sys.path.insert(1, os.getcwd()+"/../experiments")

sys.path.insert(1, os.getcwd()+"/../../data")

sys.path.insert(1, os.getcwd()+"/../code")
sys.path.insert(1, os.getcwd()+"/../code/compass")
sys.path.insert(1, os.getcwd()+"/../code/gestalt")
sys.path.insert(1, os.getcwd()+"/../code/utils")
sys.path.insert(1, os.getcwd()+"/../code/experiments")
sys.path.insert(1, os.getcwd()+"/../../data")

from compass import Point
from compass import Compass

from search import InvertedIndex
from conceptMapping import ConceptMapper
from exp_compass import CompassExperimentRunner





class Experimenter():
    def __init__(self, invertedIndexFile, referenceLocations, conceptMapFile, cardinality_invariant=False):
        
        self.invertedIndex = InvertedIndex(invertedIndexFile)
        self.cardinality_invariant = cardinality_invariant
        self.ER = CompassExperimentRunner()

        with open(referenceLocations, "r") as inFile:
                self.referenceLocations = json.load(inFile)

        with open(conceptMapFile, "rb") as inFile:
                self.conceptMaps = pickle.load(inFile)

        self.CM = ConceptMapper()

        '''
        Query Input:
                    name longitude latitude predicted_location
        0         crossing       259      105     PICTORAL_QUERY
        1  traffic_signals       179      201     PICTORAL_QUERY
        2             stop       196      114     PICTORAL_QUERY
        3             tree       225      121     PICTORAL_QUERY
        4             kerb       270      164     PICTORAL_QUERY
        5      street_lamp       346      187     PICTORAL_QUERY
        6           person       333      108     PICTORAL_QUERY
        7         bus_stop       223      122     PICTORAL_QUERY
        8             gate       336      103     PICTORAL_QUERY
        9          bollard       223      147     PICTORAL_QUERY
        '''
        self.LO_experimentsDict = {}
        with open('../data/SV/ground_truth_queries/Location-Centric_ground_truth_queries.json') as f:
            self.LO_experimentsDict = json.load(f)

        with open('../data/SV/ground_truth_queries/Location-Centric_ground_truth_results.json') as f:    
            self.LO_experimentsResultsDict = json.load(f)

        # self.LO_experimentsDict = { "1":{"northwest":["crossing"],
        #                                 "northeast":[],
        #                                 "southwest":[],
        #                                 "southeast":[]},

        #                             "2":{"northwest":["crossing"],
        #                                 "northeast":["traffic_signals"],
        #                                 "southwest":[],
        #                                 "southeast":[]},

        #                             "3":{"northwest":["crossing"],
        #                                 "northeast":["traffic_signals"],
        #                                 "southwest":["stop"],
        #                                 "southeast":[]},

        #                             "4":{"northwest":["crossing"],
        #                                 "northeast":["traffic_signals"],
        #                                 "southwest":["stop"],
        #                                 "southeast":["tree"]},

        #                             "5":{"northwest":["crossing","kerb"],
        #                                 "northeast":["traffic_signals"],
        #                                 "southwest":["stop"],
        #                                 "southeast":["tree"]},

        #                             "6":{"northwest":["crossing","kerb"],
        #                                 "northeast":["traffic_signals", "street_lamp"],
        #                                 "southwest":["stop"],
        #                                 "southeast":["tree"]},

        #                             "7":{"northwest":["crossing","kerb"],
        #                                 "northeast":["traffic_signals", "street_lamp"],
        #                                 "southwest":["stop","person"],
        #                                 "southeast":["tree"]},

        #                             "8":{"northwest":["crossing","kerb"],
        #                                 "northeast":["traffic_signals", "street_lamp"],
        #                                 "southwest":["stop","person"],
        #                                 "southeast":["tree", "bus_stop"]},

        #                             "9":{"northwest":["crossing","kerb", "gate"],
        #                                 "northeast":["traffic_signals", "street_lamp"],
        #                                 "southwest":["stop","person"],
        #                                 "southeast":["tree", "bus_stop"]},

        #                             "10":{"northwest":["crossing","kerb", "gate"],
        #                                 "northeast":["traffic_signals", "street_lamp", "bollard"],
        #                                 "southwest":["stop","person"],
        #                                 "southeast":["tree", "bus_stop"]
        #                                 }
        #                         }     

        self.OO_experimentsDict = {}

        '''
        Query Input:
                    name longitude latitude predicted_location
        0         crossing       259      105     PICTORAL_QUERY
        1  traffic_signals       179      201     PICTORAL_QUERY
        2             stop       196      114     PICTORAL_QUERY
        3             tree       225      121     PICTORAL_QUERY
        4             kerb       270      164     PICTORAL_QUERY
        5      street_lamp       346      187     PICTORAL_QUERY
        6           person       333      108     PICTORAL_QUERY
        7         bus_stop       223      122     PICTORAL_QUERY
        8             gate       336      103     PICTORAL_QUERY
        9          bollard       223      147     PICTORAL_QUERY
        '''

        self.OO_experimentsDict =   {0:{
                                        "name":"crossing",
                                        "longitude":259,
                                        "latitude":105,
                                        "predicted_location": "PICTORAL_QUERY"},
                                    1:{
                                        "name":"traffic_signals",
                                        "longitude":179,
                                        "latitude":201,
                                        "predicted_location": "PICTORAL_QUERY"},
                                    2:{
                                        "name":"stop",
                                        "longitude":196,
                                        "latitude":114,
                                        "predicted_location": "PICTORAL_QUERY"},
                                    3:{
                                        "name":"tree",
                                        "longitude":225,
                                        "latitude":121,
                                        "predicted_location": "PICTORAL_QUERY"},
                                    4:{
                                        "name":"kerb",
                                        "longitude":270,
                                        "latitude":164,
                                        "predicted_location": "PICTORAL_QUERY"},
                                    5:{
                                        "name":"street_lamp",
                                        "longitude":346,
                                        "latitude":187,
                                        "predicted_location": "PICTORAL_QUERY"},
                                    6:{
                                        "name":"person",
                                        "longitude":333,
                                        "latitude":108,
                                        "predicted_location": "PICTORAL_QUERY"},
                                    7:{
                                        "name":"bus_stop",
                                        "longitude":223,
                                        "latitude":122,
                                        "predicted_location": "PICTORAL_QUERY"},
                                    8:{
                                        "name":"gate",
                                        "longitude":336,
                                        "latitude":103,
                                        "predicted_location": "PICTORAL_QUERY"},
                                    9:{
                                        "name":"bollard",
                                        "longitude":223,
                                        "latitude":147,
                                        "predicted_location": "PICTORAL_QUERY"},  
                                        }

        '''self.OO_experimentsDict = { "1":["crossing"],

                                    "2":["crossing","traffic_signals"],

                                    "3":["crossing","traffic_signals","stop"],

                                    "4":["crossing","traffic_signals","stop","tree"],

                                    "5":["crossing","traffic_signals","stop","tree","kerb"],

                                    "6":["crossing","traffic_signals","stop","tree","kerb","street_lamp"],

                                    "7":["crossing","traffic_signals","stop","tree","kerb","street_lamp","person"],

                                    "8":["crossing","traffic_signals","stop","tree","kerb","street_lamp","person","bus_stop"],

                                    "9":["crossing","traffic_signals","stop","tree","kerb","street_lamp","person","bus_stop","gate"],

                                    "10":["crossing","traffic_signals","stop","tree","kerb","street_lamp","person","bus_stop","gate","bollard"]
                                } '''                      

    def precision(self, expected_results:set, actual_results:set):
        correct = len(expected_results.intersection(actual_results))
        if len(actual_results) == 0:
            return 1.0
        return correct/len(actual_results)
    
    def recall(self, expected_results:set, actual_results:set):
        correct = len(expected_results.intersection(actual_results))   
        if len(expected_results) == 0:
            return 1.0
        return correct/len(expected_results)

    def runLoExperiments(self):
        running_precision = 0
        running_recall = 0
        for i, experiment in enumerate(self.LO_experimentsDict.keys()):
            locationHitTracker = {}
            start_wall_time = time.time()
            start_proc_time=time.process_time()
            for quadrant in self.LO_experimentsDict[experiment].keys():
                for loc in self.referenceLocations:
                    for item in self.LO_experimentsDict[experiment][quadrant]:
                        if item in self.referenceLocations[loc][quadrant]:
                            try:
                                locationHitTracker[loc].add(item)
                            except KeyError:
                                locationHitTracker[loc] = {item}
                        else:
                            pass

            locationHitCounter = {}
            for loc in locationHitTracker:
                locationHitCounter[loc] = len(locationHitTracker[loc])

            end_proc_time=time.process_time()
            end_wall_time = time.time()
            print("\nReturned", len(locationHitCounter), "candidate locations for query:",self.LO_experimentsDict[experiment].items() )

            querylist = [self.LO_experimentsDict[experiment][x] for x in self.LO_experimentsDict[experiment]]
            num_query_terms = len(querylist[0]) + len(querylist[1]) + len(querylist[2]) + len(querylist[3])

            actual_results = []
            for loc in locationHitCounter:
                if locationHitCounter[loc] == num_query_terms:
                    actual_results.append(loc)

            print("GESTALT said: ", actual_results)
            print("GT says: ", list(self.LO_experimentsResultsDict[experiment]))
            print(locationHitCounter)
            
            precision = self.precision(actual_results=set(actual_results), expected_results=set(self.LO_experimentsResultsDict[experiment]))
            running_precision += precision
            print("PRECISION: ", precision)
            recall = self.recall(actual_results=set(actual_results), expected_results=set(self.LO_experimentsResultsDict[experiment]))
            running_recall += recall
            print("RECALL: ", recall)
            print("PROCESSOR TIME TO EXECUTE PICTORIAL LO QUERY #:", experiment, "was", end_proc_time-start_proc_time)
            print("WALL TIME TAKEN TO EXECUTE PICTORIAL LO QUERY #:", "was",end_wall_time-start_wall_time,"\n")
            #for loc in locationHitCounter.keys():
            #   print(loc,locationHitCounter[loc])
        print("OVERALL PRECISION: ", running_precision/len(self.LO_experimentsDict.keys()))
        print("OVERALL RECALL: ", running_recall/len(self.LO_experimentsDict.keys()))

    def runOoExperiments(self):

        for i in range(0, len(self.OO_experimentsDict.keys())):
                pt = Point(name=self.OO_experimentsDict[i]['name'],
                            x_coord=self.OO_experimentsDict[i]['longitude'],
                            y_coord=self.OO_experimentsDict[i]['latitude'])
                self.OO_experimentsDict[i]['point'] = pt

        #Format for the cardinality dependent queries
        names = []
        lats = []
        longs = []
        preLocs = []
        pts = []
        for i in range(0, len(self.OO_experimentsDict.keys())):
            names.append(self.OO_experimentsDict[i]['name'])
            longs.append(self.OO_experimentsDict[i]['longitude'])
            lats.append(self.OO_experimentsDict[i]['latitude'])
            preLocs.append("PICTORIAL_QUERY")
            pts.append(self.OO_experimentsDict[i]['point'])

        query_dict =    {
                        "name":names, 
                        "longitude":longs, 
                        "latitude":lats,
                        "predicted_location":preLocs
                        }

        query_df = pd.DataFrame(data=query_dict)

        numQueryObjects = [1,2,3,4,5,6,7,8,9,10] 

        for i in range(len(numQueryObjects)): #build up the number of query terms over time. 
            
            expToRun = []
            points = []

            for j in range(0,numQueryObjects[i]):
                expToRun.append(self.OO_experimentsDict[j])
                points.append(self.OO_experimentsDict[j]['point'])  #Grow the number of points to rotate by one each experiment (invariant search only)
                exp_df = query_df.head(numQueryObjects[i])          #Grow the dataframe by one additional point each experiment (cardinal search only)
            #print("RUNNING", expToRun)

            results = []

            start_wall_time = time.time()
            start_proc_time=time.process_time()

            if self.cardinality_invariant == True:

                all_rotations = self.ER.getQueryMapConfigurations(points=points)
                print("GOT", len(all_rotations), "ROTATIONS")

                for rotation in all_rotations:
                    for locationCM in self.conceptMaps.keys():
                        result = self.CM.searchMatrix(self.conceptMaps[locationCM],rotation['PICTORIAL_QUERY']['search_order'].copy())   #Don't forget to take a copy of the list... 
                        if result == True: 
                            results.append(locationCM)
                            result = False

            else:
                #Cardinality Assumed to be north
                print("Querying experiment", i)
                for locationCM in self.conceptMaps.keys():
                    cm_dict = self.ER.generateQueryMapDict(query=exp_df)
                    #print("CM_DICT", cm_dict)
                    queryMap = cm_dict["PICTORIAL_QUERY"]["concept_map"].copy()
                    searchOrder = cm_dict["PICTORIAL_QUERY"]["search_order"].copy()
                    #print("SEARCHORDER", searchOrder)
                    result = self.CM.searchMatrix(self.conceptMaps[locationCM],searchOrder.copy())   #Don't forget to take a copy of the list... 
                    if result == True: 
                        results.append(locationCM)
                        result = False
            

            end_proc_time=time.process_time()
            end_wall_time = time.time()
            print("\nReturned", len(results), "candicate locations for query:" )
            print("PROCESSOR TIME TO EXECUTE PICTORIAL OO QUERY #:", i, "was", end_proc_time-start_proc_time)
            print("WALL TIME TAKEN TO EXECUTE PICTORIAL OO QUERY #:", "was",end_wall_time-start_wall_time,"\n")


if __name__=="__main__":

    argparser = argparse.ArgumentParser()									# initialize the argParser
    
    argparser.add_argument(	"-if", "--inputFile", 							
                            help="The file used to buid an inverted index, should be a CSV with location predictions",
                            type=str,
                            default=None,
                            required=True)	
    
    argparser.add_argument(	"-cmf", "--conceptMapFile", 							
                            help="The File that stores all the concept Maps, should be a PKL file with location predictions",
                            type=str,
                            default=None,
                            required=True)	
    
    argparser.add_argument(	"-lf", "--locationsFile", 							
                            help="The File that holds the reference locations for the query interface",
                            type=str,
                            default=None,
                            required=True)	

    argparser.add_argument( "--cardinalityInvariant",
                            help="Tell the system to query in cardinality invariant mode",
                            default=False,
                            action="store_true", 
                            required=False)
    
    argparser.add_argument( "--locationCentric",
                            help="Tell the system to query in Location-centric mode",
                            default=False,
                            action="store_true", 
                            required=False)
    
    argparser.add_argument( "--objectCentric",
                            help="Tell the system to query in Location-centric mode",
                            default=False,
                            action="store_true", 
                            required=False)
    

    flags = argparser.parse_args()

    madScientist = Experimenter(invertedIndexFile=flags.inputFile, 
                                referenceLocations=flags.locationsFile, 
                                conceptMapFile=flags.conceptMapFile, 
                                cardinality_invariant=flags.cardinalityInvariant)

    if flags.locationCentric:
        madScientist.runLoExperiments()

    if flags.objectCentric:
        madScientist.runOoExperiments()