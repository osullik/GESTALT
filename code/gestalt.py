

##TODO:

# 1. Extract data from KML

# 2. Connect to OSM

# 3. Get Specific Locations from OSM

#System Imports
import os, sys, argparse, json


#Library Imports
from fastkml import kml 
from OSMPythonTools.api import Api
from OSMPythonTools.overpass import Overpass, overpassQueryBuilder
from OSMPythonTools.nominatim import Nominatim

from matplotlib import pyplot as plt
import pandas as pd

import sklearn
from sklearn.cluster import KMeans
from sklearn.cluster import DBSCAN

from scipy.spatial import KDTree

import numpy as np

#User Imports

class TerrainExtractor():

	def __init__(self, kml_directory):

		self._kml_directory = kml_directory

	def Get_kml_file_list(self):
		'''
		gets the list of kml files to be processed in a given directory
		INPUT ARGS: 
			- None, uses class _kml_directory var
		ACTIONS:
			- Get the contents of the directory given
			- filter out the KML files
			- Throw an error if no KML files found
		OUTPUT:
			- kmlFiles - List of Strings - The KML files to be imported. 
		'''

		listOfDataFiles = os.listdir(self._kml_directory)

		kmlFiles = []

		for file in listOfDataFiles:
			if file.endswith(".kml"):
				kmlFiles.append(file)
			else:
				pass

		if len(kmlFiles) == 0:
			sys.exit("No KML Files found, check directory and try again")

		print("loaded files from", self._kml_directory)
		return kmlFiles

	def Ingest_kml_file(self, kmlFileName):
		'''
		Ingests a KML file and transforms it into a dictionary 
		INPUT ARGS:
			- kmlFileName - String - the filename of the KML to import. 
			- (implicit) self._kml_directory - string - Class Property with the directory of the KML file. 
		ACTIONS: 
			- Open the KML File
			- Import KML string
			- Transform to KML Object
			- Unpack to the appropriate level (TODO: generalize to handle arbitrary depth)
			- Build dictionary out of contents, with levels (region -> Location -> Item ->(A) Description, (B) Latitude (C) Longitude)
		OUTPUT 
			- Returns LocalityDict - A dictionary of the locaiton data for each area being examined. 
		'''

		if self._kml_directory[-1] != "/":									#Prevent error from missing trailing slash
			self._kml_directory += "/"

		filePath = self._kml_directory + kmlFileName

		print("Opening", filePath)

		with open(filePath, 'rt', encoding='utf-8') as f:					#Open the file (double UTF-8 required because of fastKML error)
			 doc = f.read().encode('utf-8')

		localityDict = {}													#Initialize dict to return 

		k = kml.KML()														# Create KML Object

		k.from_string(doc)													# Convert raw KML into Object

		document = list(k.features())										# Extract the document from the object


		for region in (list(document[0].features())):						# Extract the regions (i.e. swan valley)
			regName = region.name
			localityDict[regName] = {}
			
			for location in (list(region.features())):						# Extract the locations (i.e. Wineries)
				locName = location.name
				localityDict[regName][locName] = {}
				
				featureIndex = 0
				for terrainFeature in (list(location.features())):			# Extract the Features (i.e. the objects)
					name = terrainFeature.name 
					description = terrainFeature.description
					latitude = terrainFeature.geometry.x
					longitude = terrainFeature.geometry.y
																			# Build the dictionary 

					localityDict[regName][locName][str(featureIndex)] = {}
					localityDict[regName][locName][str(featureIndex)]["name"] = name 
					localityDict[regName][locName][str(featureIndex)]["latitude"] = latitude
					localityDict[regName][locName][str(featureIndex)]["longitude"] = longitude
					localityDict[regName][locName][str(featureIndex)]["description"] = self.extractTerrainDescriptors(description)

					featureIndex += 1
					
		#for location in localityDict["Swan_Valley"]:
		#	for item in (localityDict["Swan_Valley"][location]):
		#		print (location, item, localityDict["Swan_Valley"][location][item])

		print("Generated dictionary from", kmlFileName)
		return localityDict

	def extractTerrainDescriptors(self, descriptorString):
		'''
		Helper function to turn a string of key, value pairs into a dictionary of descriptive items. 
		INPUT ARGS:
			- descriptorString - String - the string of key value pairs. 
		ACTIONS: 
			- Early stopping on 'none' description
			- Split into a list of discrete pairs
			- Split pairs on the colon operator
			- Build the dictionary of each descriptive fact
		RETURN
			- descriptors - dict - the dictionary of descriptive terms in the input string of form {index:{key:value}, ... }
		'''
		
		if descriptorString == None:										# Early stopping for null descriptions
			return None

		descriptorList = (descriptorString.split())							# Turn into list

		descriptors = {}													# Intialize the dict to return

		descriptorNumber = 0												# Initialize the index

		for descriptor in descriptorList:									# Generate the dict
			key,value = descriptor.split(":")
			descriptors[str(descriptorNumber)] = {}
			descriptors[str(descriptorNumber)][key] = value
			descriptorNumber+=1


		return descriptors

