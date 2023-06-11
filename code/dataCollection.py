# Code for data extraction in GESTALT

#System Imports
import os, json
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

		#if self._kml_directory[-1] != "/":									#Prevent error from missing trailing slash
		#	self._kml_directory += "/"

		#filePath = self._kml_directory + kmlFileName

		#print("Opening", filePath)

		with open(kmlFileName, 'rt', encoding='utf-8') as f:					#Open the file (double UTF-8 required because of fastKML error)
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
				object_dict["longitude"] = photos_dict[photo]['longitude']
				object_dict["latitude"] = photos_dict[photo]['latitude']
				object_dict["date"] = photos_dict[photo]['photo_date']
				object_dict["origin"] = "flickr"
				object_dict["source"] = photos_dict[photo]['URL']
				object_dict["class_confidence"] = photos_dict[photo]['probabilities'][i]
			objects_dict["flickr_"+photo] = object_dict.copy()

																								# Report Telemetry
		print("Analyzed {num} photos".format(num=len(photos_dict.keys())))
		print("Detected {num} objects across those photos. The most objects in a photo was {max}, and there were an average of {avg} objects per photo".format(num=objectCount, max=maxObjects, avg=(objectCount/len(photos_dict.keys()))))
		print("The vocabulary has {num} unique terms for objects".format(num=len(vocab)))
		print("The vocabulary is:", vocab)

		return vocab, objects_dict 																# Return values




class osmQueryEngine():

	def __init__(self):
		pass

	def queryOSM(self,bbox,typeQuery):
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
		objectDict = {}

		overpass = Overpass()													#Initialize OSMTools classes. 
		nominatim = Nominatim()
																				#Query the API
		
		if typeQuery == "allobjects":
			query = overpassQueryBuilder(bbox=bbox, 
										elementType="node",
										conditions="count_tags() > 0")
			
			results = overpass.query(query)
			
			for element in results.elements():										# Build the dictionary 
				try:
					objectName = element.tags()['name']
				except KeyError:
					
					if list(element.tags().values())[0].lower() in ["yes", "no"]:
						try:
							objectName = list(element.tags().values())[1]
						except IndexError:
							objectName = list(element.tags().keys())[0]
					elif list(element.tags().keys())[0] == "created_by":
						try:
							objectName = list(element.tags().values())[1]
						except IndexError:
							pass
					else:
						objectName = list(element.tags().values())[0]

				latitude = element.geometry()['coordinates'][0]
				longitude = element.geometry()['coordinates'][1]
				objectID = str(element.id())
				objectDict[objectID] = {}
				#objectDict[objectID]['tags'] = list(element.tags())
				objectDict[objectID]['latitude'] = latitude
				objectDict[objectID]['longitude'] = longitude
				objectDict[objectID]["name"] = objectName
			
			return objectDict



		else:
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