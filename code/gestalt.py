
#System Imports
import argparse, json, sys, os

#Library Imports

#User Imports

from dataCollection import TerrainExtractor, osmQueryEngine, PhotoDownloader
from ownershipAssignment import OwnershipAssigner
from conceptMapping import ConceptMapper
from search import InvertedIndex



if __name__ == "__main__":

	argparser = argparse.ArgumentParser()									# initialize the argParser

	argparser.add_argument(	"-ql", "--queryOsmLocations", 							
							help="engage mode to issue a query to OpenStreetMaps for locations",
							action="store_true",
							default=False,
							required=False)	

	argparser.add_argument(	"-qo", "--queryOsmObjects", 							
							help="engage mode to issue a query to OpenStreetMaps for objects",
							action="store_true",
							default=False,
							required=False)	
		
	argparser.add_argument( "-b", "--boundingbox", 
							help="specifies the bounding box to be passed to OSM", 
							nargs='+',
							default=None,
							required=False)
	
	argparser.add_argument( "-p", "--photosFromFlickr",
							help="engage mode to ingest the processed metadata_objects.json from the PhotoDownloader. Needs to be used in conjunction with -f and -o",
							action="store_true",
							default=False,
							required=False)
	
	argparser.add_argument( "-s", "--searchterms",
							help="search terms to pass to the overpass turbo API",
							nargs="+",
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
							help="kmlfile(s) to ingest)", 
							nargs="+", 
							default=None,
							required=False)

	argparser.add_argument(	"-oa", "--ownershipAssignment", 							
							help="Define the location membership inference method: 'kmeans', 'dbsweep', 'partitioning'",
							type=str,
							default="None",
							required=False)

	argparser.add_argument("-id", "--inputDirectory",
							help="The directory to get files from for the Ownership Assignment", 
							type=str, 
							required=False)
	
	argparser.add_argument("-od", "--outputDirectory",
							help="The directory to write files created by the Ownership Assignment", 
							type=str, 
							required=False)
	
	argparser.add_argument("-n", "--numClusters", 
							help="number of clusters to use for KMeans",
							type=int, 
							required=False)
	
	argparser.add_argument("-e", "--epsilon", 
							help="Epsilon value for DBSCAN - Float",
							type=float, 
							required=False)
	
	argparser.add_argument("-gs", "--gestaltSearch", 
							help="Invoke Gestalt's Search Mode",
							action="store_true",
							required=False)
	
	argparser.add_argument("-if", "--inputFile", 
							help="Input file to create the inverted index from",
							type=str,
							required=False)
	
	argparser.add_argument(	"-pd", "--photoDownloader", 							
							help="Mode to download files from flickr",
							action="store_true",
							default=False,
							required=False)	
	
	argparser.add_argument(	"-ccm", "--createConceptMaps", 							
							help="Create concept maps based on the predicted locations",
							action="store_true",
							default=False,
							required=False)	
	
	flags = argparser.parse_args()																		# populate variables from command line arguments


	if flags.queryOsmObjects== True: 																		# Check to see if GESTALT should execute in OSM Query mode. 
		bbox = flags.boundingbox
		outputfile = flags.output
		searchterms = flags.searchterms
		oqe = osmQueryEngine()
		
		if searchterms[0] == "allobjects":
			osmDict, vocab = oqe.queryOSMforObjects(bbox)
			outputfileName = (outputfile+"_"+"".join(bbox)+"_allobjects.json")
		else:
			osmDict = oqe.queryOSMforObjects(bbox, searchterms[0]) 													# Create the dictionary off the first search term 
			for i in range(1, len(searchterms), 1): 														# Loop through other search terms and merge each set of results into one big dict
				newDict = oqe.queryOSMforObjects(bbox, searchterms[i])
				osmDict.update(newDict)
			outputfileName = (outputfile+"".join(searchterms)+".json") 												#Define the filename to output to
		
		with open(outputfileName,'w') as outfile: 															#dump output to json
			json.dump(osmDict, outfile, indent=4)
			print("Successfully outputted data to \"{outputLoc}\"".format(outputLoc=outputfileName)) 		#user feedback. 
		exit()

	if flags.queryOsmLocations== True: 																		# Check to see if GESTALT should execute in OSM Query mode. 
		bbox = flags.boundingbox
		outputfile = flags.output
		searchterms = flags.searchterms
		oqe = osmQueryEngine()
		
		if searchterms[0] == "alllocations":
			osmDict = oqe.queryOSMforLocations(bbox, searchterms[0])
			outputfileName = (outputfile+"_"+"".join(bbox)+"_alllocations.json")
		else:
			osmDict = oqe.queryOSMforLocations(bbox, searchterms[0]) 													# Create the dictionary off the first search term 
			for i in range(1, len(searchterms), 1): 														# Loop through other search terms and merge each set of results into one big dict
				newDict = oqe.queryOSMforLocations(bbox, searchterms[i])
				osmDict.update(newDict)
			outputfileName = (outputfile+"".join(bbox)+"_alllocations.json") 												#Define the filename to output to
		
		with open(outputfileName,'w') as outfile: 															#dump output to json
			json.dump(osmDict, outfile, indent=4)
			print("Successfully outputted data to \"{outputLoc}\"".format(outputLoc=outputfileName)) 		#user feedback. 
		exit()

	if flags.kmlIngestMode == True: 																	# Check to see if gestalt should execute in KML Ingestion mode. 
		sourceFiles = flags.fileSource
		outputfile = flags.output
		tex = TerrainExtractor()
		for file in sourceFiles:
			print(file)
			fullfilename = file.split("/")[-1] 															#get everything right of final "/" (i.e. filename)
			shortFileName = fullfilename.split(".")[0] 													#get everything left of the "." (i.e not filetype)
			objectLocations, vocab = tex.Ingest_kml_file(file) 												#get the dictionary from ingesting KML file
			outputfileName = outputfile+"_"+shortFileName+".json" 										#set the output name to be distinct for the file
			with open(outputfileName,'w') as outfile: 													#output to JSON
				json.dump(objectLocations, outfile, indent=4)
			print("Successfully outputted data to \"{outputLoc}\"".format(outputLoc=outputfileName)) 	#user feedback
		exit()

	if flags.photosFromFlickr==True:
		print("INGESTING FROM FLICKR")
		object_file = flags.inputFile
		outputfile = flags.output
		tex = TerrainExtractor()
		fullfilename = object_file.split("/")[-1] 													#get everything right of final "/" (i.e. filename)
		shortFileName = fullfilename.split(".")[0] 													#get everything left of the "." (i.e not filetype)
		vocab, objectLocations = tex.ingest_flickr_objects(object_file) 									#get the dictionary from ingesting KML file
		outputfileName = outputfile+"_"+shortFileName+".json" 										#set the output name to be distinct for the file
		with open(outputfileName,'w') as outfile: 													#output to JSON
			json.dump(objectLocations, outfile, indent=4)
		print("Successfully outputted data to \"{outputLoc}\"".format(outputLoc=outputfileName)) 	#user feedback
		exit()


	if flags.ownershipAssignment.lower() == "kmeans":

		prefix = flags.inputDirectory																#Read parameters for the file
		outputFile = flags.outputDirectory
		numClusters = flags.numClusters

		objectsDict = {}																			#Initilaize the Dicts
		locationsDict = {}
																									
		for file in os.listdir(prefix):																# Load in the files
			print("Adding",file,"to K-Means")
			
			if file.startswith("objects"): 															# Get the objects files
				with open(prefix+"/"+file, "r") as inObjs:
					objects = json.load(inObjs)
				objectsDict.update(objects)
			
			if file.startswith("locations"):														# Get the locations files
				with open(prefix+"/"+file, "r") as inLocs:
					locations = json.load(inLocs)
				locationsDict.update(locations)
		
		ownerAssigner = OwnershipAssigner(locations, objects) 										# Initalize the ownership assigner
		
		df_locations, df_objects = ownerAssigner.convertToDataFrame(locationsDict, objectsDict)		# Convert the dictionaries created from the JSON inputs to Pandas Dataframes

		ownerAssigner._df_locations.to_csv(outputFile+"/locations.csv", index=False) 				# Write the dataframes to file before clustering
		ownerAssigner._df_objects.to_csv(outputFile+"/objects.csv", index=False)

		ownerAssigner.kMeans_membership(df_objects, len(locationsDict.keys())) 						# Conduct clustering
		clusters = ownerAssigner._df_objects["cluster"] 											# Infer Ownership
		print(clusters.value_counts())

		ownerAssigner._df_objects.to_csv(outputFile+"/KMEANS_PredictedLocations.csv", index=False)	# Print the Clustered file
		exit()

