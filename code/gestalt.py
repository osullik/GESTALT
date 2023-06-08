
#System Imports
import argparse, json, sys

#Library Imports
	#from fastkml import kml 
	#from OSMPythonTools.api import Api
	#from OSMPythonTools.overpass import Overpass, overpassQueryBuilder
	#from OSMPythonTools.nominatim import Nominatim

	#from matplotlib import pyplot as plt
	#import pandas as pd

	#import sklearn
	#from sklearn.cluster import KMeans
	#from sklearn.cluster import DBSCAN

	#from libpysal.weights import Queen, KNN

	#from scipy.spatial import KDTree

	#import numpy as np

	#import Levenshtein

#User Imports

from dataCollection import TerrainExtractor, osmQueryEngine
from ownershipAssignment import OwnershipAssigner



if __name__ == "__main__":

	argparser = argparse.ArgumentParser()									# initialize the argParser

	argparser.add_argument(	"-q", "--queryOsmMode", 							
							help="engage mode to issue a query to OpenStreetMaps",
							action="store_true",
							default=False,
							required=False)	
	
	argparser.add_argument( "-b", "--boundingbox", 
							help="specifies the bounding box to be passed to OSM", 
							nargs='+',
							default=None,
							required=False)
	
	argparser.add_argument( "-s", "--searchterms",
							help="search terms to pass to the overpass turbo API",
							type=list,
							default=None,
							required=False)
	
	argparser.add_argument( '-o', "--output",
							help="directory to output results to", 
							type=str,
							default="data/", 
							required=False)
	
	argparser.add_argument(	"-k", "--kmlIngestMode", 							
							help="Mode to ingest KML files",
							action="store_true",
							default=False,
							required=False)	
	
	argparser.add_argument( "-f", "--fileSource",
							help="KML file(s) to ingest)", 
							nargs="+", 
							default=None,
							required=False)

	argparser.add_argument(	"-j", "--jsonDump", 							
							help="dump the datasets to JSON",
							action="store_true",
							default=False,
							required=False)

	argparser.add_argument(	"-m", "--membershipInference", 							
							help="Define the location membership inference method: 'kmeans', 'dbsweep', 'partitioning'",
							type=str,
							default=None,
							required=False)	
	
	flags = argparser.parse_args()											# populate variables from command line arguments


	if flags.queryOsmMode== True:
		bbox = flags.boundingbox
		outputfile = flags.output
		searchterms = flags.searchterms
		oqe = osmQueryEngine()
		osmDict = oqe.queryOSM(bbox, "winery")	#TODO  need to adjust this to handle list inputs from the searchTerms parameter. 
		
		with open(outputfile,'w') as outfile:
			json.dump(osmDict, outfile, indent=4)
			print("Successfully outputted data to \"{outputLoc}\"".format(outputLoc=outputfile))
		exit()

	if flags.kmlIngestMode == True:
		sourceFiles = flags.fileSource
		outputfile = flags.output
		tex = TerrainExtractor()
		for file in sourceFiles:
			print(file)
			fullfilename = file.split("/")[-1]
			shortFileName = fullfilename.split(".")[0]
			objectLocations = tex.Ingest_kml_file(file)
			with open(outputfile+"_"+shortFileName+".json",'w') as outfile:
				json.dump(objectLocations, outfile, indent=4)
			print("Successfully outputted data to \"{outputLoc}\"".format(outputLoc=outputfile+"_"+shortFileName+".json"))
		exit()


	#kmlList = tex.Get_kml_file_list()

	gestalt = OwnershipAssigner(osmDict, objectLocations)
	flatOSM = gestalt.flatten_osm()
	flatOBJ = gestalt.flatten_obj('Swan_Valley')
	gestalt.convertToDataFrame(flatOSM, flatOBJ)
	gestalt.normalizeCoords(bbox)
	
	
	if flags.membershipInference == None or flags.membershipInference not in ['kmeans', 'dbscan', 'region', 'all']: 
		sys.exit("Please specify the membership inference method out of: 'kmeans', 'dbscan', 'region', or 'all' ")
	elif flags.membershipInference == 'kmeans':
		#numClusters = len(gestalt._locationCoordinates)
		numClusters = 6
		print("Number of Clusters:",numClusters )
		gestalt.kMeans_membership(numClusters)
		correct = gestalt._df_obj["kmeans_correct"]
		print(correct.value_counts())
		clusters = gestalt._df_obj["cluster"]
		print(clusters.value_counts())

	elif flags.membershipInference == 'dbscan':
		epsilon=0.1/6371 
		minCluster=3
		gestalt.dbscan_membership(epsilon,minCluster)
		correct = gestalt._df_obj["dbscan_correct"]
		print(correct.value_counts())
		clusters = gestalt._df_obj["cluster"]
		print(clusters.value_counts())

	elif flags.membershipInference == 'region':
		sys.exit("Not Implemented")
	elif flags.membershipInference == 'all':
		print("WARNING: DBSCAN CLUSTERS WILL BE USED FOR VISUALIZATION IN ALL MODE")
		numClusters = 6
		print("Number of Clusters:",numClusters )
		gestalt.kMeans_membership(numClusters)
		correct = gestalt._df_obj["kmeans_correct"]
		print(correct.value_counts())
		clusters = gestalt._df_obj["cluster"]
		print(clusters.value_counts())

		epsilon=0.1/6371 
		minCluster=3
		gestalt.dbscan_membership(epsilon,minCluster)
		correct = gestalt._df_obj["dbscan_correct"]
		print(correct.value_counts())
		clusters = gestalt._df_obj["cluster"]
		print(clusters.value_counts())

	if flags.jsonDump == True:
		#Dump Dicts 
		

		with open("data/objects.json", 'w') as outfile:
			json.dump(objectLocations, outfile, indent=4)

		#Dump Dataframes

		objectJSON = gestalt._df_obj.to_json(orient="records")
		#parsed_obj = loads(objectJSON)

		gestalt._df_osm.to_csv("data/osm_df.csv", index=False)
		gestalt._df_obj.to_csv("data/obj_df.csv", index=False)

		sys.exit("Exported osm data and json objects to file")



