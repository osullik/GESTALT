#Code for ownership assignment in GESTALT

#System Imports
import json
import warnings

#Library Imports
import pandas as pd
from scipy.spatial import KDTree
import sklearn
from sklearn.cluster import KMeans
import Levenshtein
import numpy as np
from sklearn.cluster import DBSCAN

import matplotlib.pyplot as plt

#User imports

class OwnershipAssigner():
	def __init__(self,locationData, objData):
		self._locationDict = locationData
		self._objectDict = objData 
		warnings.simplefilter("ignore") 									# Suppress warnings in pandas output


	def flatten_locations(self, locationsFile):
		'''
		Function to take the fully expressive Locations from openStreetMaps and squash into a flatter dict to be made into data frames
		Input Args: 
			locationsFile - dict of dicts - contains all the locations within the bounding box from OSM. 
		Operations: 
			- Iterate through the dictionary, generate lists
		Output
			- flatLocations - dict of lists
		'''

		flatLocations = {}															#Initialize vars
		locations = []
		latitudes = []
		longitudes = []

		for loc in locationsFile.keys():										#Loop through dict & append vals to list
			locations.append(loc)
			latitudes.append(locationsFile[loc]['latitude'])
			longitudes.append(locationsFile[loc]['longitude'])

		flatLocations["location"] = locations 										#Create the flattened dict of lists. 
		flatLocations["latitude"] = latitudes
		flatLocations["longitude"] = longitudes

		return flatLocations

	def flatten_objects_from_osm_dump(self, objectsDict):
		print("Starting to flatten_objects_from_osm_dump")

		flatObjects = {}
		flatObjects["object"] = []
		flatObjects["latitude"] = []
		flatObjects["longitude"] = []

		for object in objectsDict.keys():
			flatObjects["object"].append(objectsDict[object]['name'])
			flatObjects["latitude"].append(objectsDict[object]['latitude'])
			flatObjects["longitude"].append(objectsDict[object]['longitude'])

		return flatObjects
			



	def flatten_objects_from_kml(self, region):
		'''
		Function to take the fully expressive objects from the KML and squash into a flatter dict to be made into data frames
		Input Args: 
			region - string - the name of the region within the dict of objects to be flattened. 
			(implicit) self._objectDict - dict of dicts - contains all the objects within the bounding box from OSM. 
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

	def convertToDataFrame(self, flatLocations, flatObjects):								# Convert two flattened dictionaries into data frames

		#print("\n\n FLAT LOCATIONS:", flatLocations.items(),"\n\n")
		#print("\n\n FLAT OBJECTS:", flatObjects.items(),"\n\n")


		self._df_locations = pd.DataFrame.from_dict(flatLocations, orient="index")
		
		self._df_objects = pd.DataFrame.from_dict(flatObjects, orient="index")
		self._locationCoordinates = []
		self._locationIndex = {}

		i = 0

		#print("\n\n=====",self._df_locations,"=====\n\n",)
		for index, row in self._df_locations.iterrows():
			elem = [row[2],row[1]]								#Long, Lat
			self._locationCoordinates.append(elem)
			#print("LOCATION INDEX", row[0])
			#print("LOCATION COORDINATES", elem)

			self._locationIndex[i] = row[0]
			i+=1

		#print("\n\n=====",self._locationCoordinates,"=====\n\n",)
		self._location_kdTree = KDTree(self._locationCoordinates)

		self._objectCoordinates = []

		for index, row in self._df_objects.iterrows():
			elem = [row[2],row[1]]							#Long, lat
			self._objectCoordinates.append(elem)
			#self._objectIndex[index] = row[0]

		self._objects_kdTree = KDTree(self._objectCoordinates)

		print("Converted objects and OSM details to DataFrames")

		return ((self._df_locations, self._df_objects))

	def printToFile(self):
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

		self._df_locations.to_csv("data/osm_df.csv", index=False)
		self._df_objects.to_csv("data/obj_df.csv", index=False)

	def kMeans_membership(self, objs_to_cluster_df, numberOfClusters):
		print("Clustering with kMeans")
		kmeans = KMeans(n_clusters=numberOfClusters, random_state=0, n_init="auto")
		objs_to_cluster_df['cluster'] = kmeans.fit_predict(objs_to_cluster_df[['latitude','longitude']])
		centroids = kmeans.cluster_centers_
		
		self.inferLocation(objs_to_cluster_df, centroids,"kmeans")
		print(self._df_objects)

		plt.xlabel('Longitude')
		plt.ylabel('Latitude')
		plt.scatter(y=self._df_objects.latitude ,x=self._df_objects.longitude, c=self._df_objects.cluster, alpha =0.6, s=10)
		plt.scatter(y=self._df_locations['latitude'],x=self._df_locations['longitude'], label="Locations",alpha =0.6, s=10 )
		plt.savefig('../data/output/clusters.png')

	def dbscan_membership(self, epsilon=0.5/6371., minCluster=3, fuzzy_threshold=0):  # default is exact assignment
		#1/6371 is ~100m
		print("Clustering with DBScan")
		loc_arr = np.array(self._objectCoordinates)

		db_cluster =  DBSCAN(eps=epsilon, min_samples=minCluster).fit(np.radians(loc_arr))
		self._df_objects['cluster'] = db_cluster.labels_

		centroids = self.calculateCentroids(db_cluster.labels_) 

		dists = []
		for idx, row in self._df_objects.iterrows():
			obj_coord = (row['latitude'], row['longitude'])
			centroid_coord = centroids[row['cluster']]  # look up in centroid list
			dists.append(self.__distance__(obj_coord, centroid_coord))
   
		self._df_objects['assignment_prob'] = 1 - self.__normalize_probs__(dists, mask=list(self._df_objects['cluster'] != -1))
  
		# Fuzzy multiple asn
		if fuzzy_threshold > 0:
			df_multi_asn_objects = self._df_objects.copy()
			for idx, row in self._df_objects.iterrows():
				for centroid in centroids:
					obj_centroid_dist = self.__distance__((row['latitude'], row['longitude']), centroid)
					# if obj-centroid distance is within THRESHOLD% of range of obj-centroid distances we saw during exact assignment  
					threshold = fuzzy_threshold * (self.cluster_max_dist - self.cluster_min_dist)                     
					if (obj_centroid_dist - self.cluster_min_dist) < threshold:        
							df_multi_asn_objects = df_multi_asn_objects.append(row)

			self._df_objects = df_multi_asn_objects  

		self.inferLocation(self._df_objects, centroids,"dbscan")
		
		
	def __distance__(self, point1, point2):
		return np.linalg.norm(point1 - point2)
  
	def __normalize_probs__(self, column, mask):
		# expects a list mask of booleans, where True means we account for the datapoint as valid max or min
		valid_data =  np.array(column)[np.array(mask)]

		# Set class vars for fuzzy multiple assignment if applicable    
		self.cluster_min_dist = np.min(valid_data)  
		self.cluster_max_dist = np.max(valid_data)
  
		return_col = np.array((column - np.min(valid_data)) / (np.max(valid_data) - np.min(valid_data)))
		return_col[~np.array(mask)] = 0.5  # forcing the ones we don't count to have prob = 0.5
		return return_col

	def calculateCentroids(self, clusters):
		print("Calculating Centroids")
		centroids = []

		for cluster in range (0, (max(clusters)+1)): 								#+1 to account for indexing from 0
			cluster_df = self._df_objects.loc[self._df_objects['cluster'] == cluster]		# Get only the coords belonging to this cluster
			coords = []

			for index, obj in cluster_df.iterrows(): 								# Make the coords into a list, then numpy array
				coords.append([obj.latitude, obj.longitude])
			np_coords = np.array(coords)
			
			centroid = np.mean(np_coords,axis=0) 									# Get the midpoint of the array
			centroids.append(centroid) 												# Build list of centroids

		return(centroids)


	def inferLocation(self, objs_to_assign_df, centroids, method):
		#print("Inferring object location")
		mappings = {} 																#Dict so that arbitrary number of clusters can be used
		for centroid in range (0, (len(centroids))): 								# For each centroid
			d, i = self._location_kdTree.query(centroids[centroid],1) 				# Look up its nearest neighbour in the KD tree
			#idx = (list(self._locationIndex.keys()))[i]
			#print(self._locationIndex[idx])
			#print(self._locationIndex[i])
			#print(centroids[centroid])
			mappings[centroid] = self._locationIndex[i]

		objs_to_assign_df['predicted_location'] = objs_to_assign_df.cluster.map(mappings) 		# Infer that the nearest neighbour is the cluster location
	

	def evaluateClusters(self, df_to_eval, method):
		#Move this to own function later. Use Levenshtein at 0.7 to handle labelling differences. 
		matches = []

		for index,row in self._df_objects.iterrows():								
			if Levenshtein.ratio(row['predicted_location'], row["true_location"]) >= 0.7:
				matches.append("True")
			else:
				matches.append("False")

		df_to_eval[method+"_correct"] = matches

		print(df_to_eval)
