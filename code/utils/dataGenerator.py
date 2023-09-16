#Author: Kent O'Sullivan
#Email: osullik@umd.edu

# System Imports
import sys
import os
import unittest
# Library Imports
import pandas as pd
import numpy as np
import networkit as nk

# User file imports

sys.path.insert(1, os.getcwd()+"/../")
sys.path.insert(1, os.getcwd()+"/../compass")
sys.path.insert(1, os.getcwd()+"/../gestalt")
sys.path.insert(1, os.getcwd()+"/../experiments")

from compass import Point
from compass import Compass
from conceptMapping import ConceptMapper
from search import InvertedIndex
from exp_compass import CompassExperimentRunner, CompassDataLoader

class DataGenerator():
    def __init__(self):
        pass

    def generateMatrix(self,locationSize:int,numObjects:int,labels:list[str]):

        rmat = nk.generators.RmatGenerator(locationSize, 1, 0.1, 0.2, 0.5, 0.2)

        rmatG = rmat.generate()

        print(rmatG)

        print(nk.algebraic.adjacencyMatrix(rmatG,matrixType='sparse'))
        print(nk.algebraic.adjacencyMatrix(rmatG,matrixType='dense'))

        sm = nk.algebraic.adjacencyMatrix(rmatG,matrixType='sparse')
            
        row,col = sm.nonzero()

        points = []
            
        for r,c in zip(row,col):
            points.append((r,c))


        return(points)