
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
from conceptMapping import ConceptMapper



if __name__ == "__main__":

	argparser = argparse.ArgumentParser()									# initialize the argParser

	argparser.add_argument(	"-d", "--directory", 							
							help="specifies the directory where KML files are stored",
							type=str,
							default="data/",
							required=False)	

	argparser.add_argument(	"-o", "--osm", 							
							help="issue a query to OpenStreetMaps",
							action="store_true",
							default=False,
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


	tex = TerrainExtractor(flags.directory)

	kmlList = tex.Get_kml_file_list()

	objectLocations = tex.Ingest_kml_file(kmlList[0])

	bbox = [-31.90009882641578, 115.96168231510637, -31.77307863942101, 116.05029961853784] # Swan Valley isn't defined as an entity in OSM. BBOX from: https://travellingcorkscrew.com.au/wp-content/uploads/2013/08/Swan-Valley-Wineries-Map.pdf 

	oqe = osmQueryEngine()
	osmDict = oqe.queryOSM(bbox, "winery")

	gestalt = ConceptMapper(osmDict, objectLocations)
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
		with open("data/osm.json",'w') as outfile:
			json.dump(osmDict, outfile, indent=4)

		with open("data/objects.json", 'w') as outfile:
			json.dump(objectLocations, outfile, indent=4)

		#Dump Dataframes

		objectJSON = gestalt._df_obj.to_json(orient="records")
		#parsed_obj = loads(objectJSON)

		gestalt._df_osm.to_csv("data/osm_df.csv", index=False)
		gestalt._df_obj.to_csv("data/obj_df.csv", index=False)

		sys.exit("Exported osm data and json objects to file")



