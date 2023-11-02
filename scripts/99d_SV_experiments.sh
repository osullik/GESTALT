
#Activate the venv
source ../gestalt_env/Scripts/activate


ECHO = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
ECHO = = = = = = = = EXPERIMENTS FOR QUERY TIMES = = = = = = = = = = =
ECHO = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =


SEARCH_INPUT_FILE="../data/SV/output/ownershipAssignment/DBSCAN_PredictedLocations_FT=0.0.csv"

ECHO DUMPING INVERTED INDEX
#python3 ../code/gestalt.py --dumpInvertedIndex --inputFile $SEARCH_INPUT_FILE 





ECHO = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
ECHO = = = = = = = = EXPERIMENTS FOR PICTORIAL QUERY PREC/RECALL = = = = = = = = = = =
ECHO = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

INVERTED_INDEX="../data/SV/output/ownershipAssignment/DBSCAN_PredictedLocations_FT=0.0.csv"
CONCEPT_MAPS="../data/SV/output/concept_mapping/ConceptMaps_DBSCAN_PredictedLocations_FT=0.0.pkl"
UI_LOCATIONS="../data/SV/output/concept_mapping/RelativeLocations_DBSCAN_PredictedLocations_FT=0.0.JSON"

ECHO = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
ECHO = = = = = = = = EXPERIMENTS LOCATION CENTRIC = = = = = = = = = = 
ECHO = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

#Test Pictorial Queries
python ../code/experimentVariablesGT.py --inputFile $INVERTED_INDEX --conceptMapFile $CONCEPT_MAPS --locationsFile $UI_LOCATIONS --locationCentric

ECHO = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
ECHO = = = = = = = = EXPERIMENTS OBJECT CENTRIC = = = = = = = = = = 
ECHO = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

#Test Pictorial Queries
python ../code/experimentVariablesGT.py --inputFile $INVERTED_INDEX --conceptMapFile $CONCEPT_MAPS --locationsFile $UI_LOCATIONS --objectCentric

ECHO = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
ECHO = = = = = = = = EXPERIMENTS CARDINALITY INVARIANT = = = = = = = = = = 
ECHO = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

#Test Pictorial Queries
python ../code/experimentVariablesGT.py --inputFile $INVERTED_INDEX --conceptMapFile $CONCEPT_MAPS --locationsFile $UI_LOCATIONS --objectCentric --cardinalityInvariant