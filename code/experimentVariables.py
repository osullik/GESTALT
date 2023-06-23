#VARIABLES

import argparse, pickle, json, time

from search import InvertedIndex
from conceptMapping import ConceptMapper



class Experimenter():
    def __init__(self, invertedIndexFile, referenceLocations, conceptMapFile):
        
        self.invertedIndex = InvertedIndex(invertedIndexFile)

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
        self.LO_experimentsDict = { "1":{"northwest":["crossing"],
                                        "northeast":[],
                                        "southwest":[],
                                        "southeast":[]},

                                    "2":{"northwest":["crossing"],
                                        "northeast":["traffic_signals"],
                                        "southwest":[],
                                        "southeast":[]},

                                    "3":{"northwest":["crossing"],
                                        "northeast":["traffic_signals"],
                                        "southwest":["stop"],
                                        "southeast":[]},

                                    "4":{"northwest":["crossing"],
                                        "northeast":["traffic_signals"],
                                        "southwest":["stop"],
                                        "southeast":["tree"]},

                                    "5":{"northwest":["crossing","kerb"],
                                        "northeast":["traffic_signals"],
                                        "southwest":["stop"],
                                        "southeast":["tree"]},

                                    "6":{"northwest":["crossing","kerb"],
                                        "northeast":["traffic_signals", "street_lamp"],
                                        "southwest":["stop"],
                                        "southeast":["tree"]},

                                    "7":{"northwest":["crossing","kerb"],
                                        "northeast":["traffic_signals", "street_lamp"],
                                        "southwest":["stop","person"],
                                        "southeast":["tree"]},

                                    "8":{"northwest":["crossing","kerb"],
                                        "northeast":["traffic_signals", "street_lamp"],
                                        "southwest":["stop","person"],
                                        "southeast":["tree", "bus_stop"]},

                                    "9":{"northwest":["crossing","kerb", "gate"],
                                        "northeast":["traffic_signals", "street_lamp"],
                                        "southwest":["stop","person"],
                                        "southeast":["tree", "bus_stop"]},

                                    "10":{"northwest":["crossing","kerb", "gate"],
                                        "northeast":["traffic_signals", "street_lamp", "bollard"],
                                        "southwest":["stop","person"],
                                        "southeast":["tree", "bus_stop"]
                                        }
                                }     

        self.OO_experimentsDict = {}
        self.OO_experimentsDict = { "1":["crossing"],

                                    "2":["crossing","traffic_signals"],

                                    "3":["crossing","traffic_signals","stop"],

                                    "4":["crossing","traffic_signals","stop","tree"],

                                    "5":["crossing","traffic_signals","stop","tree","kerb"],

                                    "6":["crossing","traffic_signals","stop","tree","kerb","street_lamp"],

                                    "7":["crossing","traffic_signals","stop","tree","kerb","street_lamp","person"],

                                    "8":["crossing","traffic_signals","stop","tree","kerb","street_lamp","person","bus_stop"],

                                    "9":["crossing","traffic_signals","stop","tree","kerb","street_lamp","person","bus_stop","gate"],

                                    "10":["crossing","traffic_signals","stop","tree","kerb","street_lamp","person","bus_stop","gate","bollard"]
                                }                       

        
    def runLoExperiments(self):
        for experiment in self.LO_experimentsDict.keys():
            locationHitCounter = {}
            start_wall_time = time.time()
            start_proc_time=time.process_time()
            for quadrant in self.LO_experimentsDict[experiment].keys():
                for loc in self.referenceLocations:
                    for item in self.LO_experimentsDict[experiment][quadrant]:
                        if item in self.referenceLocations[loc][quadrant]:
                            try:
                                locationHitCounter[loc] +=1
                            except KeyError:
                                locationHitCounter[loc] = 1
                        else:
                            pass
            end_proc_time=time.process_time()
            end_wall_time = time.time()
            print("\nReturned", len(locationHitCounter), "candicate locations for query:",self.LO_experimentsDict[experiment].items() )
            print("PROCESSOR TIME TO EXECUTE PICTORIAL LO QUERY #:", experiment, "was", end_proc_time-start_proc_time)
            print("WALL TIME TAKEN TO EXECUTE PICTORIAL LO QUERY #:", "was",end_wall_time-start_wall_time,"\n")
            #for loc in locationHitCounter.keys():
            #   print(loc,locationHitCounter[loc])

    def runOoExperiments(self):
        for experiment in self.OO_experimentsDict.keys():
            start_wall_time = time.time()
            start_proc_time=time.process_time()

            results = []
            for locationCM in self.conceptMaps.keys():
                result = self.CM.searchMatrix(self.conceptMaps[locationCM],self.OO_experimentsDict[experiment].copy())   #Don't forget to take a copy of the list... 
                if result == True: 
                    results.append(locationCM)
                    result = False
            
            #if len(results) ==0:                                            #Output. TODO: Use Popup window to output
            #    print('No Results Found')
            #else:
            #    print("Found Following Matches to Query:")
            #    for res in results: 
            #        print(res)

            end_proc_time=time.process_time()
            end_wall_time = time.time()
            print("\nReturned", len(results), "candicate locations for query:", self.OO_experimentsDict[experiment] )
            print("PROCESSOR TIME TO EXECUTE PICTORIAL OO QUERY #:", experiment, "was", end_proc_time-start_proc_time)
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
    

    flags = argparser.parse_args()

    madScientist = Experimenter(invertedIndexFile=flags.inputFile, referenceLocations=flags.locationsFile, conceptMapFile=flags.conceptMapFile)

    #madScientist.runLoExperiments()
    madScientist.runOoExperiments()