#Author: Kent O'Sullivan
#Email: osullik@umd.edu

# System Imports
import sys
import os
import unittest
import random
import string 
import argparse
# Library Imports
import pandas as pd
import numpy as np
import networkit as nk
import matplotlib.pyplot as plt

# User file imports

sys.path.insert(1, os.getcwd()+"/../")
sys.path.insert(1, os.getcwd()+"/../compass")
sys.path.insert(1, os.getcwd()+"/../gestalt")
sys.path.insert(1, os.getcwd()+"/../experiments")

from compass import Point, Compass
from conceptMapping import ConceptMapper
from search import InvertedIndex
from exp_compass import CompassExperimentRunner, CompassDataLoader

class DataGenerator():
    def __init__(self):
        self.compass = Compass()
        pass

    def generateMatrix(self,scaleFactor:int,edgeFactor:int):
        '''
        PURPOSE:
            Generate a random matrix of using an RMAT generator, which generates 
            scale free graphs. We repurpose the adjacency matrix to randonly initialize
            the distribution of objects in our location to follow a power-law distribution
        INPUT ARGS:
            scaleFactor - int - the size of the matrix is n = 2^scaleFactor
            edgeFactor - int - the number of edges in the graph, calculated as m = n * edgeFactor
        PROCESS:
            Initialize an RMAT generator (the four float params determine how 'skewed' the distribution will be)
                we use the standard Kroneker distribution from Graph500 pending a more detailed study of how objects
                are positioned in reality.
            Convert into a sparse matrix
            Extract all the non-zero coordinates of the sparse matrix
        OUTPUT:
            points - list of tuples of form (x,y) 

        '''
        points = []

        #Initalize the generator
        rmat = nk.generators.RmatGenerator(scaleFactor, edgeFactor, 0.57, 0.19, 0.19, 0.05) #Parameters taken from Graph500
        rmatG = rmat.generate()

        #Generate a sparse matrix representaiton of the RMAT generated graph. 
        sm = nk.algebraic.adjacencyMatrix(rmatG,matrixType='sparse')

        #Extract row and column info from the sparse matrix and save each coordinate pair to a list
        row,col = sm.nonzero()    
        for r,c in zip(row,col):
            points.append((r,c))

        return(points)

    def labelNodes(self,points:list[tuple], numClasses:int, random_seed:int, queryTerms:dict=None)->dict:
        '''
        PURPOSE:
            Label each of the nodes generated by the RMAT algorithm to reflect the skewed-ness of real
            world distributions.
        INPUT ARGS:
            point - list of tuples of form (x,y) - the coordinates to insert a label to 
            numClasses - int - the number of distinct labels to use (e.g) a '3' would mean that all objects will
                be spread between only 3 classes
            random_seed - int - allows for replication of results; also used to determine the skewed-ness of the
                labelling distribution. Higher values will have a greater skew. 
            queryTerms - dict with keys [name, latitude, longitude] and values of lists where each index in the three
                lists corresponds to a single object. These are the query terms that we will insert to ensure 
                known true positives and false negatives in evaluation.
        PROCESSS:
            Using all of the letters of the english alphabet in lower case and caps (total: 52 classes) randomly select
                a subset to use as labels. 
            Use Numpy to generate an inverse Pareto distribution with 1000 samples. 
            For each coordinate that was passed to the function, add a label from the distribution generated, starting at
                the beginning if we have more than 1000 objects. However, if the coordinate is one of the query terms we want
                to insert, the query term will be inserted instead. 
            Add all the remaining 'query terms'
        OUTPUT
            namedPoints - dict of lists - has keys [name, latitude, longitude] and values of lists where each index in the three
                lists corresponds to a single object.
        
        '''

        RANDOM_POWER = random_seed  #the higher the random_seed value, the more skewed the power distribution
        SAMPLES = 1000
        np.random.seed(random_seed)
        random.seed(random_seed)

        namedPoints = {}
        classes = []
        labels = []
    
        #Randomly choose labels to be in the labelList
        if numClasses > len(string.ascii_letters):
            print("Maximum number of classes is", len(string.ascii_letters), "setting numClasses to:", len(string.ascii_letters))
        while len(classes) < numClasses:
            classes.append(random.choice(string.ascii_letters))
        
        #Create a sample power-law distribution, and divide it into bins representing each possible class
        s = np.random.power(RANDOM_POWER, SAMPLES)
        count, bins, ignored = plt.hist(s, bins=numClasses-1)
        binList = np.digitize(s,bins)

        names = []
        longitudes = []
        latitudes = []

        #Extract query terms from their dictionary to something easier to work with
        if queryTerms is not None:
            terms = queryTerms.copy()
            names_copy = terms['names'].copy() #I don't know what this does but if I delete it everything breaks. 
            queryCoords = []
            for i in range(0, len(terms['name'])):
                queryCoords.append((terms['longitude'][i],terms['latitude'][i]))
        else:
            queryCoords = None
            
        #For each coordinate, assign it a label based on the power law distribution we generated. 
        #If a query point we want to insert exists at the same location, insert the query point instead

        for i in range(0, len(points)):
            coord = points[i]

            #Insert the query point if we need to
            if queryCoords is not None:
                found = []
                for q_coord in queryCoords:
                    if q_coord == coord:
                        names.append(terms['name'].copy()[queryCoords.index(q_coord)]) #Copy because lists are mutable...
                        longitudes.append(q_coord[0])
                        latitudes.append(q_coord[1])
                        found.append(q_coord)
                if len(found) != 0:
                    for f in found:
                        #print("TERMS_NAME", terms['name'])
                        #print("REMOVING",terms['name'][queryCoords.index(f)])
                        terms['name'].remove(terms['name'][queryCoords.index(f)]) 
                        queryCoords.remove(f)

            #Generate labels using the power law distro otherwise              
            
            #print("POINTS LENGTH", len(points))
            #print("BUINLIST LEN", len(binList))
            #print("CLASSES", classes)

            labelIndex = binList[i % len(binList)]  #Start at beginning if longer than list
            #print("BINLIST", binList)
            #print("LABELINDEX", labelIndex)
            #print("CLASSES", classes)
            try:  
                label = classes[labelIndex-1]
            except IndexError as e:
                #print("LABEL INDEX", labelIndex)
                label = classes[labelIndex] #Handle the modulo == 0 issue
            names.append(label)
            longitudes.append(coord[0])
            latitudes.append(coord[1])

        #Add any remaining query terms
        if queryCoords is not None:
            for x,y in queryCoords:
                names.append(terms['name'][queryCoords.index((x,y))])
                longitudes.append(x)
                latitudes.append(y)

        #Build the dictionary.
        namedPoints["name"] = names
        namedPoints["longitude"] = longitudes
        namedPoints["latitude"] = latitudes

        return(namedPoints)

    def saveToFile(self, experiment_name:str, saveType:str, number:int, data:dict):
        '''
        PURPOSE: 
            Save a generated location and/or query to disk. 
        INPUT ARGS: 
            experiment_name - string - the name of the experiment to be run - used to construct filepath
            saveType - string - either 'location' or 'query' - used to construct filepath
            number - int - the number of the location / query / experiment being generated
            data - dict of lists - has keys [name, latitude, longitude] and values of lists where each index in the three
                lists corresponds to a single object.
        PROCESS:
            If the directories don't exist, create them 
            Create the files
        OUTPUT:
            returns filePathToSave - string - the file path to where the file was saved
            the file that is saved to disk at 'GESTALT/data/experiments/experiment_name/saveType/saveType_number.csv'
        
        '''

        dataDirectory = ""
        for p in sys.path:
            if p.endswith("data"):
                dataDirectory = p
        
        assert dataDirectory in sys.path,"Unable to find the 'GESTALT/data' directory - does it exist?"

        experimentsDirectoryPath = os.path.join(dataDirectory, "experiments")
        assert  os.path.exists(experimentsDirectoryPath),"'data/experiments' does not exist." 

        experimentDirectoryPath = os.path.join(experimentsDirectoryPath, experiment_name)
        
        if os.path.exists(experimentDirectoryPath) == False:
            os.mkdir(experimentDirectoryPath)
        
        assert  os.path.exists(experimentDirectoryPath),"'data/experiments/'"+experiment_name+" does not exist." 

        typeDirectoryPath = os.path.join(experimentDirectoryPath, saveType)
        
        if os.path.exists(typeDirectoryPath) == False:
            os.mkdir(typeDirectoryPath)
        
        assert  os.path.exists(typeDirectoryPath),"'data/experiments/'"+experiment_name+saveType+" does not exist." 

        filePathToSave = typeDirectoryPath+"/"+saveType+str(number)+".csv"

        df_to_save = pd.DataFrame(data=data)

        df_to_save.to_csv(filePathToSave,sep=",",header=True,index=False)

        print("FILEPATHTOSAVE", filePathToSave)

        return(filePathToSave)

    def distortQuery(self, query_dict:dict,canvas_size:int, rotation_degrees:int=0, expansion:float=0, shift_vertical:float=0, shift_horizontal:float=0):
        '''
        PURPOSE:
            Given a query, apply distortions to rotation, expansion, and lateral shifts to change it while still 
            preserving the relative positioning between points
        INPUT ARGS:
            query_dict - dict of lists - has keys [name, latitude, longitude] and values of lists where each index in the three
                lists corresponds to a single object.
            canvas_size - int - assuming a square canvas will generate a canvas_size x canvas_size surface to work with. 
            rotation_degrees - int - number from 0 to 360 that rotates the query points (and snaps them to the grid) [INACTIVE when == 0]
            expansion - float - a number from - 0 to 1 that determines how far the query should "spread" from the centre of the
                canvas (all queries will centre on the centroid as a start point.) [INACTIVE when == 0]
            shift_vertical - float - a number from -1 to 1 that defines how far up or down the canvas the query term should shift, with the maximal
                shift being this value times the maximum y value [INACTIVE when == 0
            shift_horizontal - float - a number from -1 to 1 that defines how far left or right on the canvas the query term should shift, with the maximal
                shift being this value times the maximum x value [INACTIVE when == 0]
        PROCESS:
            Apply each transformation in turn, ignoring it if == 0
        OUTPUT:
            returnQuery - dict of lists - has keys [name, latitude, longitude] and values of lists where each index in the three
                lists corresponds to a single object.
        
        '''
        #Always follow same order: 
            #Rotate
            #Expand
            #Shift Up
            #Shift Sideways

        MIN_X = 0
        MIN_Y = 0
        MAX_X = canvas_size
        MAX_Y = canvas_size
        centroid = Point('centroid', (MAX_X/2),( MAX_Y/2))

        points = []

        #Make points
        for i in range(len(query_dict['name'])):
            points.append(Point(query_dict['name'][i], query_dict['longitude'][i], query_dict['latitude'][i]))

        p_ll, p_tr, p_c = self.compass.getCentroid(points)

        #if p_c.getCoordinates() != centroid.getCoordinates():
            #print("CLUSTER",p_c.getCoordinates())
            #print("CLUSTER_BB", p_ll.getCoordinates(), p_tr.getCoordinates())
            #print("CANVAS", centroid.getCoordinates())
            #print("CANVAS_BB", (MIN_X,MIN_Y), (MAX_X,MAX_Y))

        #Rotate
        if rotation_degrees != 0:
            points = self.compass.rotateAllPoints(centroid=centroid, points=points, angle=rotation_degrees, alignToIntegerGrid=True)

        #Expand
        if expansion != 0:
            assert 0 < expansion <= 1, "expansion must be a value between 0 and 1"
            
            max_expansion = int(canvas_size*expansion)
            eachDirection = int(max_expansion/2)
            max_LL = (centroid.getCoordinates()[0]-eachDirection, centroid.getCoordinates()[1]-eachDirection) 
            max_TR = (centroid.getCoordinates()[0]+eachDirection, centroid.getCoordinates()[1]+eachDirection) 
            

            (cx,cy) = centroid.getCoordinates()

            finished = False
            while finished == False:
                for point in points:
                    #print("EXPANSION", point.dumpTuple())
                    (x,y) = point.getCoordinates()
                    if x > cx:
                        x += 1
                    if x < cx:
                        x -= 1
                    if y > cy:
                        y += 1
                    if y < cy:
                        y -= 1

                    point.updateCoordinates(x,y)
                    
                    #print("X", max_LL[0], max_TR[0])
                    #print("X", max_LL[1], max_TR[1])
                    if (x <= max_LL[0] or x >= max_TR[0] or y <= max_LL[1] or y >= max_TR[1]):
                        finished = True
                
                if finished == True:
                    break
        
        #Shift Up/Down
        if shift_vertical != 0:
            assert -1 <= shift_vertical <= 1, "shift_vertical must be between -1 and +1"

            max_shift = int(canvas_size*shift_vertical)
            each_direction = int(max_shift/2)
            
            if shift_vertical <0:
                sign = -1
            else:
                sign = 1
            
            min_y = centroid.getCoordinates()[1]-each_direction
            max_y = centroid.getCoordinates()[1]+each_direction

            finished = False
            while finished == False:    
                for point in points:
                    #print("VERT", point.dumpTuple())
                    (x,y) = point.getCoordinates()
                    y = y+(1*sign)
                    point.updateCoordinates(x,y)
                    if y == min_y or y == max_y:
                        finished = True
                if finished == True:
                    break

        #Shift Left/Right
        if shift_horizontal != 0:
            assert -1 <= shift_horizontal <= 1, "shift_horizontal must be between -1 and +1"

            max_shift = int(canvas_size*shift_horizontal)

            each_direction = int(max_shift/2)
            
            if shift_horizontal <0:
                sign = -1
            else:
                sign = 1
            
            min_x = centroid.getCoordinates()[0]-each_direction
            max_x = centroid.getCoordinates()[0]+each_direction
            
            finished = False
            while finished == False:    
                for point in points:
                    #print("HORIZ",point.dumpTuple())
                    (x,y) = point.getCoordinates()
                    x = x+(1*sign)
                    point.updateCoordinates(x,y)
                    if x == min_x or x == max_x:
                        finished = True
                if finished == True:
                    break
        
        #Regerate Dictionaries
        names = []
        longitudes = []
        latitudes = []
        returnQuery = {}

        for point in points:
            tup = point.dumpTuple()
            names.append(tup[0])
            longitudes.append(tup[1][0])
            latitudes.append(tup[1][1])

        returnQuery['name'] = names
        returnQuery['longitude'] = longitudes
        returnQuery['latitude'] = latitudes

        print("returnQuery", returnQuery)
        return returnQuery

