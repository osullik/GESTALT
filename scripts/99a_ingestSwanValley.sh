#Activate the venv
source ../gestalt_env/bin/activate

ECHO SETTING UP CLEAN:

echo DELETING OLD DATA
rm -r ../data/SV/input
rm -r ../data/SV/output
#Don't delete photos to save on re-downloading. 

echo MAKING NEW DIRECTORY STRUCTURE
mkdir ../data/SV
mkdir ../data/SV/input/
mkdir ../data/SV/output/
mkdir ../data/SV/output/dataCollection
mkdir ../data/SV/output/ownershipAssignment
mkdir ../data/SV/output/concept_mapping
mkdir ../data/SV/photos

echo IMPORTING INPUT KML
cp -r ../data/input ../data/SV/

#Vars for KNL Ingest
KMLFILE1="../data/SV/input/Swan_Valley.kml"
KML_OUTPUTFILENAME="../data/SV/output/dataCollection/objects_KML" #the python code will append a ".json", don't include it here. 

#Vars for OSM Object Query 
BB_SW_LONG="115.96168231510637"
BB_SW_LAT="-31.90009882641578"
BB_NE_LONG="116.05029961853784"
BB_NE_LAT="-31.77307863942101" 
SEARCHTERM1="allobjects"
OSM_OBJ_OUTPUT_FILE="../data/SV/output/dataCollection/objects"  #note .json extension will be applied by python script

#VARS FOR FLICKR QUERY
echo "QUERYING FLICKR FOR IMAGES"
echo "your FLICKR API Key is:" $flickr_key
echo "your FLICKR Secret key is:" $flickr_secret
ulimit -n 1000
FLICKR_OUTPUTDIRECTORY="../data/SV/photos/"  #note .json extension will be applied by python script
FLICKR_START_PAGE="1"                       #Note: adjsut to recommence when it fails

# VARS FOR FLICKR INGEST:
FLICKR_INPUTFILE="../data/SV/photos/115.96168231510637_-31.90009882641578_116.05029961853784_-31.77307863942101/metadata_objects.json"
FLICKR_OUTPUTFILE="../data/SV/output/dataCollection/objects_flickr"  #note .json extension will be applied by python script

#Vars for OSM LOCATION Query: 

OSM_LOCATION_SEARCH_TERM="all_locations"
OSM_LOCATION_OUTPUTFILE="../data/SV/output/dataCollection/locations"  #note .json extension will be applied by python script

#Vars for DBSCAN:

DBSCAN_INPUT_DIRECTORY="../data/SV/output/datacollection"
DBSCAN_OUTPUT_DIRECTORY="../data/SV/output/ownershipAssignment"
EPSILON=0.00000156961
MIN_CLUSTER_SIZE=3
FUZZY_THRESHOLD=0.0

#Vars for Concept Mapping: 

CM_INPUT_FILE="../data/SV/output/ownershipAssignment/DBSCAN_PredictedLocations_FT=0.0.csv"
CM_OUTPUT_DIRECTORY="../data/SV/output/concept_mapping"
CM_LOCATIONS_FILE="../data/SV/output/dataCollection/locations-31.90009882641578115.96168231510637-31.77307863942101116.05029961853784_alllocations.json"


#Vars for Inverted Index Query Demo

SEARCH_INPUT_FILE="../data/SV/output/ownershipAssignment/DBSCAN_PredictedLocations_FT=0.0.csv"
QUERY_TERMS1="car person cup clock truck"
QUERY_TERMS2="cup bench bird"
QUERY_TERMS3="bench bird"
QUERY_TERMS4="bird"

# Vars for Pictorial Qery Demo

INVERTED_INDEX="../data/SV/output/ownershipAssignment/DBSCAN_PredictedLocations_FT=0.0.csv"
CONCEPT_MAPS="../data/SV/output/concept_mapping/ConceptMaps_DBSCAN_PredictedLocations_FT=0.0.pkl"
UI_LOCATIONS="../data/SV/output/concept_mapping/RelativeLocations_DBSCAN_PredictedLocations_FT=0.0.JSON"

#Jngest Hand-Labelled tags from KML
echo INGESTING KML
python3 ../code/gestalt.py -k -f $KMLFILE1 -o $KML_OUTPUTFILENAME