class osmQueryEngine():


	def __init__(self):
		pass

	def queryOSM(self,bbox, typeQuery):
		'''
		(Description generated by chatGPT)
		input args:
    		- bbox: The bounding box to search within, as a list of four decimal values representing the minimum and maximum longitude and latitude values.
   			- typeQuery: The value to search for within the craft tag of the nodes.

		actions:
		    - Initialize an empty dictionary called locationDict.
		    - Use the Overpass API to query OpenStreetMap for all nodes with the craft tag equal to the typeQuery value and within the bounding box specified by bbox.
		    - Loop through the results of the query and extract the location name, latitude, and longitude of each element.
		    - Store the extracted location data in the locationDict dictionary with the location name as the key and the latitude and longitude as the values.
		    - Return the locationDict dictionary.

		outputs:
    		- locationDict: A dictionary containing the location names as keys and the corresponding latitude and longitude values as values.
		'''

		locationDict = {}														# Initialize dict to return 

		overpass = Overpass()													#Initialize OSMTools classes. 
		nominatim = Nominatim()
																				#Query the API
		query = overpassQueryBuilder(	bbox=bbox, 
										elementType="node",
										selector="'craft'="+typeQuery)

		results = overpass.query(query)

		for element in results.elements():										# Build the dictionary 
			locationName = element.tags()['name']
			latitude = element.geometry()['coordinates'][0]
			longitude = element.geometry()['coordinates'][1]
			locationDict[locationName] = {}
			locationDict[locationName]['latitude'] = latitude
			locationDict[locationName]['longitude'] = longitude

		print("Got OSM records for all", typeQuery, "within", bbox)
		return locationDict