if flags.ownershipAssignment.lower() == "dbscan":
		
		prefix = flags.inputDirectory																#Read parameters for the file
		outputFile = flags.outputDirectory
		numClusters = flags.numClusters
		epsilon= flags.epsilon
		minCluster = flags.numClusters

		objectsDict = {}																			#Initilaize the Dicts
		locationsDict = {}

		for file in os.listdir(prefix):																# Load in the files
			print("Adding",file,"to K-Means")
			
			if file.startswith("objects"): 															# Get the objects files
				with open(prefix+"/"+file, "r") as inObjs:
					objects = json.load(inObjs)
				objectsDict.update(objects)
			
			if file.startswith("locations"):														# Get the locations files
				with open(prefix+"/"+file, "r") as inLocs:
					locations = json.load(inLocs)
				locationsDict.update(locations)
		
		ownerAssigner = OwnershipAssigner(locations, objects) 										# Initalize the ownership assigner
		
		df_locations, df_objects = ownerAssigner.convertToDataFrame(locationsDict, objectsDict)		# Convert the dictionaries created from the JSON inputs to Pandas Dataframes

		ownerAssigner._df_locations.to_csv(outputFile+"/locations.csv", index=False) 				# Write the dataframes to file before clustering
		ownerAssigner._df_objects.to_csv(outputFile+"/objects.csv", index=False)


		ownerAssigner.dbscan_membership(epsilon,minCluster) 										# Cluster the objects
		clusters = ownerAssigner._df_objects["cluster"] 											# Infer the location
		print(clusters.value_counts())

		ownerAssigner._df_objects.to_csv(outputFile+"/DBSCAN_PredictedLocations.csv", index=False)	# Save to file
		exit()