#Query OSM for Objects
echo "QUERYING OSM FOR OBJECTS"
python3 ../code/gestalt.py -qo -b $BB_SW_LAT $BB_SW_LONG $BB_NE_LAT $BB_NE_LONG -s $SEARCHTERM1 -o $OSM_OBJ_OUTPUT_FILE


# Query Flickr for Objects (NOTE - COMMENT THIS LINE OUT IF YOU DONT WANT TO QUERY THE FLICKR INTERFACE)
ECHO QUERYING FLICKR FOR IMAGES AND RUNNING OBJECT DETECTION
#python3 ../code/gestalt.py -pd -b $BB_SW_LONG $BB_SW_LAT $BB_NE_LONG $BB_NE_LAT -od $FLICKR_OUTPUTDIRECTORY -fpn $FLICKR_START_PAGE

#Process flickr files. 
echo "PROCESSING FLICKR IMAGES FOR OBJECTS"
python3 ../code/gestalt.py -p -if $FLICKR_INPUTFILE -o $FLICKR_OUTPUTFILE

#Query to OSM for locations
echo "QUERYING OSM FOR LOCATIONS"
python3 ../code/gestalt.py -ql -b $BB_SW_LAT $BB_SW_LONG $BB_NE_LAT $BB_NE_LONG -s $OSM_LOCATION_SEARCH_TERM -o $OSM_LOCATION_OUTPUTFILE

#Use DBSCAN to cluster (exact )
echo CLUSTERING WITH DBSCAN EPSILON: $EPSILON MINCLUSTER: $MIN_CLUSTER_SIZE and FUZZY THRESHOLD $FUZZY_THRESHOLD
python3 ../code/gestalt.py --ownershipAssignment dbscan --inputDirectory $DBSCAN_INPUT_DIRECTORY --outputDirectory $DBSCAN_OUTPUT_DIRECTORY --epsilon $EPSILON --numClusters $MIN_CLUSTER_SIZE --fuzzy_threshold $FUZZY_THRESHOLD

#Conduct Concept mapping
echo "CREATING CONCEPT MAPS"
python3 ../code/gestalt.py -ccm --inputFile $CM_INPUT_FILE --outputDirectory $CM_OUTPUT_DIRECTORY --fileSource $CM_LOCATIONS_FILE

#TEST SEARCHING:
echo SEARCHING INVERTED INDEX
python3 ../code/gestalt.py --gestaltSearch --inputFile $SEARCH_INPUT_FILE --searchterms $QUERY_TERMS1
python3 ../code/gestalt.py --gestaltSearch --inputFile $SEARCH_INPUT_FILE --searchterms $QUERY_TERMS2
python3 ../code/gestalt.py --gestaltSearch --inputFile $SEARCH_INPUT_FILE --searchterms $QUERY_TERMS3
python3 ../code/gestalt.py --gestaltSearch --inputFile $SEARCH_INPUT_FILE --searchterms $QUERY_TERMS4

# Launch UI
echo LAUNCHING UI
python3 ../code/UI.py --inputFile $INVERTED_INDEX --conceptMapFile $CONCEPT_MAPS --locationsFile $UI_LOCATIONS


ECHO = = = = = = = = = = = = = = = = = = = = = = = = 
ECHO = = = = = = = = EXPERIMENTS = = = = = = = = = =
ECHO = = = = = = = = = = = = = = = = = = = = = = = =

echo = = = = = = = = = RUNNING EXPERIMENTS FOR HAND LABELLED DATA ONLY = = = = = = = = = 

#Common Variables:
INPUT_DIRECTORY="../data/SV/output/experiments/datacollection"
OUTPUT_DIRECTORY="../data/SV/output/experiments/ownershipAssignment/wineries_only"
#Epsilon here roughly 50m
EPSILON=0.00000784806
MIN_CLUSTER_SIZE=3

# Clean out Existing data:
echo DELETING OLD DATA
rm -r ../data/SV/output/experiments

mkdir ../data/SV/output/experiments
mkdir ../data/SV/output/experiments/dataCollection
mkdir ../data/SV/output/experiments/ownershipAssignment
mkdir ../data/SV/output/experiments/ownershipAssignment/wineries_only

