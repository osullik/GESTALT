
#System Imports
import argparse, json, sys, os

#Library Imports

#User Imports

from dataCollection import TerrainExtractor, osmQueryEngine
from ownershipAssignment import OwnershipAssigner



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
							default=None,
							required=False)

	argparser.add_argument("-lf", "--locationsFile",
							help="The path to a file containing the locations to cluster around, a JSON file", 
							type=str, 
							required=False)

	argparser.add_argument("-of", "--objectsFile", 
							help="The path to a file containing the objects", 
							required=False)	
	
	argparser.add_argument("-n", "--numClusters", 
							help="number of clusters to use for KMeans",
							type=int, 
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
		object_file = flags.objectsFile
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
		objectsDict = {}
		locationsDict = {}
		prefix = "../data/output/dataCollection"
		for file in os.listdir(prefix):
			print(file)
			if file.startswith("objects"):
				with open(prefix+"/"+file, "r") as inObjs:
					objects = json.load(inObjs)
				objectsDict.update(objects)
			if file.startswith("locations"):
				with open(prefix+"/"+file, "r") as inLocs:
					locations = json.load(inLocs)
				locationsDict.update(locations)

		#print(objectsDict)
		#print(locationsDict)
		
		outputFile = flags.output
		numClusters = flags.numClusters
		
		ownerAssigner = OwnershipAssigner(locations, objects)
		#flatLocations = ownerAssigner.flatten_locations(locations)
		#flatObjects= ownerAssigner.flatten_objects(objects)
		#flatOSMObjects = ownerAssigner.flatten_objects_from_osm_dump(objects)
		df_locations, df_objects = ownerAssigner.convertToDataFrame(locationsDict, objectsDict)

		ownerAssigner._df_locations.to_csv("../data/output/ownershipAssignment/locations.csv", index=False)
		ownerAssigner._df_objects.to_csv("../data/output/ownershipAssignment/objects.csv", index=False)

		ownerAssigner.kMeans_membership(df_objects, len(locationsDict.keys()))
		#correct = ownerAssigner._df_obj["kmeans_correct"]
		#print(correct.value_counts())
		clusters = ownerAssigner._df_objects["cluster"]
		print(clusters.value_counts())

		ownerAssigner._df_objects.to_csv("../data/output/ownershipAssignment/PredictedLocations.csv", index=False)

		

'''
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


'''