if flags.photoDownloader == True:
	b_box = flags.boundingbox
	print("BOUNDING BOX:",b_box)
	outputDirectory = flags.outputDirectory+(str(b_box))

	downer = PhotoDownloader()
	photos, b_box_dict = downer.searchBoundingBox(b_box[0],b_box[1],b_box[2],b_box[3])
	photos=outputDirectory
	downer.processQueryResults(photos,outputDirectory)

	json_file = outputDirectory+"/metadata"
	output = downer.detect_tags_from_jpgs_in_directory(outputDirectory, json_file)
	with open(json_file+"_objects.json", "w") as out:
		out.write(output)

	exit()

if flags.createConceptMaps==True: 
	predictedLocationsCSV = flags.inputFile
	outputDirectory = flags.outputDirectory
	CM = ConceptMapper()
	conceptMaps = CM.createConceptMap(predictedLocationsCSV)
	predictedLocationsCSV = predictedLocationsCSV.split("/")[-1]
	predictedLocationsCSV = predictedLocationsCSV.split(".")[0]

	outputFile = outputDirectory+"/ConceptMaps_"+predictedLocationsCSV+".json"
	
	try:
		os.makedirs(outputDirectory)
	except FileExistsError:
		pass
	with open(outputFile,"w") as out:
		toSave = json.dumps(conceptMaps,indent=4)
		out.write(toSave)




if flags.gestaltSearch == True: 
	searchterms = flags.searchterms
	invertedIndexSourceCSV = flags.inputFile

	ii = InvertedIndex(invertedIndexSourceCSV)
	results = ii.search(searchterms)
	print(results)	