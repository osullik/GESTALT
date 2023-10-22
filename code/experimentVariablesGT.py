import argparse, pickle, json, time, sys, os
import pandas as pd

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
        self.CM = ConceptMapper()

        with open(referenceLocations, "r") as inFile:
                self.referenceLocations = json.load(inFile)

        with open(conceptMapFile, "rb") as inFile:
                self.conceptMaps = pickle.load(inFile)

        self.LO_experimentsDict = {}
        with open('../data/SV/ground_truth_queries/Location-Centric_ground_truth_queries.json') as f:
            self.LO_experimentsDict = json.load(f)
        with open('../data/SV/ground_truth_queries/Location-Centric_ground_truth_results.json') as f:    
            self.LO_experimentsResultsDict = json.load(f)        

        self.OO_experimentsDict = {}
        with open('../data/SV/ground_truth_queries/Object-Centric_ground_truth_queries.json') as f:
            self.OO_experimentsDict = json.load(f)
        with open('../data/SV/ground_truth_queries/Object-Centric_ground_truth_results.json') as f:    
            self.OO_experimentsResultsDict = json.load(f)

        self.OOI_experimentsDict = {}
        with open('../data/SV/ground_truth_queries/Object-Centric-Inv_ground_truth_queries.json') as f:
            self.OOI_experimentsDict = json.load(f)
        with open('../data/SV/ground_truth_queries/Object-Centric-Inv_ground_truth_results.json') as f:    
            self.OOI_experimentsResultsDict = json.load(f)

   
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
    
    def compareLocStructures(self, a, b):
        matches = 0
        for quadrant in a:
            matches += len(set(a[quadrant]).intersection(set(b[quadrant])))
        return matches

    def runLoExperiments(self):
        running_precision = 0
        running_recall = 0
        for i, experiment in enumerate(self.LO_experimentsDict.keys()):
            start_wall_time = time.time()
            start_proc_time=time.process_time()
            locationHitCounter = {}
            for loc in self.referenceLocations:
                matches = self.compareLocStructures(self.referenceLocations[loc], self.LO_experimentsDict[experiment])
                if matches > 0:
                    locationHitCounter[loc] = matches

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

        print("OVERALL PRECISION: ", running_precision/len(self.LO_experimentsDict.keys()))
        print("OVERALL RECALL: ", running_recall/len(self.LO_experimentsDict.keys()))

    def runOoExperiments(self):
        running_precision = 0
        running_recall = 0
        for i, experiment in enumerate(self.OO_experimentsDict):
            if i == 7:  # skip duplicate obejct query until fixed, check lines 266,267 if removing this
                continue
            print(self.OO_experimentsDict[experiment])
            names = self.OO_experimentsDict[experiment]['names']
            lats = self.OO_experimentsDict[experiment]['lats']
            longs = self.OO_experimentsDict[experiment]['longs']
            points = []
            preLocs = []
            for j in range(len(names)):
                pt = Point(name=names[j],
                        x_coord=longs[j],
                        y_coord=lats[j])
                points.append(pt)
                preLocs.append("PICTORIAL_QUERY")
            self.OO_experimentsDict[experiment]['point'] = points
            self.OO_experimentsDict[experiment]['preLocs'] = preLocs

            query_dict = {
                        "name":self.OO_experimentsDict[experiment]['names'], 
                        "longitude":self.OO_experimentsDict[experiment]['longs'], 
                        "latitude":self.OO_experimentsDict[experiment]['lats'],
                        "predicted_location":self.OO_experimentsDict[experiment]['preLocs']
                        }

            query_df = pd.DataFrame(data=query_dict)
            actual_results = []

            #Cardinality Assumed to be north
            print("Querying experiment", i)
            for locationCM in self.conceptMaps.keys():
                cm_dict = self.ER.generateQueryMapDict(query=query_df)
                #print("CM_DICT", cm_dict)
                ##queryMap = cm_dict["PICTORIAL_QUERY"]["concept_map"].copy()
                searchOrder = cm_dict["PICTORIAL_QUERY"]["search_order"].copy()
                #print("SEARCHORDER", searchOrder)
                result = self.CM.searchMatrix(self.conceptMaps[locationCM],searchOrder.copy())
                if result == True: 
                    actual_results.append(locationCM)
                    result = False
            print("GESTALT said: ", actual_results)
            print("GT says: ", list(self.OO_experimentsResultsDict[experiment]))
            precision = self.precision(actual_results=set(actual_results), expected_results=set(self.OO_experimentsResultsDict[experiment]))
            running_precision += precision
            print("PRECISION: ", precision)
            recall = self.recall(actual_results=set(actual_results), expected_results=set(self.OO_experimentsResultsDict[experiment]))
            running_recall += recall
            print("RECALL: ", recall)
        
        print("OVERALL PRECISION: ", running_precision/(len(self.OO_experimentsDict.keys()) -1))  #minus 1 since skipping query 7
        print("OVERALL RECALL: ", running_recall/(len(self.OO_experimentsDict.keys()) -1)) #minus 1 since skipping query 7

    def runOoInvExperiments(self):
        running_precision = 0
        running_recall = 0
        for i, experiment in enumerate(self.OOI_experimentsDict):
            if i == 7:  # skip duplicate obejct query until fixed
                continue
            print(self.OOI_experimentsDict[experiment])
            names = self.OOI_experimentsDict[experiment]['names']
            lats = self.OOI_experimentsDict[experiment]['lats']
            longs = self.OOI_experimentsDict[experiment]['longs']
            points = []
            preLocs = []
            for j in range(len(names)):
                pt = Point(name=names[j],
                        x_coord=longs[j],
                        y_coord=lats[j])
                points.append(pt)
                preLocs.append("PICTORIAL_QUERY")
            self.OOI_experimentsDict[experiment]['point'] = points
            self.OOI_experimentsDict[experiment]['preLocs'] = preLocs

            query_dict = {
                        "name":self.OOI_experimentsDict[experiment]['names'], 
                        "longitude":self.OOI_experimentsDict[experiment]['longs'], 
                        "latitude":self.OOI_experimentsDict[experiment]['lats'],
                        "predicted_location":self.OOI_experimentsDict[experiment]['preLocs']
                        }

            query_df = pd.DataFrame(data=query_dict)
            actual_results = []

            print("Querying experiment", i)
            all_rotations = self.ER.getQueryMapConfigurations(points=self.OOI_experimentsDict[experiment]['point'])
            print("GOT", len(all_rotations), "ROTATIONS")

            for rotation in all_rotations:
                for locationCM in self.conceptMaps.keys():
                    result = self.CM.searchMatrix(self.conceptMaps[locationCM],rotation['PICTORIAL_QUERY']['search_order'].copy())
                    if result == True: 
                        actual_results.append(locationCM)
                        result = False

            print("GESTALT said: ", actual_results)
            print("GT says: ", list(self.OOI_experimentsResultsDict[experiment]))
            precision = self.precision(actual_results=set(actual_results), expected_results=set(self.OOI_experimentsResultsDict[experiment]))
            running_precision += precision
            print("PRECISION: ", precision)
            recall = self.recall(actual_results=set(actual_results), expected_results=set(self.OOI_experimentsResultsDict[experiment]))
            running_recall += recall
            print("RECALL: ", recall)
        
        print("OVERALL PRECISION: ", running_precision/(len(self.OOI_experimentsDict.keys()) -1))  #minus 1 since skipping query 7
        print("OVERALL RECALL: ", running_recall/(len(self.OOI_experimentsDict.keys()) -1)) #minus 1 since skipping query 7



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

    if flags.objectCentric and not flags.cardinalityInvariant:
        madScientist.runOoExperiments()

    if flags.objectCentric and flags.cardinalityInvariant:
        madScientist.runOoInvExperiments()