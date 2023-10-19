
#Activate the venv
source ../gestalt_env/bin/activate


ECHO = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
ECHO = = = = = = = = EXPERIMENTS FOR QUERY TIMES = = = = = = = = = = =
ECHO = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =


SEARCH_INPUT_FILE="../data/DC/output/ownershipAssignment/DBSCAN_PredictedLocations_FT=0.0.csv"

ECHO DUMPING INVERTED INDEX
#python3 ../code/gestalt.py --dumpInvertedIndex --inputFile $SEARCH_INPUT_FILE 


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

ECHO = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
ECHO = = = = = = = = EXPERIMENTS CARDINALITY INVARIANT TIMES = = = = = = = = = = 
ECHO = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

#Test Pictorial Queries
python3 ../code/experimentVariables.py --inputFile $INVERTED_INDEX --conceptMapFile $CONCEPT_MAPS --locationsFile $UI_LOCATIONS --cardinalityInvariant