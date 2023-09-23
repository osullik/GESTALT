#Author: Kent O'Sullivan
#Email: osullik@umd.edu

# System Imports
import sys
import os
# Library Imports
import pandas as pd
# User file imports

sys.path.insert(1, os.getcwd()+"/../")
sys.path.insert(1, os.getcwd()+"/../compass")
sys.path.insert(1, os.getcwd()+"/../gestalt")
sys.path.insert(1, os.getcwd()+"/../experiments")

from conceptMapping import ConceptMapper

class QuadrantMapConverter():
    def __init__(self):
        self.CM = ConceptMapper()

    def generateQuadrantMap(self,input_df:pd.DataFrame)->dict:
        locationDict = {}
        
        min_x = input_df.min(axis=0)['longitude']
        max_x = input_df.max(axis=0)['longitude']
        min_y = input_df.min(axis=0)['latitude']
        max_y = input_df.max(axis=0)['latitude'] 
        midpoint = ((max_x/2),(max_y/2))

        for idx, row in input_df.iterrows():
            locationDict[idx] = {}
            locationDict[idx]['name'] = row["name"]
            locationDict[idx]['longitude'] = row["longitude"]
            locationDict[idx]['latitude'] = row["latitude"]
            

        quadrantDict = self.CM.getRelativeLocation(locationDict=locationDict,midpoint=midpoint)

        return(quadrantDict)