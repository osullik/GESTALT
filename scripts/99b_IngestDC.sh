
#Activate the venv
source ../gestalt_env/bin/activate

#Vars for OSM Object Query 
BB_SW_LONG="-77.120248"
BB_SW_LAT="38.791086"
BB_NE_LONG="-76.911012" 
BB_NE_LAT="38.995732"
SEARCHTERM1="allobjects"
OSM_OBJ_OUTPUT_FILE="../data/DC/output/dataCollection/objects"  #note .json extension will be applied by python script

#Vars for FLICKR Query

FLICKR_OUTPUTDIRECTORY="../data/DC/photos/"  #note .json extension will be applied by python script
FLICKR_START_PAGE="1"                       #Note: adjsut to recommence when it fails

#Vars for FLICKR Ingestion

FLICKR_INPUTFILE="../data/DC/photos/['-77.120248', '38.791086', '-76.911012', '38.995732']/metadata_objects.json"
FLICKR_OUTPUTFILE="../data/DC/output/dataCollection/objects_flickr"  #note .json extension will be applied by python script

#Vars for OSM LOCATION Query: 

OSM_LOCATION_SEARCH_TERM="all_locations"
OSM_LOCATION_OUTPUTFILE="../data/DC/output/dataCollection/locations"  #note .json extension will be applied by python script

#Vars for DBSCAN:

DBSCAN_INPUT_DIRECTORY="../data/DC/output/datacollection"
DBSCAN_OUTPUT_DIRECTORY="../data/DC/output/ownershipAssignment"
EPSILON=0.00000156961
MIN_CLUSTER_SIZE=3
FUZZY_THRESHOLD=0.0

#Vars for Concept Mapping: 

CM_INPUT_FILE="../data/DC/output/ownershipAssignment/DBSCAN_PredictedLocations_FT=0.0.csv"
CM_OUTPUT_DIRECTORY="../data/DC/output/concept_mapping"
CM_LOCATIONS_FILE="../data/DC/output/dataCollection/locations38.791086-77.12024838.995732-76.911012_alllocations.json"
#Query OSM for Objects
python3 ../code/gestalt.py -qo -b $BB_SW_LAT $BB_SW_LONG $BB_NE_LAT $BB_NE_LONG -s $SEARCHTERM1 -o $OSM_OBJ_OUTPUT_FILE


# Query Flickr for Objects
#echo "your FLICKR API Key is:" $flickr_key
#echo "your FLICKR Secret key is:" $flickr_secret
#ulimit -n 5000
#python3 ../code/gestalt.py -pd -b $BB_SW_LONG $BB_SW_LAT $BB_NE_LONG $BB_NE_LAT -od $FLICKR_OUTPUTDIRECTORY -fpn $FLICKR_START_PAGE

#Process the FLICKR objects
#python3 ../code/gestalt.py -p -if $FLICKR_INPUTFILE -o $FLICKR_OUTPUTFILE

#Query OSM For Locations
#python3 ../code/gestalt.py -ql -b $BB_SW_LAT $BB_SW_LONG $BB_NE_LAT $BB_NE_LONG -s $OSM_LOCATION_SEARCH_TERM -o $OSM_LOCATION_OUTPUTFILE

#Use DBSCAN to cluster (exact )
#python3 ../code/gestalt.py --ownershipAssignment dbscan --inputDirectory $DBSCAN_INPUT_DIRECTORY --outputDirectory $DBSCAN_OUTPUT_DIRECTORY --epsilon $EPSILON --numClusters $MIN_CLUSTER_SIZE --fuzzy_threshold $FUZZY_THRESHOLD

#Conduct Concept mapping

python3 ../code/gestalt.py -ccm --inputFile $CM_INPUT_FILE --outputDirectory $CM_OUTPUT_DIRECTORY --fileSource $CM_LOCATIONS_FILE