class Gestalt():
	def __init__(self,osmData, objData):
		self._osmDict = osmData
		self._objDict = objData 

	def flatten_osm(self):
		'''
		Function to take the fully expressive Locations from openStreetMaps and squash into a flatter dict to be made into data frames
		Input Args: 
			(implicit) self._osmDict - dict of dicts - contains all the locations within the bounding box from OSM. 
		Operations: 
			- Iterate through the dictionary, generate lists
		Output
			- flatOSM - dict of lists
		'''

		flatOSM = {}															#Initialize vars
		locations = []
		latitudes = []
		longitudes = []

		for loc in self._osmDict.keys():										#Loop through dict & append vals to list
			locations.append(loc)
			latitudes.append(self._osmDict[loc]['latitude'])
			longitudes.append(self._osmDict[loc]['longitude'])

		flatOSM["location"] = locations 										#Create the flattened dict of lists. 
		flatOSM["latitude"] = latitudes
		flatOSM["longitude"] = longitudes

		return flatOSM

	def flatten_obj(self, region):
		'''
		Function to take the fully expressive objects from the KML and squash into a flatter dict to be made into data frames
		Input Args: 
			region - string - the name of the region within the dict of objects to be flattened. 
			(implicit) self._objDict - dict of dicts - contains all the objects within the bounding box from OSM. 
		Operations: 
			- Iterate through the dictionary, generate lists
		Output
			- flatOBJ - dict of lists
		'''

		flatOBJ = {} 															# Initialize vars
		locations = []
		objects = []
		latitudes = []
		longitudes = []

		for loc in self._objDict[region].keys():								# Loop through each object
			for obj in self._objDict[region][loc].keys():
				#print(self._objDict[region][loc][obj])
				objects.append(self._objDict[region][loc][obj]['name'])
				latitudes.append(self._objDict[region][loc][obj]['latitude'])
				longitudes.append(self._objDict[region][loc][obj]['longitude'])
				locations.append(loc)

		flatOBJ["object"] = objects 											# Construct the dictionary 
		flatOBJ["latitude"] = latitudes
		flatOBJ["longitude"] = longitudes
		flatOBJ["true_location"] = locations

		return flatOBJ

	def convertToDataFrame(self, flatOSM, flatOBJ):								# Convert two flattened dictionaries into data frames

		self._df_osm = pd.DataFrame(data=flatOSM)
		self._df_obj = pd.DataFrame(data=flatOBJ)
		self._locationCoordinates = []
		self._locationIndex = {}

		for index, row in self._df_osm.iterrows():
		    elem = [row[1],row[2]]
		    self._locationCoordinates.append(elem)
		    self._locationIndex[index] = row[0]

		self._location_kdTree = KDTree(self._locationCoordinates)

		self._objectCoordinates = []

		for index, row in self._df_obj.iterrows():
		    elem = [row[1],row[2]]
		    self._objectCoordinates.append(elem)
		    #self._objectIndex[index] = row[0]


		print("Converted objects and OSM details to DataFrames")


	def normalizeCoords(self, boundingBox):
		'''
		Function to flatten coordiantes into a 0-100 grid for vizualization. 
		Input Args: 
			- boundingBox - list of floats - defines the max and min x and y coords to serve as 0 and 100. 
			- (implicit) self._df_osm - pandas dataframe containing the names, lat and longs of locations. 
			- (implicit) self._df_obj - pandas dataframe containing the names, lat, longs and parent locations of objects. 
		Actions: 
			- Use minimax normalization to make the bounding box go from 0:100
			- Append minimax normalized coordinates to end of dataframe
		Returns: 
			- Prints to csv the modified self._df_osm and self._df_obj dataframes. 
 		'''

 		#Print the dataframes to file. 

		self._df_osm.to_csv("data/osm_df.csv", index=False)
		self._df_obj.to_csv("data/obj_df.csv", index=False)

	def kMeans_membership(self, numberOfClusters):
		print("Clustering with kMeans")
		kmeans = KMeans(n_clusters=numberOfClusters, random_state=0, n_init="auto")
		self._df_obj['cluster'] = kmeans.fit_predict(self._df_obj[['latitude','longitude']])
		centroids = kmeans.cluster_centers_
		
		self.inferLocation(centroids)
		print(self._df_obj)

	def dbscan_membership(self, epsilon=0.5/6371., minCluster=3):
		#1/6371 is ~100m
		print("Clustering with DBScan")
		loc_arr = np.array(self._objectCoordinates)

		db_cluster =  DBSCAN(eps=epsilon, min_samples=minCluster).fit(np.radians(loc_arr))
		self._df_obj['cluster'] = db_cluster.labels_
		print(self._df_obj)

		
		centroids = self.calculateCentroids(db_cluster.labels_)
		self.inferLocation(centroids)
		print(self._df_obj)

	def calculateCentroids(self, clusters):
		print("Calculating Centroids")
		centroids = []



		for cluster in range (0, (max(clusters)+1)): #+1 to account for indexing from 0
			print("Checking cluster", cluster)
			cluster_df = self._df_obj.loc[self._df_obj['cluster'] == cluster]
			coords = []
			for index, obj in cluster_df.iterrows():
				coords.append([obj.latitude, obj.longitude])
			np_coords = np.array(coords)
			centroid = np.mean(np_coords,axis=0)
			centroids.append(centroid)

		return(centroids)


	def inferLocation(self,centroids):
		mappings = {}
		for centroid in range (0, (len(centroids))):
		    d, i = self._location_kdTree.query(centroids[centroid],1)
		    mappings[centroid] = self._locationIndex[i]

		self._df_obj['PredictedLocation'] = self._df_obj.cluster.map(mappings)





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

	gestalt = Gestalt(osmDict, objectLocations)
	flatOSM = gestalt.flatten_osm()
	flatOBJ = gestalt.flatten_obj('Swan_Valley')
	gestalt.convertToDataFrame(flatOSM, flatOBJ)
	gestalt.normalizeCoords(bbox)
	
	if flags.jsonDump == True:
		with open("data/osm.json",'w') as outfile:
			json.dump(osmDict, outfile, indent=4)

		with open("data/objects.json", 'w') as outfile:
			json.dump(objectLocations, outfile, indent=4)

		sys.exit("Exported osm data and json objects to file")
	
	if flags.membershipInference == None or flags.membershipInference not in ['kmeans', 'dbscan', 'partitioning']: 
		sys.exit("Please specify the membership inference method out of: 'kmeans', 'dbscan', or 'partitioning'")
	elif flags.membershipInference == 'kmeans':
		gestalt.kMeans_membership(6)
	elif flags.membershipInference == 'dbscan':
		gestalt.dbscan_membership()