# Prepare 
#Import KML for Experiment
EXP_KMLFILE1="../data/SV/input/Swan_Valley.kml"
EXP_KML_OUTPUTFILENAME="../data/SV/output/experiments/dataCollection/objects_KML" #the python code will append a ".json", don't include it here. 
python3 ../code/gestalt.py -k -f $EXP_KMLFILE1 -o $EXP_KML_OUTPUTFILENAME

#Get the locations
EXP_SEARCHTERM1="winery"
EXP_SEARCHTERM2="brewery"
EXP_OUTPUTFILE="../data/SV/output/experiments/dataCollection/locations_"  #note .json extension will be applied by python script
python3 ../code/gestalt.py -ql -b $BB_SW_LAT $BB_SW_LONG $BB_NE_LAT $BB_NE_LONG -s $EXP_SEARCHTERM1 $EXP_SEARCHTERM2 -o $EXP_OUTPUTFILE

#Variables for Iteration1
INPUT_FILE="../data/SV/output/experiments/ownershipAssignment/wineries_only/DBSCAN_PredictedLocations_FT=0.0.csv"
FUZZY_THRESHOLD=0.0
python3 ../code/gestalt.py --ownershipAssignment dbscan --inputDirectory $INPUT_DIRECTORY --outputDirectory $OUTPUT_DIRECTORY --epsilon $EPSILON --numClusters $MIN_CLUSTER_SIZE --fuzzy_threshold $FUZZY_THRESHOLD
ECHO RUNNING EXPERIMENT WITH DBSCAN EPSILON: $EPSILON MINCLUSTER: $MIN_CLUSTER_SIZE and FUZZY THRESHOLD $FUZZY_THRESHOLD
python3 ../code/ClusteringMetrics.py -c $INPUT_FILE

#Variables for Iteration2
INPUT_FILE="../data/SV/output/experiments/ownershipAssignment/wineries_only/DBSCAN_PredictedLocations_FT=0.2.csv"
FUZZY_THRESHOLD=0.2
python3 ../code/gestalt.py --ownershipAssignment dbscan --inputDirectory $INPUT_DIRECTORY --outputDirectory $OUTPUT_DIRECTORY --epsilon $EPSILON --numClusters $MIN_CLUSTER_SIZE --fuzzy_threshold $FUZZY_THRESHOLD
ECHO RUNNING EXPERIMENT WITH DBSCAN EPSILON: $EPSILON MINCLUSTER: $MIN_CLUSTER_SIZE and FUZZY THRESHOLD $FUZZY_THRESHOLD
python3 ../code/ClusteringMetrics.py -c $INPUT_FILE

#Variables for Iteration3
INPUT_FILE="../data/SV/output/experiments/ownershipAssignment/wineries_only/DBSCAN_PredictedLocations_FT=0.4.csv"
FUZZY_THRESHOLD=0.4
python3 ../code/gestalt.py --ownershipAssignment dbscan --inputDirectory $INPUT_DIRECTORY --outputDirectory $OUTPUT_DIRECTORY --epsilon $EPSILON --numClusters $MIN_CLUSTER_SIZE --fuzzy_threshold $FUZZY_THRESHOLD
ECHO RUNNING EXPERIMENT WITH DBSCAN EPSILON: $EPSILON MINCLUSTER: $MIN_CLUSTER_SIZE and FUZZY THRESHOLD $FUZZY_THRESHOLD
python3 ../code/ClusteringMetrics.py -c $INPUT_FILE

#Variables for Iteration4
INPUT_FILE="../data/SV/output/experiments/ownershipAssignment/wineries_only/DBSCAN_PredictedLocations_FT=0.6.csv"
FUZZY_THRESHOLD=0.6
python3 ../code/gestalt.py --ownershipAssignment dbscan --inputDirectory $INPUT_DIRECTORY --outputDirectory $OUTPUT_DIRECTORY --epsilon $EPSILON --numClusters $MIN_CLUSTER_SIZE --fuzzy_threshold $FUZZY_THRESHOLD
ECHO RUNNING EXPERIMENT WITH DBSCAN EPSILON: $EPSILON MINCLUSTER: $MIN_CLUSTER_SIZE and FUZZY THRESHOLD $FUZZY_THRESHOLD
python3 ../code/ClusteringMetrics.py -c $INPUT_FILE