if __name__ == "__main__":

    argparser = argparse.ArgumentParser()									# initialize the argParser

    #General Params
    argparser.add_argument("--experimentName",
                            help="The name of the experiment we are running",
                            type = str,
                            required = False) 

    argparser.add_argument("--randomSeed",
                            help="number to use as random seed. Also controls the skew in the class distribution",
                            type = int,
                            required = False)

    #Location-Specific Params
    argparser.add_argument("--numLocations",
                            help="The number of Locations to create for this run",
                            type = int,
                            default=10,
                            required = False) 
    
    argparser.add_argument("--scaleFactor",
                            help="number to raise 2 to the power of to generate the graph for creating locations",
                            type = int,
                            required = False)
    
    argparser.add_argument("--edgeFactor",
                            help="number to multiple 2^scaleFactor by to get edges in graph",
                            type = int,
                            required = False)

    argparser.add_argument("--numClasses",
                            help="The number of object classes to create in any given location",
                            type=int,
                            required = False)

    #Query Specific Params
    argparser.add_argument("--numQueryTerms",
                            help="The number of Objects to add to the query term for this run",
                            type = int,
                            default=5,
                            required = False) 

    argparser.add_argument("--queryRatio",
                            help="The number (between 0 and 1) of Queries to generate as a proportion of locations",
                            type = float,
                            required = False) 

    argparser.add_argument("--numQueryDistortions",
                            help="Number between 0 and 4 that determines how many of the distortions will be (randomly) applied to the query terms",
                            type=int,
                            required = False)



                       

    flags = argparser.parse_args()

    SEED = flags.randomSeed
    random.seed(SEED)

    #Initialize the generator

    DG = DataGenerator()

    #Get the original Queries
    originalQueries = {} 
    for i in range(0, int(flags.queryRatio*flags.numLocations)):
        q_names = []
        q_latitudes = []
        q_longitudes = []

        for j in range(0, flags.numQueryTerms):
            q_names.append(j)
            q_longitudes.append(random.randint(0,flags.scaleFactor))
            q_latitudes.append(random.randint(0,flags.scaleFactor))
        
        originalQueries[i] =    {"name":q_names,
                        "longitude":q_longitudes,
                        "latitude":q_latitudes}

    print("QUERIES:")
    print(originalQueries)

    #Distort the queries
    distortedQueries = {}
    

    for i in range(len(originalQueries.keys())):
        params = random.choices(["rotation_degrees","expansion","shift_vertical","shift_horizontal"],k=flags.numQueryDistortions)
        param_vals = []

        if "rotation_degrees" in params:
            param_vals.append(random.randint(0,360))
        else:
            param_vals.append(0)
        if "expansion" in params:
            param_vals.append(random.random())
        else:
            param_vals.append(0)
        if "shift_vertical" in params:
            param_vals.append(random.uniform(-1,1))
        else:
            param_vals.append(0)
        if "shift_horizontal" in params:
            param_vals.append(random.uniform(-1,1))
        else:
            param_vals.append(0)

        print("Distorting query", i, "With params", param_vals)
        distortedQueries[i] = DG.distortQuery(query_dict=originalQueries[i],
                                                    canvas_size=2^flags.scaleFactor, 
                                                    rotation_degrees=param_vals[0], 
                                                    expansion=param_vals[1], 
                                                    shift_vertical=param_vals[2], 
                                                    shift_horizontal=param_vals[3])
    print(distortedQueries)

    pointLists = []
    locations = {}

    print("Creating Locations...")
    for i in range(0, flags.numLocations):
        pointsList = DG.generateMatrix(scaleFactor=flags.scaleFactor, edgeFactor=flags.edgeFactor)
        try:
            locations[i] = DG.labelNodes(points=pointsList,numClasses=flags.numClasses, random_seed=flags.randomSeed, queryTerms=distortedQueries[i])
            #print("Creating Location", i, "with embedded query", i)
        except KeyError as e:
            locations[i] = DG.labelNodes(points=pointsList,numClasses=flags.numClasses, random_seed=flags.randomSeed, queryTerms=None)
            #print("Creating Location", i, "with no embedded query")

    #print(locations)

    for i in range(len(locations.keys())):
        print("Saved to", DG.saveToFile(experiment_name=flags.experimentName, saveType='location', number=i, data=locations[i]))
    
    for i in range(len(distortedQueries.keys())):
        #print("SAVING:", distortedQueries[i])
        print("Saved to", DG.saveToFile(experiment_name=flags.experimentName, saveType='query', number=i, data=distortedQueries[i]))
