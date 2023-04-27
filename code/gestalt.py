

##TODO:

# 1. Extract data from KML

# 2. Connect to OSM

# 3. Get Specific Locations from OSM

#System Imports
import os, sys, argparse


#Library Imports
from fastkml import kml 

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


if __name__ == "__main__":

	argparser = argparse.ArgumentParser()									# initialize the argParser

	argparser.add_argument(	"-d", "--directory", 							
							help="specifies the directory where KML files are stored",
							type=str,
							default="data/",
							required=False)	
	
	flags = argparser.parse_args()											# populate variables from command line arguments

	gestalt = TerrainExtractor(flags.directory)

	kmlList = gestalt.Get_kml_file_list()

	gestalt.Ingest_kml_file(kmlList[0])



