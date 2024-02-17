# Code for data extraction in GESTALT

#System Imports
import os, sys, json, requests, glob, time
from datetime import datetime
#Library Imports
from fastkml import kml 
from OSMPythonTools.overpass import Overpass, overpassQueryBuilder
from OSMPythonTools.nominatim import Nominatim
import flickrapi
from ultralytics import YOLO
from pathlib import Path

# User File Imports


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
					object_dict["object_prob"] = CLASS_CONFIDENCE
					object_dict["assignment_prob"] = 1
					try:
						object_dict["ground_truth_location"] = location.name
					except:
						object_dict["ground_truth_location"] = "None"
				
					objects_dict["kml_"+str(objectCount)] = object_dict.copy()

		#Report Telemetry 
		print("\n\nGenerated dictionary from", kmlFileName)
		print("Analyzed {num} regions".format(num=len(list(document[0].features()))))
		print("Analyzed {num} locations across those regions".format(num=locationCount))
		print("Detected {num} objects across those locations. The most objects in a location was {max}, and there were an average of {avg} objects per location".format(num=objectCount, max=maxObjects, avg=(objectCount/locationCount)))
		print("The vocabulary has {num} unique terms for objects".format(num=len(vocab)))
		print("The vocabulary is:", vocab,"\n")		

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
			try:
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
					object_dict["object_prob"] = photos_dict[photo]['probabilities'][i]
					object_dict["assignment_prob"] = 1
					object_dict["ground_truth_location"] = "None"
			except KeyError:
				print ("No Objects\n", photos_dict[photo])
			
			objects_dict["flickr_"+photo] = object_dict.copy() 									# Add a COPY (hooray for mutability...) of the dictionary to the parent dictionary

																								# Report Telemetry
		print("\n\nAnalyzed {num} photos".format(num=len(photos_dict.keys())))
		print("Detected {num} objects across those photos. The most objects in a photo was {max}, and there were an average of {avg} objects per photo".format(num=objectCount, max=maxObjects, avg=(objectCount/len(photos_dict.keys()))))
		print("The vocabulary has {num} unique terms for objects".format(num=len(vocab)))
		print("The vocabulary is:", vocab, "\n")

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
		results = overpass.query(query, timeout=100) 										# Extract the results by querying the database

		# TODO: FIX DATE
			
		for element in results.elements():										# Extract likely objects based on their attributes. 

			found = False
			
			#try:
			#	objectName = element.tags()['emergency']
			#	found = True
			#except KeyError:
			#	pass
			#print(element.tags())

			try:
				objectName = element.tags()['railway']
				found = True
			except KeyError:
				pass

			try:
				objectName = element.tags()['barrier']
				found = True
			except KeyError:
				pass

			try:
				objectName = element.tags()['power']
				found = True
			except KeyError:
				pass			
			
			try:
				objectName = element.tags()['highway']
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
				objectName = element.tags()['sport']
				found = True
			except KeyError:
				pass

			try:
				objectName = element.tags()['artwork_type']
				found = True
			except KeyError:
				pass

			try:
				objectName = element.tags()['leisure']
				found = True
			except KeyError:
				pass

			try:
				objectName = element.tags()['historic']
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
				objectDict[objectID]['object_prob'] = CLASS_CONFIDENCE
				objectDict[objectID]['assignment_prob'] = 1
				objectDict[objectID]["ground_truth_location"] = "None"

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
				placeName = element.tags()['historic_landmark']
				found = True
			except KeyError:
				pass 		

			try:
				placeName = element.tags()['name']
				found = True
			except KeyError:
				pass

			try:
				placeName = element.tags()['surveillance'] 							#Get rid of named surveillance cameras
				found = False
			except KeyError:
				pass	

			try:
				placeName = element.tags()['bicycle_rental'] 							#Get rid of named surveillance cameras
				found = False
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
				locationDict[locationID]["ground_truth_location"] = "None"

			
			locationCount +=1

				
		# Print telemetry to the user	
		print("\n\nQuery got {num} possible locations from OSM".format(num=len(results.elements())))
		print("Added {num} locations of that original query result. {count} were dropped for not being locations, or poor data quality\n".format(num=locationCount-droppedCount, count=droppedCount))
		#print("The names of all the locations are", placenames)

		return locationDict

