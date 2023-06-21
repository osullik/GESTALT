#createConceptMaps.sh

#Activate the venv
source ../gestalt_env/bin/activate

#Common Variables:
INPUT_DIRECTORY="../data/output/datacollection"
OUTPUT_DIRECTORY="../data/output/ownershipAssignment"
INPUT_FILE="../data/output/ownershipAssignment/DBSCAN_PredictedLocations.csv"

#Variables for Iteration1
EPSILON=0.000015696123058
MIN_CLUSTER_SIZE=3
FUZZY_THRESHOLD=0.0
python3 ../code/gestalt.py --ownershipAssignment dbscan --inputDirectory $INPUT_DIRECTORY --outputDirectory $OUTPUT_DIRECTORY --epsilon $EPSILON --numClusters $MIN_CLUSTER_SIZE --fuzzy_threshold $FUZZY_THRESHOLD
ECHO RUNNING EXPERIMENT WITH DBSCAN EPSILON: $EPSILON MINCLUSTER: $MIN_CLUSTER_SIZE and FUZZY THRESHOLD $FUZZY_THRESHOLD
python3 ../code/experiments.py -c $INPUT_FILE

#Variables for Iteration2
EPSILON=0.000015696123058
MIN_CLUSTER_SIZE=3
FUZZY_THRESHOLD=0.1
python3 ../code/gestalt.py --ownershipAssignment dbscan --inputDirectory $INPUT_DIRECTORY --outputDirectory $OUTPUT_DIRECTORY --epsilon $EPSILON --numClusters $MIN_CLUSTER_SIZE --fuzzy_threshold $FUZZY_THRESHOLD
ECHO RUNNING EXPERIMENT WITH DBSCAN EPSILON: $EPSILON MINCLUSTER: $MIN_CLUSTER_SIZE and FUZZY THRESHOLD $FUZZY_THRESHOLD
python3 ../code/experiments.py -c $INPUT_FILE

#Variables for Iteration3
EPSILON=0.000015696123058
MIN_CLUSTER_SIZE=3
FUZZY_THRESHOLD=0.2
python3 ../code/gestalt.py --ownershipAssignment dbscan --inputDirectory $INPUT_DIRECTORY --outputDirectory $OUTPUT_DIRECTORY --epsilon $EPSILON --numClusters $MIN_CLUSTER_SIZE --fuzzy_threshold $FUZZY_THRESHOLD
ECHO RUNNING EXPERIMENT WITH DBSCAN EPSILON: $EPSILON MINCLUSTER: $MIN_CLUSTER_SIZE and FUZZY THRESHOLD $FUZZY_THRESHOLD
python3 ../code/experiments.py -c $INPUT_FILE

#Variables for Iteration4
EPSILON=0.000015696123058
MIN_CLUSTER_SIZE=3
FUZZY_THRESHOLD=0.3
python3 ../code/gestalt.py --ownershipAssignment dbscan --inputDirectory $INPUT_DIRECTORY --outputDirectory $OUTPUT_DIRECTORY --epsilon $EPSILON --numClusters $MIN_CLUSTER_SIZE --fuzzy_threshold $FUZZY_THRESHOLD
ECHO RUNNING EXPERIMENT WITH DBSCAN EPSILON: $EPSILON MINCLUSTER: $MIN_CLUSTER_SIZE and FUZZY THRESHOLD $FUZZY_THRESHOLD
python3 ../code/experiments.py -c $INPUT_FILE

#Variables for Iteration5
EPSILON=0.000015696123058
MIN_CLUSTER_SIZE=3
FUZZY_THRESHOLD=0.4
python3 ../code/gestalt.py --ownershipAssignment dbscan --inputDirectory $INPUT_DIRECTORY --outputDirectory $OUTPUT_DIRECTORY --epsilon $EPSILON --numClusters $MIN_CLUSTER_SIZE --fuzzy_threshold $FUZZY_THRESHOLD
ECHO RUNNING EXPERIMENT WITH DBSCAN EPSILON: $EPSILON MINCLUSTER: $MIN_CLUSTER_SIZE and FUZZY THRESHOLD $FUZZY_THRESHOLD
python3 ../code/experiments.py -c $INPUT_FILE