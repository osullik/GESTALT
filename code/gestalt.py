
#System Imports
import argparse, json, sys

#Library Imports

#User Imports

from dataCollection import TerrainExtractor, osmQueryEngine
from ownershipAssignment import OwnershipAssigner
from queryFlickr import photoDownloader



if __name__ == "__main__":

	argparser = argparse.ArgumentParser()									# initialize the argParser

	argparser.add_argument(	"-q", "--queryOsmMode", 							
							help="engage mode to issue a query to OpenStreetMaps",
							action="store_true",
							default=False,
							required=False)	
		
	argparser.add_argument( "-b", "--boundingbox", 
							help="specifies the bounding box to be passed to OSM", 
							nargs='+',
							default=None,
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
							help="KML file(s) to ingest)", 
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


	if flags.queryOsmMode== True: 																		# Check to see if GESTALT should execute in OSM Query mode. 
		bbox = flags.boundingbox
		outputfile = flags.output
		searchterms = flags.searchterms
		oqe = osmQueryEngine()
		
		if searchterms[0] == "allobjects":
			osmDict = oqe.queryOSM(bbox, searchterms[0])
			outputfileName = (outputfile+"_"+"".join(bbox)+"_allobjects.json")
		else:
			osmDict = oqe.queryOSM(bbox, searchterms[0]) 													# Create the dictionary off the first search term 
			for i in range(1, len(searchterms), 1): 														# Loop through other search terms and merge each set of results into one big dict
				newDict = oqe.queryOSM(bbox, searchterms[i])
				osmDict.update(newDict)
			outputfileName = (outputfile+"".join(searchterms)+".json") 												#Define the filename to output to
		
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
			objectLocations = tex.Ingest_kml_file(file) 												#get the dictionary from ingesting KML file
			outputfileName = outputfile+"_"+shortFileName+".json" 										#set the output name to be distinct for the file
			with open(outputfileName,'w') as outfile: 													#output to JSON
				json.dump(objectLocations, outfile, indent=4)
			print("Successfully outputted data to \"{outputLoc}\"".format(outputLoc=outputfileName)) 	#user feedback
		exit()

	''if flags.ownershipAssignment.lower() == "kmeans":
		with open(flags.locationsFile, "r") as inLocs:
				locations = json.load(inLocs)
		with open(flags.objectsFile, "r") as inObjs:
			objects = json.load(inObjs)
		outputFile = flags.output
		numClusters = flags.numClusters
		
		ownerAssigner = OwnershipAssigner(locations, objects)
		flatLocations = ownerAssigner.flatten_locations(locations)
		#flatObjects= ownerAssigner.flatten_objects(objects)
		flatOSMObjects = ownerAssigner.flatten_objects_from_osm_dump(objects)
		df_locations, df_objects = ownerAssigner.convertToDataFrame(flatLocations, flatOSMObjects)
		ownerAssigner.kMeans_membership(flatOSMObjects, numClusters)
		correct = ownerAssigner._df_obj["kmeans_correct"]
		print(correct.value_counts())
		clusters = ownerAssigner._df_obj["cluster"]
		print(clusters.value_counts())''

		

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