#Variables for Iteration5
INPUT_FILE="../data/SV/output/experiments/ownershipAssignment/wineries_only/DBSCAN_PredictedLocations_FT=0.8.csv"
FUZZY_THRESHOLD=0.8
python3 ../code/gestalt.py --ownershipAssignment dbscan --inputDirectory $INPUT_DIRECTORY --outputDirectory $OUTPUT_DIRECTORY --epsilon $EPSILON --numClusters $MIN_CLUSTER_SIZE --fuzzy_threshold $FUZZY_THRESHOLD
ECHO RUNNING EXPERIMENT WITH DBSCAN EPSILON: $EPSILON MINCLUSTER: $MIN_CLUSTER_SIZE and FUZZY THRESHOLD $FUZZY_THRESHOLD
python3 ../code/ClusteringMetrics.py -c $INPUT_FILE

#Variables for Iteration6
INPUT_FILE="../data/SV/output/experiments/ownershipAssignment/wineries_only/DBSCAN_PredictedLocations_FT=1.0.csv"
FUZZY_THRESHOLD=1.0
python3 ../code/gestalt.py --ownershipAssignment dbscan --inputDirectory $INPUT_DIRECTORY --outputDirectory $OUTPUT_DIRECTORY --epsilon $EPSILON --numClusters $MIN_CLUSTER_SIZE --fuzzy_threshold $FUZZY_THRESHOLD
ECHO RUNNING EXPERIMENT WITH DBSCAN EPSILON: $EPSILON MINCLUSTER: $MIN_CLUSTER_SIZE and FUZZY THRESHOLD $FUZZY_THRESHOLD
python3 ../code/ClusteringMetrics.py -c $INPUT_FILE


echo = = = = = = = = = RUNNING EXPERIMENTS FOR ALL DATA = = = = = = = = = 

OUTPUT_DIRECTORY="../data/SV/output/experiments/ownershipAssignment/combined"

rm -r "../data/SV/output/experiments/ownershipAssignment/combined"
mkdir "../data/SV/output/experiments/ownershipAssignment/combined"

#Import KML for Experiment
EXP_KMLFILE1="../data/SV/input/Swan_Valley.kml"
EXP_KML_OUTPUTFILENAME="../data/SV/output/experiments/dataCollection/objects_KML" #the python code will append a ".json", don't include it here. 
python3 ../code/gestalt.py -k -f $EXP_KMLFILE1 -o $EXP_KML_OUTPUTFILENAME

#Get all objects for Experiment
EXP_SEARCHTERM1="allobjects"
EXP_OUTPUTFILE="../data/SV/output/experiments/dataCollection/objects_"  #note .json extension will be applied by python script
python3 ../code/gestalt.py -qo -b $BB_SW_LAT $BB_SW_LONG $BB_NE_LAT $BB_NE_LONG -s $EXP_SEARCHTERM1 -o $EXP_OUTPUTFILE

#Ingest all processed FLICKR objecte
EXP_INPUTFILE="../data/SV/photos/115.96168231510637_-31.90009882641578_116.05029961853784_-31.77307863942101/metadata_objects.json"
EXP_OUTPUTFILE="../data/SV/output/experiments/dataCollection/objects_flickr"  #note .json extension will be applied by python script
python3 ../code/gestalt.py -p -if $EXP_INPUTFILE -o $EXP_OUTPUTFILE

#Ingest All Locations for Querying
EXP_SEARCHTERM1="all_locations"
EXP_OUTPUTFILE="../data/SV/output/experiments/dataCollection/locations_"  #note .json extension will be applied by python script
python3 ../code/gestalt.py -ql -b $BB_SW_LAT $BB_SW_LONG $BB_NE_LAT $BB_NE_LONG -s $EXP_SEARCHTERM1 -o $EXP_OUTPUTFILE

#Variables for Iteration1
INPUT_FILE="../data/SV/output/experiments/ownershipAssignment/combined/DBSCAN_PredictedLocations_FT=0.0.csv"
FUZZY_THRESHOLD=0.0
python3 ../code/gestalt.py --ownershipAssignment dbscan --inputDirectory $INPUT_DIRECTORY --outputDirectory $OUTPUT_DIRECTORY --epsilon $EPSILON --numClusters $MIN_CLUSTER_SIZE --fuzzy_threshold $FUZZY_THRESHOLD
ECHO RUNNING EXPERIMENT WITH DBSCAN EPSILON: $EPSILON MINCLUSTER: $MIN_CLUSTER_SIZE and FUZZY THRESHOLD $FUZZY_THRESHOLD
python3 ../code/ClusteringMetrics.py -c $INPUT_FILE