class PhotoDownloader():
	'''
	Class to hold the objects and methods relating to querying the FlickrAPI for the GESTALT Project
	INPUT ARGS:
		Nil
	FUNCTIONS: 
		-
		-
		-
	OUTPUTS:
		Photos downloaded from the flickrAPI within a given bounding box into the data/photos directory
		A JSON dump of metadata affiliated with those photos into the same directory.
	'''

	def __init__(self):
		#Get API keys from environment variables. (API access can be requested here: https://www.flickr.com/services/api/misc.api_keys.html)
		self._api_key = os.getenv('flickr_key')
		self._api_secret = os.getenv('flickr_secret')
		#Initialize the FlickrAPI object
		self._flickr = flickrapi.FlickrAPI(self._api_key, self._api_secret, format='parsed-json')
	
	#Functions

	def constructURL(self, photo):
		'''
		constructs a URL compatible with the flickrAPI based on a 'photo' returned by the search function
		INPUT ARGS: 
			photo - dictionary - describing a single photo returned from the flickr API
		PROCEDURE:
			given the relevant fields in the photo result passed to the function, construct the url to that photo on flickr. 
		OUTPUT:
			returnTuple - tuple, consisiting of: 
				photoid - string - the unique identifier of the photo in flickr's database
				url - string - the URL to access the photo described in the input parameter
				secret - string - the 'secret' parameter extracted from the input photo description (used to access files on the flickr servers)
		'''     

		server_id = photo['server']
		photo_id = photo['id']
		secret = photo['secret']
		size = "b"

		url = "https://live.staticflickr.com/{serverid}/{id}_{secret}_{sizesuffix}.jpg".format(serverid=server_id, id=photo_id, secret=secret, sizesuffix=size)

		returnTuple = (photo['id'], secret, url)
		return returnTuple


	def getMetadata(self, photoId, photoSecret):
		'''
		constructs a dictionary containing relevant data about the photo being downloaded. 
		INPUT ARGS:
			apiObject - flickrAPI object - the flickr API query tool
			photoID - string - the unique identifier of a photo on flickr's servers
			photoSecret - string - a secret identifier used to access photos on flickr's servers
		PROCESS:
			Create the dictionary to store the results
			Query the API for the EXIF data and the GEO data 
				nb some GPS data is in the EXIF, but we found it to be truncated and inconsistent
			Parse out the relevant fields of the EXIF and GEO data into the dictionary
		OUTPUT:
			photoData - dictionary with keys [photo_bearing_ref, photo_bearing, photo_data, longitude, latitude]    
				nb: some additional keys are added later
				nb: Initialized to NULL - used later in error checking
		'''
	

		photoData = {}                                                  # Initialize dictionary to hold results
		photoData["photo_bearing_ref"] = "NULL"
		photoData["photo_bearing"] = "NULL"
		photoData["photo_date"] = "NULL"
		photoData["longitude"] = "NULL"
		photoData["latitude"] = "NULL"

		try:
			exif = self._flickr.photos.getExif(photo_id=photoId,                  # Query the flickr API for EXIF data
										secret=photoSecret)
			
			for ex in exif['photo']['exif']:                                # Parse the relevant EXIF data
				if ex['tag'] == "GPSImgDirection":
					photoData["photo_bearing"] = (ex['raw']['_content'])
				if ex['tag'] == "GPSImgDirectionRef":
					photoData["photo_bearing_ref"] = (ex['raw']['_content'])
				if ex['tag'] == "DateTimeOriginal":
					photoData["photo_date"] = (ex['raw']['_content'])
		except:
			print("Unable to get EXIF for", photoId)
				
		
		geo = self._flickr.photos.geo.getLocation(api_key=self._api_key,            # Query the flickr API for GEO Data
													photo_id=photoId,
													extras="geo,dateTaken")        
																		# Parse the relevant GEO data
		
		photoData["longitude"] = geo['photo']['location']['longitude']
		photoData["latitude"] = geo['photo']['location']['latitude']



		return(photoData)

	def searchBoundingBox(self, LL_LON, LL_LAT, TR_LON, TR_LAT):
		'''
		Searches the flickr API for images within a given bounding box
		INPUT ARGS: 
			LL_LON - string - the longitude for the lower left corner of the bounding box. Will be between -180 and +180
			LL_LAT - string - the latitude for the lower left corner of the bounding box. Will be between -90 and +90
			TR_LON - string - the longitude for the top right corner of the bounding box. Will be between -180 and +180.
			TR_LAT - string - the latitude for the top right corner of the bounding box. Will be between -90 and +90. 
		PROCESS:
			Create the bounding box string and query the API with it
		OUTPUT:
			returnTuple - tuple - contains: 
				photos - dict - the results of the query
				b_box_dict - dict - a dictionary of bounding box values for use by later functions. 
		'''
		
		b_box_dict = {
			"LL_LON":LL_LON,
			"LL_LAT":LL_LAT,
			"TR_LON":TR_LON,
			"TR_LAT":TR_LAT
		}

		b_box = LL_LON+","+LL_LAT+","+TR_LON+","+TR_LAT
		
		print("\n\n==========QUERYING FLICKR==========\n")
		print("b_box:", b_box)

		results = {}

		results[1] = self._flickr.photos.search(bbox=b_box,
											safe_search=1,
											content_type=1,
											has_geo=1,
											min_taken_date="2020-01-01 00:00:00")

		print("NUM PAGES", int(results[1]['photos']['pages']))
		for i in range(1,int(results[1]['photos']['pages'])+1):
			results[i] = self._flickr.photos.search(bbox=b_box,
											safe_search=1,
											content_type=1,
											has_geo=1,
											min_taken_date="2020-01-01 00:00:00",
											page=i)                                        
			
			
		returnTuple = (results, b_box_dict)
		return returnTuple


	def processQueryResults(self, queryResults, outputDirectory, page=1):
		'''
		processes the results of a bounding box query to the Flickr API
		INPUT ARGS:
			outputDirectory - string - filepath to the output directory
		PROCESSES: 
			Check the output directory exists
			Step through each photo, get its metadata and save it to file
			Combine all metadata to a JSON and dump to same file

		OUTPUTS: 
			Photo Files Outputted to the outputDirectory
			JSON file with photo Metadata to the Output Directory
		'''


		try:                                                            #Make the output directory
			os.makedirs(outputDirectory)
		except FileExistsError:
			#already Exists
			pass

		imageMetadata = {}                                              #Init the metadata dict

		#Handle the case that it fails, so we don't re-process the same files, pull up the dictionary of metadata from storage. 
		try:
			for file in os.listdir(outputDirectory): 
				if file.startswith("metadata"): 															
					with open(outputDirectory+"/"+file, "r") as inObjs:
						objects = json.load(inObjs)
						imageMetadata.update(objects)
		except FileNotFoundError:
			pass
						

		for page in range(page, len(queryResults.keys())):
			print("PROCESSING PAGE # :", page)
			#print("page keys:", page.keys())    
			for photo in queryResults[page]['photos']['photo']:                         #Loop through each photo in the query results
				photo_id, photoSecret, photoURL = self.constructURL(photo)       #construct the URL to get the photos from the search results
				
				if photo_id in imageMetadata.keys():								#Stop double handling of photos when the API fails. 
					print("Already Extracted")
					continue 
				else:
					print("EXTRACTING PHOTO", photo_id)
					try:
						photoFile = requests.get(photoURL)                          #Download and save the photo
					except:
						print("Error getting photo on page", page) 					#Resilience to API gremlins
						print("Sleeping 10 seconds and trying again")
						time.sleep(10)
						try: 
							photoFile = requests.get(photoURL)
						except:
							print("Error getting photo on page", page)
							print("Passing photo:", photo_id)
				

					photoFileName = outputDirectory+"/"+photo_id+".jpg"
					
					imageMetadata[photo_id] = self.getMetadata(photo_id, photoSecret)    #Extract the image metadata
					imageMetadata[photo_id]['URL'] = photoURL                       #Add URL to the metadata

					with open(photoFileName, "wb") as out:                          #Save the file to the output directory
						out.write(photoFile.content)


			metadataFile = outputDirectory+"/metadata_page:"+str(page)+".json"                     #Save the metadata to the output directory 
			with open(metadataFile, 'w') as out:
				print("Dumping metadata to", metadataFile )
				json.dump(imageMetadata, out, indent=4)


		
	def detect_tags_from_jpgs_in_directory(self, directory_name, json_filename):
		# Find all jpegs in the directory
		#full_list_of_img_files = glob.glob(os.path.join(directory_name,"*.jpg")) # Glob has just given up for me. TODO: Fix glob here. 
		full_list_of_img_files = []
		#print(os.listdir(directory_name))
		try:
			for file in os.listdir(directory_name): 
				if file.split(".")[-1] == "jpg":
					full_list_of_img_files.append(directory_name+"/"+file)
		except FileNotFoundError:
			print("Oops")
			pass
				
		#print("LOOKING IN:",os.path.join(directory_name,"*.jpg"))
		#print("IMAGE FILES\n", full_list_of_img_files)

		json_dict = {}                                              #Init the JSON dict

		#Handle the case that it fails, so we don't re-process the same files, pull up the dictionary of metadata from storage. 
		try:
			for file in os.listdir(directory_name): 
				if file.startswith("metadata"): 															
					with open(directory_name+"/"+file, "r") as inObjs:
						objects = json.load(inObjs)
						json_dict.update(objects)
		except FileNotFoundError:
			pass

		#print(json_dict.keys())

		print("RUNNING YOLO TO DETECT OBJECTS IN COLLECTED PHOTOS\n")

		# Chunk images into lists of size MAX_FILES_OPEN
		MAX_FILES_OPEN = 200                                                            #BUG: will trigger a OSError 24 'too many files open' 
																						#WORKAROUND:    before running the code run the command  in your shell "ulimit -n 1000" 
																						#               where 1000 is whatever number you want to have as the max file limit
		for i in range(0, len(full_list_of_img_files), MAX_FILES_OPEN):
			list_of_img_files = full_list_of_img_files[i : i + MAX_FILES_OPEN]
			#list_of_img_files = full_list_of_img_files										# Bug workaround where it wasn't running on sub-lists
			# Find all jpegs in the directory
			#list_of_img_files = glob.glob(os.path.join(directory_name,"*.jpg"))

			# Read in json file
			#json_dict = json.load(open(json_filename+".json"))

			# Instantiate model
			model = YOLO("yolov8m.pt")

			# Run images through model and get results
			results = model.predict(list_of_img_files, verbose=False, stream=False)			#Bug workaround, wouldn't run not in streaming mode for DC dataset. 

			#Check that we got results for every image
			assert len(results) == len(list_of_img_files)

			# Loop over each image

			for idx in range(len(list_of_img_files)):
				file_id = Path(list_of_img_files[idx]).stem  # extract filename without path or extension
				result = results[idx]
				tags = []
				coords = []
				probs = []
				# Loop over each object detected in the image
				for box in result.boxes:
					class_id = result.names[box.cls[0].item()]
					cords = box.xyxy[0].tolist()
					cords = [round(x) for x in cords]
					conf = round(box.conf[0].item(), 2)

					tags.append(class_id)  # object type like person or bench
					coords.append(cords)  # coordinates in the image like [121, 632, 207, 732]
					probs.append(conf)  # confidence score like 0.81
				
				try:
					json_dict[file_id].update({"objects":tags, "coordinates":coords, "probabilities":probs})
				except KeyError:
					print("NOT FOUND:",file_id,"\n Tags:",tags,"\n coords:", coords, "\n probs", probs)

		return json.dumps(json_dict,indent=4)
