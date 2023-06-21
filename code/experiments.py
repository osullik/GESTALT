#GESTALT/code/experiments.py


#Calculate Precision / Recall of clustering

# Get Ground Truth Labels

# Get Clusters

#System Imports
import argparse, json, sys, os

#Library Imports: 
from fastkml import kml 
import pandas as pd


class Experiments():
    def __init__(self):
        pass

    def loadClustersFromFile(self, clusterFileName:str):
        if clusterFileName is not None: 
            sourceData_df = pd.read_csv(clusterFileName)[['name','longitude','latitude','predicted_location','ground_truth_location']]
        else:
            exit("Unable to find dataframe. Please check your CSV / Dataframe and Try again")

        return(sourceData_df)

    def calculatePrecisionAndRecall(self, clusterDataframe):
        resultsDict = {}

        for idx, row in clusterDataframe.iterrows():

            if row["predicted_location"] == row["ground_truth_location"]:
                try:
                    resultsDict[row["ground_truth_location"]]["correct"] +=1
                except KeyError:
                    try:
                        resultsDict[row["ground_truth_location"]]["correct"] =1
                    except KeyError:
                        resultsDict[row["ground_truth_location"]] = {}
            else:
                try:
                    resultsDict[row["ground_truth_location"]]["wrong"] +=1
                except KeyError:
                    try:
                        resultsDict[row["ground_truth_location"]]["wrong"] =1
                    except KeyError:
                        resultsDict[row["ground_truth_location"]] = {}

        for entry in resultsDict.items():
            print(entry)


if __name__=="__main__":

    argparser = argparse.ArgumentParser()									# initialize the argParser
    
    argparser.add_argument(	"-c", "--clusterFile", 							
							help="CSV of clusters with predicted locations",
                            type=str,
							default=None,
							required=True)	


    flags = argparser.parse_args()																		# populate variables from command line arguments

    madScientist = Experiments()
    clusterDF = madScientist.loadClustersFromFile(flags.clusterFile)

    results = madScientist.calculatePrecisionAndRecall(clusterDF)