#Variables for Iteration2
INPUT_FILE="../data/SV/output/experiments/ownershipAssignment/combined/DBSCAN_PredictedLocations_FT=0.2.csv"
FUZZY_THRESHOLD=0.2
python3 ../code/gestalt.py --ownershipAssignment dbscan --inputDirectory $INPUT_DIRECTORY --outputDirectory $OUTPUT_DIRECTORY --epsilon $EPSILON --numClusters $MIN_CLUSTER_SIZE --fuzzy_threshold $FUZZY_THRESHOLD
ECHO RUNNING EXPERIMENT WITH DBSCAN EPSILON: $EPSILON MINCLUSTER: $MIN_CLUSTER_SIZE and FUZZY THRESHOLD $FUZZY_THRESHOLD
python3 ../code/ClusteringMetrics.py -c $INPUT_FILE

#Variables for Iteration3
INPUT_FILE="../data/SV/output/experiments/ownershipAssignment/combined/DBSCAN_PredictedLocations_FT=0.4.csv"
FUZZY_THRESHOLD=0.4
python3 ../code/gestalt.py --ownershipAssignment dbscan --inputDirectory $INPUT_DIRECTORY --outputDirectory $OUTPUT_DIRECTORY --epsilon $EPSILON --numClusters $MIN_CLUSTER_SIZE --fuzzy_threshold $FUZZY_THRESHOLD
ECHO RUNNING EXPERIMENT WITH DBSCAN EPSILON: $EPSILON MINCLUSTER: $MIN_CLUSTER_SIZE and FUZZY THRESHOLD $FUZZY_THRESHOLD
python3 ../code/ClusteringMetrics.py -c $INPUT_FILE

#Variables for Iteration4
INPUT_FILE="../data/SV/output/experiments/ownershipAssignment/combined/DBSCAN_PredictedLocations_FT=0.6.csv"
FUZZY_THRESHOLD=0.6
python3 ../code/gestalt.py --ownershipAssignment dbscan --inputDirectory $INPUT_DIRECTORY --outputDirectory $OUTPUT_DIRECTORY --epsilon $EPSILON --numClusters $MIN_CLUSTER_SIZE --fuzzy_threshold $FUZZY_THRESHOLD
ECHO RUNNING EXPERIMENT WITH DBSCAN EPSILON: $EPSILON MINCLUSTER: $MIN_CLUSTER_SIZE and FUZZY THRESHOLD $FUZZY_THRESHOLD
python3 ../code/ClusteringMetrics.py -c $INPUT_FILE

#Variables for Iteration5
INPUT_FILE="../data/SV/output/experiments/ownershipAssignment/combined/DBSCAN_PredictedLocations_FT=0.8.csv"
FUZZY_THRESHOLD=0.8
python3 ../code/gestalt.py --ownershipAssignment dbscan --inputDirectory $INPUT_DIRECTORY --outputDirectory $OUTPUT_DIRECTORY --epsilon $EPSILON --numClusters $MIN_CLUSTER_SIZE --fuzzy_threshold $FUZZY_THRESHOLD
ECHO RUNNING EXPERIMENT WITH DBSCAN EPSILON: $EPSILON MINCLUSTER: $MIN_CLUSTER_SIZE and FUZZY THRESHOLD $FUZZY_THRESHOLD
python3 ../code/ClusteringMetrics.py -c $INPUT_FILE

#Variables for Iteration6
INPUT_FILE="../data/SV/output/experiments/ownershipAssignment/combined/DBSCAN_PredictedLocations_FT=1.0.csv"
FUZZY_THRESHOLD=1.0
python3 ../code/gestalt.py --ownershipAssignment dbscan --inputDirectory $INPUT_DIRECTORY --outputDirectory $OUTPUT_DIRECTORY --epsilon $EPSILON --numClusters $MIN_CLUSTER_SIZE --fuzzy_threshold $FUZZY_THRESHOLD
ECHO RUNNING EXPERIMENT WITH DBSCAN EPSILON: $EPSILON MINCLUSTER: $MIN_CLUSTER_SIZE and FUZZY THRESHOLD $FUZZY_THRESHOLD
python3 ../code/ClusteringMetrics.py -c $INPUT_FILE