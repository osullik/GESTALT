# Code for data extraction in GESTALT

#System Imports
import os, json
from datetime import datetime
#Library Imports
from fastkml import kml 
from OSMPythonTools.overpass import Overpass, overpassQueryBuilder
from OSMPythonTools.nominatim import Nominatim


class TerrainExtractor():

	def __init__(self):
		pass
		#self._kml_directory = kml_directory

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
		a function to take a KML file and transform it into an object-centric dicionary
		INPUT ARGS: 
			kmlFileName: the path to the kmlFile to be ingested
		PROCESS:
			Iterate through each "region (top level directory in the KML)
			Iterate through each "location (second level directory in the KML)
			For each object in the location create a dictonary with all relevant metadata and add the obejct names to a set
			Combine the dictionaries into an objects dictionary. 
			Report the results of the telemetry
		OUTPUTS:
			vocab - set of strings - the set of unique object terms observed in the objects extracted from the photos
			objects_dict - dict of dicts of the form: 
			
				objectID:
					name:
					longitude:
					latitude:
					date:
					origin:
					source:
					class_confidence:
		'''

		CLASS_CONFIDENCE = 1.0 												# Set the confidence of the object class classification for the KML files

		with open(kmlFileName, 'rt', encoding='utf-8') as f:				#Open the file (double UTF-8 required because of fastKML error)
			 doc = f.read().encode('utf-8')

		objects_dict = {}													#Initialize dict to return 
		object_dict = {}

		vocab = set() 														# Telemetry variables		
		locationCount = 0
		objectCount = 0
		maxObjects = 0

		k = kml.KML()														# Create KML Object
		k.from_string(doc)													# Convert raw KML into Object
		document = list(k.features())										# Extract the document from the object


		for region in (list(document[0].features())):						# Extract the regions
			#regName = region.name											# regName not required in new implementation, leaving in case of future restructuring
			
			for location in (list(region.features())):						# Extract the locations
				if len(list(location.features())) > maxObjects:
					maxObjects = len(list(location.features()))
				locationCount +=1
				
				#locName = location.name									# locName not required in new implementation, leaving in case of future restructuring
				
				for terrainFeature in (list(location.features())):			# Extract the Fobjects
					vocab.add(terrainFeature.name)
					objectCount += 1
					name = terrainFeature.name 
					#description = terrainFeature.description				# Description field is a string with multiple pairs of format key:value that describe attributes of an object. Not used in current implementation. 
					latitude = terrainFeature.geometry.y
					longitude = terrainFeature.geometry.x
																			# Build the dictionary

					object_dict["name"] = name								# Create dict entry for this object 
					object_dict["longitude"] = longitude
					object_dict["latitude"] = latitude
					object_dict["date"] = str((datetime.fromtimestamp(os.path.getmtime(kmlFileName)).strftime("%d-%m-%y %H:%M:%S"))) # Get the datetime the file was created, convert from unix to DateTime and format it. 
					object_dict["origin"] = "kml"
					object_dict["source"] = kmlFileName 					# Source of the object points to the KML file it came from
					object_dict["class_confidence"] = CLASS_CONFIDENCE
				
					objects_dict["kml_"+str(objectCount)] = object_dict.copy()

		#Report Telemetry 
		print("Generated dictionary from", kmlFileName)
		print("Analyzed {num} regions".format(num=len(list(document[0].features()))))
		print("Analyzed {num} locations across those regions".format(num=locationCount))
		print("Detected {num} objects across those locations. The most objects in a photo was {max}, and there were an average of {avg} objects per location".format(num=objectCount, max=maxObjects, avg=(objectCount/locationCount)))
		print("The vocabulary has {num} unique terms for objects".format(num=len(vocab)))
		print("The vocabulary is:", vocab)		

		return objects_dict, vocab

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
	
	def ingest_flickr_objects(self, photos_file):
		'''
		a function to take the metadata_objects.json file outputted by the photoDownloader and transform it into an object-centric dicionary
		INPUT ARGS: 
			photos_file: the path to the file containing the results of the object detection run by the photoDownloader component of data collection. 
		PROCESS:
			Iterate through each photo
			For each object in the photo create a dictonary with all relevant metadata and add the obejct names to a set
			Combine the dictionaries into an objects dictionary. 
			Report the results of the telemetry
		OUTPUTS:
			vocab - set of strings - the set of unique object terms observed in the objects extracted from the photos
			objects_dict - dict of dicts of the form: 
			
				objectID:
					name:
					longitude:
					latitude:
					date:
					origin:
					source:
					class_confidence:
		'''

		objects_dict = {}																		# Initialize structures for data collection and 
		object_dict = {}
		
		vocab = set()																			# Initialize data structures for telemetry 
		objectCount = 0
		maxObjects = 0

		print("INGESTING FLICKR METADATA")

		with open(photos_file, "r") as infile: 													# Get the file outputted by the photoDownloader
			photos_dict = json.load(infile)

		for photo in photos_dict.keys(): 														# Step through each photo
			if len(photos_dict[photo]["objects"]) > maxObjects:
				maxObjects = len(photos_dict[photo]["objects"])

			for i in range(0, len(photos_dict[photo]["objects"])): 								# Step through each object (using numeric indexing because objects and probabilites are lists with shared indexing)
				
				objectCount +=1 																# Update telemetry  
				vocab.add(photos_dict[photo]['objects'][i])

				object_dict["name"] = photos_dict[photo]['objects'][i] 							# Create dict entry for this object 
				object_dict["longitude"] = float(photos_dict[photo]['longitude'])
				object_dict["latitude"] = float(photos_dict[photo]['latitude'])
				object_dict["date"] = photos_dict[photo]['photo_date']
				object_dict["origin"] = "flickr"
				object_dict["source"] = photos_dict[photo]['URL']
				object_dict["class_confidence"] = photos_dict[photo]['probabilities'][i]
			
			objects_dict["flickr_"+photo] = object_dict.copy() 									# Add a COPY (hooray for mutability...) of the dictionary to the parent dictionary

																								# Report Telemetry
		print("Analyzed {num} photos".format(num=len(photos_dict.keys())))
		print("Detected {num} objects across those photos. The most objects in a photo was {max}, and there were an average of {avg} objects per photo".format(num=objectCount, max=maxObjects, avg=(objectCount/len(photos_dict.keys()))))
		print("The vocabulary has {num} unique terms for objects".format(num=len(vocab)))
		print("The vocabulary is:", vocab)

		return vocab, objects_dict 																# Return values


class osmQueryEngine():

	def __init__(self):
		pass

	def queryOSMforObjects(self, bbox):
		'''
		queries the OSM database for objects within a bounding box
		INPUT ARGS:
			bbox - string - bounding box to search in
		PROCESS:
			query the API
			Extract elements likely to be objects based on their attributes; list developed by manual examination of the OSM ontology https://raw.githubusercontent.com/doroam/planning-do-roam/master/Ontology/tags.owl
			Build a dictionary and return it
		OUTPUT
			vocab - set of strings - the list of unique terms that describe the objects added from OSM
			object_dict - dict of dicts of the form: 
			
				objectID:
					name:
					longitude:
					latitude:
					date:
					origin:
					source:
					class_confidence: 
		'''

		CLASS_CONFIDENCE = 0.7 													#Set confidence to reflect the untrusted labeller aspect.
		objectDict = {}

		overpass = Overpass()													#Initialize OSMTools classes. 
																				#Query the API
		vocab = set()															# Initialize data structures for telemetry 
		objectCount = 0
		droppedCount = 0

		query = overpassQueryBuilder(bbox=bbox, 								# build Query the API for all nodes with at least one tag
										elementType="node",
										conditions="count_tags() > 0")		
		results = overpass.query(query) 										# Extract the results by querying the database

		# TODO: FIX DATE
			
		for element in results.elements():										# Extract likely objects based on their attributes. 

			found = False
			
			#try:
			#	objectName = element.tags()['emergency']
			#	found = True
			#except KeyError:
			#	pass

			try:
				objectName = element.tags()['highway']
				found = True
			except KeyError:
				pass

			try:
				objectName = element.tags()['historic']
				found = True
			except KeyError:
				pass

			try:
				objectName = element.tags()['leisure']
				found = True
			except KeyError:
				pass

			try:
				objectName = element.tags()['man_made']
				found = True
			except KeyError:
				pass

			try:
				objectName = element.tags()['natural']
				found = True
			except KeyError:
				pass

			try:
				objectName = element.tags()['power']
				found = True
			except KeyError:
				pass

			try:
				objectName = element.tags()['railway']
				found = True
			except KeyError:
				pass

			try:
				objectName = element.tags()['sport']
				found = True
			except KeyError:
				pass

			if found == False: 														# If element not in those attributes, drop it
				droppedCount +=1 													# Telemetry for number of objects dropped
			else:
				latitude = element.geometry()['coordinates'][1] 						# Extract lat, long etc. 
				longitude = element.geometry()['coordinates'][0]
				objectID = "osm_"+str(element.id())
				objectDict[objectID] = {}
				
				objectDict[objectID]["name"] = objectName 								#Build the dict
				objectDict[objectID]['longitude'] = longitude
				objectDict[objectID]['latitude'] = latitude
				try:
					objectDict[objectID]['date'] = element.timestamp()
				except TypeError:
					objectDict[objectID]['date'] = datetime.now().strftime("%d-%m-%y %H:%M:%S")				
				objectDict[objectID]['origin'] = "osm"
				objectDict[objectID]['source'] = "https://www.openstreetmap.org/node/{node}".format(node=str(element.id()))
				objectDict[objectID]['class_confidence'] = CLASS_CONFIDENCE

				vocab.add(objectName) 													# Add the term to the vocab
			objectCount += 1

		# Print telemetry to the user	
		print("Query got {num} objects from OSM".format(num=len(results.elements())))
		print("Added {num} objects of that original query result. {count} were dropped for not being objects, or poor data quality".format(num=objectCount-droppedCount, count=droppedCount))
		print("The vocabulary has {num} terms".format(num=len(vocab)))
		print("The vocabulary is:", vocab)
		
		return objectDict, vocab

	
	def queryOSMforLocations(self,bbox,typeQuery):
		'''
		input args:
    		- bbox: The bounding box to search within, as a list of four decimal values representing the minimum and maximum longitude and latitude values.
   			- typeQuery: The value to search for within the craft tag of the nodes. When "all_locations" retrieves all locations within a given bounding box. 

		actions:
		    - Initialize an empty dictionary called locationDict.
		    - Use the Overpass API to query OpenStreetMap for all nodes at least one tag.
		    - Loop through the results of the query and extract the location name, latitude, and longitude of each element.
		    - Store the extracted location data in the locationDict dictionary with the location name as the key and the latitude and longitude as the values.
		    - Return the locationDict dictionary.

		outputs:
    		- locationDict: A dictionary containing the location names as keys and the corresponding latitude and longitude values as values.
		'''
		CLASS_CONFIDENCE = 0.7

		overpass = Overpass()													#Initialize OSMTools classes. 
		
		locationCount = 0
		droppedCount = 0
		placenames = set()

		locationDict = {}														# Initialize dict to return 
		if typeQuery == "all_locations":
			
			query = overpassQueryBuilder(bbox=bbox, 								# build Query the API for all nodes with at least one tag
										elementType="node",
										conditions="count_tags() > 0")		
			results = overpass.query(query) 										# Extract the results by querying the database
		
		else:
			query = overpassQueryBuilder(	bbox=bbox, 
											elementType="node",
											selector="'craft'="+typeQuery)

			results = overpass.query(query)

			
		for element in results.elements():										# Extract likely objects based on their attributes. 
			
			found=False
			
			try:
				placeName = element.tags()['name']
				found = True
			except KeyError:
				pass

			try:
				placeName = element.tags()['highway'] 							#Get rid of named busstops and overpasses
				found = False
			except KeyError:
				pass
		
			if found == False: 														# If element not in those attributes, drop it
				droppedCount +=1 													# Telemetry for number of objects dropped
			
			else:
				placenames.add(placeName)

				locationID = "osm_"+str(element.id())
				name = placeName
				latitude = element.geometry()['coordinates'][1]
				longitude = element.geometry()['coordinates'][0]

				locationDict[locationID] = {}
				locationDict[locationID]['name'] = name
				locationDict[locationID]['longitude'] = longitude
				locationDict[locationID]['latitude'] = latitude
				try:
					locationDict[locationID]['date'] = element.timestamp()
				except TypeError:
					locationDict[locationID]['date'] = datetime.now().strftime("%d-%m-%y %H:%M:%S")
				locationDict[locationID]['origin'] = "osm"
				locationDict[locationID]['source'] = "https://www.openstreetmap.org/node/{node}".format(node=str(element.id()))
				locationDict[locationID]['class_confidence'] = CLASS_CONFIDENCE

			
			locationCount +=1

				
		# Print telemetry to the user	
		print("Query got {num} possible locations from OSM".format(num=len(results.elements())))
		print("Added {num} objects of that original query result. {count} were dropped for not being locations, or poor data quality".format(num=locationCount-droppedCount, count=droppedCount))
		#print("The names of all the locations are", placenames)

		return locationDict