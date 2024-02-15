#Activate the venv
source ../gestalt_env/bin/activate

echo SETTING UP CLEAN:

echo DELETING OLD DATA
rm -r ../data/HAM/output
#Don't delete photos to save on re-downloading. 

echo MAKING NEW DIRECTORY STRUCTURE
mkdir ../data/HAM
mkdir ../data/HAM/input/
mkdir ../data/HAM/output/
mkdir ../data/HAM/output/dataCollection/
mkdir ../data/HAM/output/ownershipAssignment/
mkdir ../data/HAM/output/concept_mapping/
mkdir ../data/HAM/photos/

#Vars for OSM Object Query 
BB_SW_LONG="9.713691"
BB_SW_LAT="53.388071"
BB_NE_LONG="10.34807" 
BB_NE_LAT="53.744626"
SEARCHTERM1="allobjects"
OSM_OBJ_OUTPUT_FILE="../data/HAM/output/dataCollection/objects"  #note .json extension will be applied by python script

#Vars for FLICKR Query
echo QUERYING FLICKR FOR IMAGES
echo your FLICKR API Key is: $flickr_key
echo your FLICKR Secret key is: $flickr_secret
ulimit -n 1000
FLICKR_OUTPUTDIRECTORY="../data/HAM/photos/"  #note .json extension will be applied by python script
FLICKR_START_PAGE="1"                       #Note: adjsut to recommence when it fails

#Vars for FLICKR Ingestion

FLICKR_INPUTFILE="../data/HAM/photos/9.713691_53.388071_10.34807_53.744626/metadata_objects.json"
FLICKR_OUTPUTFILE="../data/HAM/output/dataCollection/objects_flickr"  #note .json extension will be applied by python script

#Vars for OSM LOCATION Query: 

OSM_LOCATION_SEARCH_TERM="all_locations"
OSM_LOCATION_OUTPUTFILE="../data/HAM/output/dataCollection/locations"  #note .json extension will be applied by python script

#Vars for DBSCAN:

DBSCAN_INPUT_DIRECTORY="../data/HAM/output/datacollection"
DBSCAN_OUTPUT_DIRECTORY="../data/HAM/output/ownershipAssignment"
EPSILON=0.00000156961
MIN_CLUSTER_SIZE=3
FUZZY_THRESHOLD=0.0

#Vars for Concept Mapping: 

CM_INPUT_FILE="../data/HAM/output/ownershipAssignment/DBSCAN_PredictedLocations_FT=0.0.csv"
CM_OUTPUT_DIRECTORY="../data/HAM/output/concept_mapping"
CM_LOCATIONS_FILE="../data/HAM/output/dataCollection/locations9.713691_53.388071_10.34807_53.744626_alllocations.json"


#Vars for Inverted Index Query Demo

SEARCH_INPUT_FILE="../data/HAM/output/ownershipAssignment/DBSCAN_PredictedLocations_FT=0.0.csv"
QUERY_TERMS1="apple picnic_table"
QUERY_TERMS2="cup bench bird"
QUERY_TERMS3="bench bird"
QUERY_TERMS4="bird"

# Vars for Pictorial Qery Demo

INVERTED_INDEX="../data/HAM/output/ownershipAssignment/DBSCAN_PredictedLocations_FT=0.0.csv"
CONCEPT_MAPS="../data/HAM/output/concept_mapping/ConceptMaps_DBSCAN_PredictedLocations_FT=0.0.pkl"
UI_LOCATIONS="../data/HAM/output/concept_mapping/RelativeLocations_DBSCAN_PredictedLocations_FT=0.0.JSON"

#Query OSM for Objects
echo QUERYING OSM FOR OBJECTS
python3 ../code/gestalt.py -qo -b $BB_SW_LAT $BB_SW_LONG $BB_NE_LAT $BB_NE_LONG -s $SEARCHTERM1 -o $OSM_OBJ_OUTPUT_FILE

# Query Flickr for Objects
echo QUERYING FLICKR FOR IMAGES
echo "your FLICKR API Key is:" $flickr_key
echo "your FLICKR Secret key is:" $flickr_secret
ulimit -n 5000
python3 ../code/gestalt.py -pd -b $BB_SW_LONG $BB_SW_LAT $BB_NE_LONG $BB_NE_LAT -od $FLICKR_OUTPUTDIRECTORY -fpn $FLICKR_START_PAGE

#Process the FLICKR objects
echo PROCESSING FLICKR IMAGES FOR OBJECTS
python3 ../code/gestalt.py -p -if $FLICKR_INPUTFILE -o $FLICKR_OUTPUTFILE

#Query OSM For Locations
echo QUERYING OSM FOR LOCATIONS
python3 ../code/gestalt.py -ql -b $BB_SW_LAT $BB_SW_LONG $BB_NE_LAT $BB_NE_LONG -s $OSM_LOCATION_SEARCH_TERM -o $OSM_LOCATION_OUTPUTFILE

#Use DBSCAN to cluster (exact )
echo CLUSTERING WITH DBSCAN EPSILON: $EPSILON MINCLUSTER: $MIN_CLUSTER_SIZE and FUZZY THRESHOLD $FUZZY_THRESHOLD
python3 ../code/gestalt.py --ownershipAssignment dbscan --inputDirectory $DBSCAN_INPUT_DIRECTORY --outputDirectory $DBSCAN_OUTPUT_DIRECTORY --epsilon $EPSILON --numClusters $MIN_CLUSTER_SIZE --fuzzy_threshold $FUZZY_THRESHOLD

#Conduct Concept mapping
echo CREATING CONCEPT MAPS
python3 ../code/gestalt.py -ccm --inputFile $CM_INPUT_FILE --outputDirectory $CM_OUTPUT_DIRECTORY --fileSource $CM_LOCATIONS_FILE


#TEST SEARCHING:
#echo SEARCHING INVERTED INDEX
python3 ../code/gestalt.py --gestaltSearch --inputFile $SEARCH_INPUT_FILE --searchterms $QUERY_TERMS1
python3 ../code/gestalt.py --gestaltSearch --inputFile $SEARCH_INPUT_FILE --searchterms $QUERY_TERMS2
python3 ../code/gestalt.py --gestaltSearch --inputFile $SEARCH_INPUT_FILE --searchterms $QUERY_TERMS3
python3 ../code/gestalt.py --gestaltSearch --inputFile $SEARCH_INPUT_FILE --searchterms $QUERY_TERMS4

# Launch UI
echo LAUNCHING UI
#python3 ../code/UI.py --inputFile $INVERTED_INDEX --conceptMapFile $CONCEPT_MAPS --locationsFile $UI_LOCATIONS


