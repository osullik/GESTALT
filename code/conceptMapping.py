# Code for Concept Mapping in Python

#System Imports

#Library Imports
import pandas as pd
from scipy.spatial import KDTree
import sklearn
from sklearn.cluster import KMeans
import Levenshtein
import numpy as np
from sklearn.cluster import DBSCAN

#User imports

class ConceptMapper():
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

		attributeNumbers = []
		attributes = set() 														# Set used to generate list of unique descriptors

		for region in self._objDict.keys():										# Loop to get all the attribute descriptors. 
			for loc in self._objDict[region].keys():
				for obj in self._objDict[region][loc].keys():
					if self._objDict[region][loc][obj]["description"] != None:
						attributeNumbers.append(len(self._objDict[region][loc][obj]["description"]))
						for key in self._objDict[region][loc][obj]["description"].keys():
							attributes.add(list(self._objDict[region][loc][obj]["description"][key].keys())[0])
								
					else:
						attributeNumbers.append(0)


		flatOBJ["object"] = [] 											# Construct the dictionary 
		flatOBJ["latitude"] = []
		flatOBJ["longitude"] = []
		flatOBJ["true_location"] = []
		for attribute in attributes: 									# Add in keys and empty lists for each descriptor
			flatOBJ[attribute] = []



		for loc in self._objDict[region].keys():								# Loop through each object
			for obj in self._objDict[region][loc].keys():
				#print(self._objDict[region][loc][obj])
				flatOBJ["object"].append(self._objDict[region][loc][obj]['name'])
				flatOBJ["latitude"].append(self._objDict[region][loc][obj]['latitude'])
				flatOBJ["longitude"].append(self._objDict[region][loc][obj]['longitude'])
				flatOBJ["true_location"].append(loc)

				usedDescriptors = [] 											#Loop through each descriptor for an object, append to respective list or append None
				if self._objDict[region][loc][obj]['description'] is not None:
					for descriptor in self._objDict[region][loc][obj]['description'].keys():
						for key in self._objDict[region][loc][obj]['description'][descriptor].keys():
							#try:
							flatOBJ[key].append((self._objDict[region][loc][obj]['description'][descriptor][key]))
							#except KeyError:
							#	flatOBJ[key] = []
							#	flatOBJ[key].append((self._objDict[region][loc][obj]['description'][descriptor][key]))
							usedDescriptors.append(key)

				for attribute in attributes:
					if attribute not in usedDescriptors:
						#try:
						flatOBJ[attribute].append(None)
						usedDescriptors.append(attribute)
						#except KeyError:
						#	flatOBJ[attribute] = []
						#	flatOBJ[attribute].append(None)


		for obj in flatOBJ.keys():
			if len(flatOBJ[obj]) > len(flatOBJ["object"]): #Hacky workaround to get dataframes to be same length. TODO: Fix bug. 
				del flatOBJ[obj][-1]

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

		self._objects_kdTree = KDTree(self._objectCoordinates)

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
		
		self.inferLocation(centroids,"kmeans")
		print(self._df_obj)

	def dbscan_membership(self, epsilon=0.5/6371., minCluster=3):
		#1/6371 is ~100m
		print("Clustering with DBScan")
		loc_arr = np.array(self._objectCoordinates)

		db_cluster =  DBSCAN(eps=epsilon, min_samples=minCluster).fit(np.radians(loc_arr))
		self._df_obj['cluster'] = db_cluster.labels_
		print(self._df_obj)

		
		centroids = self.calculateCentroids(db_cluster.labels_)
		self.inferLocation(centroids,"dbscan")
		print(self._df_obj)

	#def regionalization(self, numberOfClusters=6):
	#	print("Regionalizing")
	#	w = Queen.from_dataframe(np.array(self._locationCoordinates))

	#	model = AgglomerativeClustering(
	#	linkage="ward", connectivity=w.sparse, n_clusters=6)
	#	model.fit(np.radians(loc_arr))

	#	print(model)

	def calculateCentroids(self, clusters):
		print("Calculating Centroids")
		centroids = []

		for cluster in range (0, (max(clusters)+1)): 								#+1 to account for indexing from 0
			cluster_df = self._df_obj.loc[self._df_obj['cluster'] == cluster]		# Get only the coords belonging to this cluster
			coords = []

			for index, obj in cluster_df.iterrows(): 								# Make the coords into a list, then numpy array
				coords.append([obj.latitude, obj.longitude])
			np_coords = np.array(coords)
			
			centroid = np.mean(np_coords,axis=0) 									# Get the midpoint of the array
			centroids.append(centroid) 												# Build list of centroids

		return(centroids)


	def inferLocation(self,centroids,method):
		print("Inferring object location")
		mappings = {} 																#Dict so that arbitrary number of clusters can be used
		for centroid in range (0, (len(centroids))): 								# For each centroid
		    d, i = self._location_kdTree.query(centroids[centroid],1) 				# Look up its nearest neighbour in the KD tree
		    mappings[centroid] = self._locationIndex[i]

		self._df_obj['predicted_location_'+method] = self._df_obj.cluster.map(mappings) 		# Infer that the nearest neighbour is the cluster location

		matches = []

		#Move this to own function later. Use Levenshtein at 0.7 to handle labelling differences. 
		for index,row in self._df_obj.iterrows():								
			if Levenshtein.ratio(row['predicted_location_'+method], row["true_location"]) >= 0.7:
				matches.append("True")
			else:
				matches.append("False")

		self._df_obj[method+"_correct"] = matches

		print(self._df_obj)