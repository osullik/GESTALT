
#Activate the venv
source ../gestalt_env/bin/activate

#echo SETTING UP CLEAN:

#echo DELETING OLD DATA
#rm -r ../data/DC/output
#Don't delete photos to save on re-downloading. 

#echo MAKING NEW DIRECTORY STRUCTURE
#mkdir ../data/DC
#mkdir ../data/DC/input/
#mkdir ../data/DC/output/
#mkdir ../data/DC/output/dataCollection/
#mkdir ../data/DC/output/ownershipAssignment/
#mkdir ../data/DC/output/concept_mapping/
#mkdir ../data/DC/photos/

#Vars for OSM Object Query 
BB_SW_LONG="-77.120248"
BB_SW_LAT="38.791086"
BB_NE_LONG="-76.911012" 
BB_NE_LAT="38.995732"
SEARCHTERM1="allobjects"
OSM_OBJ_OUTPUT_FILE="../data/DC/output/dataCollection/objects"  #note .json extension will be applied by python script

#Vars for FLICKR Query
echo QUERYING FLICKR FOR IMAGES
echo your FLICKR API Key is: $flickr_key
echo your FLICKR Secret key is: $flickr_secret
ulimit -n 1000
FLICKR_OUTPUTDIRECTORY="../data/DC/photos/"  #note .json extension will be applied by python script
FLICKR_START_PAGE="1"                       #Note: adjsut to recommence when it fails

#Vars for FLICKR Ingestion

FLICKR_INPUTFILE="../data/DC/photos/-77.120248_38.791086_-76.911012_38.995732/metadata_objects.json"
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


#Vars for Inverted Index Query Demo

SEARCH_INPUT_FILE="../data/DC/output/ownershipAssignment/DBSCAN_PredictedLocations_FT=0.0.csv"
QUERY_TERMS1="apple picnic_table"
QUERY_TERMS2="cup bench bird"
QUERY_TERMS3="bench bird"
QUERY_TERMS4="bird"

# Vars for Pictorial Qery Demo

INVERTED_INDEX="../data/DC/output/ownershipAssignment/DBSCAN_PredictedLocations_FT=0.0.csv"
CONCEPT_MAPS="../data/DC/output/concept_mapping/ConceptMaps_DBSCAN_PredictedLocations_FT=0.0.pkl"
UI_LOCATIONS="../data/DC/output/concept_mapping/RelativeLocations_DBSCAN_PredictedLocations_FT=0.0.JSON"

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


ECHO = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
ECHO = = = = = = = = EXPERIMENTS FOR QUERY TIMES = = = = = = = = = = =
ECHO = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =


SEARCH_INPUT_FILE="../data/DC/output/ownershipAssignment/DBSCAN_PredictedLocations_FT=0.0.csv"

ECHO DUMPING INVERTED INDEX
python3 ../code/gestalt.py --dumpInvertedIndex --inputFile $SEARCH_INPUT_FILE 


QUERY_TERMS1="crossing"
QUERY_TERMS2="traffic_signals"
QUERY_TERMS3="stop"
QUERY_TERMS4="tree"
QUERY_TERMS5="kerb"

QUERY_TERMS6="crossing traffic_signals"
QUERY_TERMS7="crossing stop"
QUERY_TERMS8="crossing tree"
QUERY_TERMS9="crossing kerb"

QUERY_TERMS10="crossing traffic_signals stop"
QUERY_TERMS11="crossing traffic_signals tree"
QUERY_TERMS12="crossing traffic_signals kerb"

QUERY_TERMS13="crossing traffic_signals stop tree"
QUERY_TERMS14="crossing traffic_signals stop kerb"

QUERY_TERMS15="crossing traffic_signals stop tree kerb"

QUERY_TERMS16="crossing traffic_signals stop tree kerb street_lamp person bus_stop gate bollard"

python3 ../code/gestalt.py --gestaltSearch --inputFile $SEARCH_INPUT_FILE --searchterms $QUERY_TERMS1
python3 ../code/gestalt.py --gestaltSearch --inputFile $SEARCH_INPUT_FILE --searchterms $QUERY_TERMS2
python3 ../code/gestalt.py --gestaltSearch --inputFile $SEARCH_INPUT_FILE --searchterms $QUERY_TERMS3
python3 ../code/gestalt.py --gestaltSearch --inputFile $SEARCH_INPUT_FILE --searchterms $QUERY_TERMS4
python3 ../code/gestalt.py --gestaltSearch --inputFile $SEARCH_INPUT_FILE --searchterms $QUERY_TERMS5
python3 ../code/gestalt.py --gestaltSearch --inputFile $SEARCH_INPUT_FILE --searchterms $QUERY_TERMS6
python3 ../code/gestalt.py --gestaltSearch --inputFile $SEARCH_INPUT_FILE --searchterms $QUERY_TERMS7
python3 ../code/gestalt.py --gestaltSearch --inputFile $SEARCH_INPUT_FILE --searchterms $QUERY_TERMS8
python3 ../code/gestalt.py --gestaltSearch --inputFile $SEARCH_INPUT_FILE --searchterms $QUERY_TERMS9
python3 ../code/gestalt.py --gestaltSearch --inputFile $SEARCH_INPUT_FILE --searchterms $QUERY_TERMS10
python3 ../code/gestalt.py --gestaltSearch --inputFile $SEARCH_INPUT_FILE --searchterms $QUERY_TERMS11
python3 ../code/gestalt.py --gestaltSearch --inputFile $SEARCH_INPUT_FILE --searchterms $QUERY_TERMS12
python3 ../code/gestalt.py --gestaltSearch --inputFile $SEARCH_INPUT_FILE --searchterms $QUERY_TERMS13
python3 ../code/gestalt.py --gestaltSearch --inputFile $SEARCH_INPUT_FILE --searchterms $QUERY_TERMS14
python3 ../code/gestalt.py --gestaltSearch --inputFile $SEARCH_INPUT_FILE --searchterms $QUERY_TERMS15
python3 ../code/gestalt.py --gestaltSearch --inputFile $SEARCH_INPUT_FILE --searchterms $QUERY_TERMS16


ECHO = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
ECHO = = = = = = = = EXPERIMENTS FOR PICTORIAL QUERY TIMES = = = = = = = = = = =
ECHO = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

INVERTED_INDEX="../data/DC/output/ownershipAssignment/DBSCAN_PredictedLocations_FT=0.0.csv"
CONCEPT_MAPS="../data/DC/output/concept_mapping/ConceptMaps_DBSCAN_PredictedLocations_FT=0.0.pkl"
UI_LOCATIONS="../data/DC/output/concept_mapping/RelativeLocations_DBSCAN_PredictedLocations_FT=0.0.JSON"
#Test Pictorial Queries
python3 ../code/experimentVariables.py --inputFile $INVERTED_INDEX --conceptMapFile $CONCEPT_MAPS --locationsFile $UI_LOCATIONS

