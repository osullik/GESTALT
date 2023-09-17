#Author: Kent O'Sullivan
#Email: osullik@umd.edu

# System Imports
import sys
import os
import unittest
import random
import string 
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
        pass

    def generateMatrix(self,scaleFactor:int,edgeFactor:int):
        points = []

        rmat = nk.generators.RmatGenerator(scaleFactor, edgeFactor, 0.57, 0.19, 0.19, 0.05) #Parameters taken from Graph500
        rmatG = rmat.generate()

        #print(nk.algebraic.adjacencyMatrix(rmatG,matrixType='sparse'))
        #print(nk.algebraic.adjacencyMatrix(rmatG,matrixType='dense'))

        #Generate a sparse matrix of the RMAT generated material. 
        sm = nk.algebraic.adjacencyMatrix(rmatG,matrixType='sparse')

        #Extract row and column info from the sparse matrix
        row,col = sm.nonzero()  
            
        for r,c in zip(row,col):
            points.append((r,c))

        return(points)

    def labelNodes(self,points:list[tuple], numClasses:int, random_seed:int)->dict:

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
        count, bins, ignored = plt.hist(s, bins=numClasses)
        binList = np.digitize(s,bins)

        names = []
        longitudes = []
        latitudes = []

        #For each coordinate, assign it a label based on the power law distribution we generated. 
        for i in range(0, len(points)):
            coord = points[i]
            labelIndex = binList[i % len(points)]  #Start at beginning if longer than list
            label = classes[labelIndex-1]
            names.append(label)
            longitudes.append(coord[0])
            latitudes.append(coord[1])

        #Build the dictionary.
        namedPoints["name"] = names
        namedPoints["longitude"] = longitudes
        namedPoints["latitude"] = latitudes

        return(namedPoints)

    def saveToFile(self, experiment_name:str, saveType:str, number:int, data:dict):

        dataDirectory = ""
        for p in sys.path:
            if p.endswith("data"):
                dataDirectory = p
        
        assert((dataDirectory in sys.path),"Unable to find the 'GESTALT/data' directory - does it exist?")

        experimentsDirectoryPath = os.path.join(dataDirectory, "experiments")
        assert (os.path.exists(experimentsDirectoryPath),"'data/experiments' does not exist.")

        experimentDirectoryPath = os.path.join(experimentsDirectoryPath, experiment_name)
        
        if os.path.exists(experimentDirectoryPath) == False:
            os.mkdir(experimentDirectoryPath)
        
        assert (os.path.exists(experimentDirectoryPath),"'data/experiments/'"+experiment_name+" does not exist.")

        typeDirectoryPath = os.path.join(experimentDirectoryPath, saveType)
        
        if os.path.exists(typeDirectoryPath) == False:
            os.mkdir(typeDirectoryPath)
        
        assert (os.path.exists(typeDirectoryPath),"'data/experiments/'"+experiment_name+saveType+" does not exist.")

        filePathToSave = typeDirectoryPath+"/"+saveType+str(number)+".csv"

        df_to_save = pd.DataFrame(data=data)

        df_to_save.to_csv(filePathToSave,sep=",",header=True,index=False)

        print("FILEPATHTOSAVE", filePathToSave)

        return(filePathToSave)