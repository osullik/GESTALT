#createConceptMaps.sh

#Activate the venv
source ../gestalt_env/bin/activate

#Common Variables:
INPUT_DIRECTORY="../data/output/datacollection"
OUTPUT_DIRECTORY="../data/output/ownershipAssignment"
INPUT_FILE="../data/output/ownershipAssignment/DBSCAN_PredictedLocations.csv"

# Clean out Existing data:
echo DELETING OLD DATA
rm -r ../data/output/dataCollection
mkdir ../data/output/dataCollection

# Add in only the known data

echo = = = = = = = = = RUNNING EXPERIMENTS FOR HAND LABELLED DATA ONLY = = = = = = = = = 

sh 10_ingestKML.sh
sh 50_queryLocations.sh


#Variables for Iteration1
EPSILON=0.000015696123058
MIN_CLUSTER_SIZE=3
FUZZY_THRESHOLD=0.0
python3 ../code/gestalt.py --ownershipAssignment dbscan --inputDirectory $INPUT_DIRECTORY --outputDirectory $OUTPUT_DIRECTORY --epsilon $EPSILON --numClusters $MIN_CLUSTER_SIZE --fuzzy_threshold $FUZZY_THRESHOLD
ECHO RUNNING EXPERIMENT WITH DBSCAN EPSILON: $EPSILON MINCLUSTER: $MIN_CLUSTER_SIZE and FUZZY THRESHOLD $FUZZY_THRESHOLD
python3 ../code/ClusteringMetrics.py -c $INPUT_FILE

#Variables for Iteration2
EPSILON=0.000015696123058
MIN_CLUSTER_SIZE=3
FUZZY_THRESHOLD=0.1
python3 ../code/gestalt.py --ownershipAssignment dbscan --inputDirectory $INPUT_DIRECTORY --outputDirectory $OUTPUT_DIRECTORY --epsilon $EPSILON --numClusters $MIN_CLUSTER_SIZE --fuzzy_threshold $FUZZY_THRESHOLD
ECHO RUNNING EXPERIMENT WITH DBSCAN EPSILON: $EPSILON MINCLUSTER: $MIN_CLUSTER_SIZE and FUZZY THRESHOLD $FUZZY_THRESHOLD
python3 ../code/ClusteringMetrics.py -c $INPUT_FILE

#Variables for Iteration3
EPSILON=0.000015696123058
MIN_CLUSTER_SIZE=3
FUZZY_THRESHOLD=0.2
python3 ../code/gestalt.py --ownershipAssignment dbscan --inputDirectory $INPUT_DIRECTORY --outputDirectory $OUTPUT_DIRECTORY --epsilon $EPSILON --numClusters $MIN_CLUSTER_SIZE --fuzzy_threshold $FUZZY_THRESHOLD
ECHO RUNNING EXPERIMENT WITH DBSCAN EPSILON: $EPSILON MINCLUSTER: $MIN_CLUSTER_SIZE and FUZZY THRESHOLD $FUZZY_THRESHOLD
python3 ../code/ClusteringMetrics.py -c $INPUT_FILE

#Variables for Iteration4
EPSILON=0.000015696123058
MIN_CLUSTER_SIZE=3
FUZZY_THRESHOLD=0.3
python3 ../code/gestalt.py --ownershipAssignment dbscan --inputDirectory $INPUT_DIRECTORY --outputDirectory $OUTPUT_DIRECTORY --epsilon $EPSILON --numClusters $MIN_CLUSTER_SIZE --fuzzy_threshold $FUZZY_THRESHOLD
ECHO RUNNING EXPERIMENT WITH DBSCAN EPSILON: $EPSILON MINCLUSTER: $MIN_CLUSTER_SIZE and FUZZY THRESHOLD $FUZZY_THRESHOLD
python3 ../code/ClusteringMetrics.py -c $INPUT_FILE

#Variables for Iteration5
EPSILON=0.000015696123058
MIN_CLUSTER_SIZE=3
FUZZY_THRESHOLD=0.4
python3 ../code/gestalt.py --ownershipAssignment dbscan --inputDirectory $INPUT_DIRECTORY --outputDirectory $OUTPUT_DIRECTORY --epsilon $EPSILON --numClusters $MIN_CLUSTER_SIZE --fuzzy_threshold $FUZZY_THRESHOLD
ECHO RUNNING EXPERIMENT WITH DBSCAN EPSILON: $EPSILON MINCLUSTER: $MIN_CLUSTER_SIZE and FUZZY THRESHOLD $FUZZY_THRESHOLD
python3 ../code/ClusteringMetrics.py -c $INPUT_FILE

#Variables for Iteration5
EPSILON=0.000015696123058
MIN_CLUSTER_SIZE=3
FUZZY_THRESHOLD=0.5
python3 ../code/gestalt.py --ownershipAssignment dbscan --inputDirectory $INPUT_DIRECTORY --outputDirectory $OUTPUT_DIRECTORY --epsilon $EPSILON --numClusters $MIN_CLUSTER_SIZE --fuzzy_threshold $FUZZY_THRESHOLD
ECHO RUNNING EXPERIMENT WITH DBSCAN EPSILON: $EPSILON MINCLUSTER: $MIN_CLUSTER_SIZE and FUZZY THRESHOLD $FUZZY_THRESHOLD
python3 ../code/ClusteringMetrics.py -c $INPUT_FILE

#Variables for Iteration5
EPSILON=0.000015696123058
MIN_CLUSTER_SIZE=3
FUZZY_THRESHOLD=0.6
python3 ../code/gestalt.py --ownershipAssignment dbscan --inputDirectory $INPUT_DIRECTORY --outputDirectory $OUTPUT_DIRECTORY --epsilon $EPSILON --numClusters $MIN_CLUSTER_SIZE --fuzzy_threshold $FUZZY_THRESHOLD
ECHO RUNNING EXPERIMENT WITH DBSCAN EPSILON: $EPSILON MINCLUSTER: $MIN_CLUSTER_SIZE and FUZZY THRESHOLD $FUZZY_THRESHOLD
python3 ../code/ClusteringMetrics.py -c $INPUT_FILE

#Variables for Iteration5
EPSILON=0.000015696123058
MIN_CLUSTER_SIZE=3
FUZZY_THRESHOLD=0.7
python3 ../code/gestalt.py --ownershipAssignment dbscan --inputDirectory $INPUT_DIRECTORY --outputDirectory $OUTPUT_DIRECTORY --epsilon $EPSILON --numClusters $MIN_CLUSTER_SIZE --fuzzy_threshold $FUZZY_THRESHOLD
ECHO RUNNING EXPERIMENT WITH DBSCAN EPSILON: $EPSILON MINCLUSTER: $MIN_CLUSTER_SIZE and FUZZY THRESHOLD $FUZZY_THRESHOLD
python3 ../code/ClusteringMetrics.py -c $INPUT_FILE

#Variables for Iteration5
EPSILON=0.000015696123058
MIN_CLUSTER_SIZE=3
FUZZY_THRESHOLD=0.8
python3 ../code/gestalt.py --ownershipAssignment dbscan --inputDirectory $INPUT_DIRECTORY --outputDirectory $OUTPUT_DIRECTORY --epsilon $EPSILON --numClusters $MIN_CLUSTER_SIZE --fuzzy_threshold $FUZZY_THRESHOLD
ECHO RUNNING EXPERIMENT WITH DBSCAN EPSILON: $EPSILON MINCLUSTER: $MIN_CLUSTER_SIZE and FUZZY THRESHOLD $FUZZY_THRESHOLD
python3 ../code/ClusteringMetrics.py -c $INPUT_FILE

#Variables for Iteration5
EPSILON=0.000015696123058
MIN_CLUSTER_SIZE=3
FUZZY_THRESHOLD=0.9
python3 ../code/gestalt.py --ownershipAssignment dbscan --inputDirectory $INPUT_DIRECTORY --outputDirectory $OUTPUT_DIRECTORY --epsilon $EPSILON --numClusters $MIN_CLUSTER_SIZE --fuzzy_threshold $FUZZY_THRESHOLD
ECHO RUNNING EXPERIMENT WITH DBSCAN EPSILON: $EPSILON MINCLUSTER: $MIN_CLUSTER_SIZE and FUZZY THRESHOLD $FUZZY_THRESHOLD
python3 ../code/ClusteringMetrics.py -c $INPUT_FILE

#Variables for Iteration5
EPSILON=0.000015696123058
MIN_CLUSTER_SIZE=3
FUZZY_THRESHOLD=1.0
python3 ../code/gestalt.py --ownershipAssignment dbscan --inputDirectory $INPUT_DIRECTORY --outputDirectory $OUTPUT_DIRECTORY --epsilon $EPSILON --numClusters $MIN_CLUSTER_SIZE --fuzzy_threshold $FUZZY_THRESHOLD
ECHO RUNNING EXPERIMENT WITH DBSCAN EPSILON: $EPSILON MINCLUSTER: $MIN_CLUSTER_SIZE and FUZZY THRESHOLD $FUZZY_THRESHOLD
python3 ../code/ClusteringMetrics.py -c $INPUT_FILE

echo = = = = = = = = = RUNNING EXPERIMENTS FOR ALL DATA = = = = = = = = = 

sh 10_ingestKML.sh
sh 20_queryAllObjects.sh
sh 40_ingestFlickrObjects.sh
sh 51_queryAllLocations.sh

#Variables for Iteration1
EPSILON=0.000015696123058
MIN_CLUSTER_SIZE=3
FUZZY_THRESHOLD=0.0
python3 ../code/gestalt.py --ownershipAssignment dbscan --inputDirectory $INPUT_DIRECTORY --outputDirectory $OUTPUT_DIRECTORY --epsilon $EPSILON --numClusters $MIN_CLUSTER_SIZE --fuzzy_threshold $FUZZY_THRESHOLD
ECHO RUNNING EXPERIMENT WITH DBSCAN EPSILON: $EPSILON MINCLUSTER: $MIN_CLUSTER_SIZE and FUZZY THRESHOLD $FUZZY_THRESHOLD
python3 ../code/ClusteringMetrics.py -c $INPUT_FILE

#Variables for Iteration2
EPSILON=0.000015696123058
MIN_CLUSTER_SIZE=3
FUZZY_THRESHOLD=0.1
python3 ../code/gestalt.py --ownershipAssignment dbscan --inputDirectory $INPUT_DIRECTORY --outputDirectory $OUTPUT_DIRECTORY --epsilon $EPSILON --numClusters $MIN_CLUSTER_SIZE --fuzzy_threshold $FUZZY_THRESHOLD
ECHO RUNNING EXPERIMENT WITH DBSCAN EPSILON: $EPSILON MINCLUSTER: $MIN_CLUSTER_SIZE and FUZZY THRESHOLD $FUZZY_THRESHOLD
python3 ../code/ClusteringMetrics.py -c $INPUT_FILE

#Variables for Iteration3
EPSILON=0.000015696123058
MIN_CLUSTER_SIZE=3
FUZZY_THRESHOLD=0.2
python3 ../code/gestalt.py --ownershipAssignment dbscan --inputDirectory $INPUT_DIRECTORY --outputDirectory $OUTPUT_DIRECTORY --epsilon $EPSILON --numClusters $MIN_CLUSTER_SIZE --fuzzy_threshold $FUZZY_THRESHOLD
ECHO RUNNING EXPERIMENT WITH DBSCAN EPSILON: $EPSILON MINCLUSTER: $MIN_CLUSTER_SIZE and FUZZY THRESHOLD $FUZZY_THRESHOLD
python3 ../code/ClusteringMetrics.py -c $INPUT_FILE

#Variables for Iteration4
EPSILON=0.000015696123058
MIN_CLUSTER_SIZE=3
FUZZY_THRESHOLD=0.3
python3 ../code/gestalt.py --ownershipAssignment dbscan --inputDirectory $INPUT_DIRECTORY --outputDirectory $OUTPUT_DIRECTORY --epsilon $EPSILON --numClusters $MIN_CLUSTER_SIZE --fuzzy_threshold $FUZZY_THRESHOLD
ECHO RUNNING EXPERIMENT WITH DBSCAN EPSILON: $EPSILON MINCLUSTER: $MIN_CLUSTER_SIZE and FUZZY THRESHOLD $FUZZY_THRESHOLD
python3 ../code/ClusteringMetrics.py -c $INPUT_FILE

#Variables for Iteration5
EPSILON=0.000015696123058
MIN_CLUSTER_SIZE=3
FUZZY_THRESHOLD=0.4
python3 ../code/gestalt.py --ownershipAssignment dbscan --inputDirectory $INPUT_DIRECTORY --outputDirectory $OUTPUT_DIRECTORY --epsilon $EPSILON --numClusters $MIN_CLUSTER_SIZE --fuzzy_threshold $FUZZY_THRESHOLD
ECHO RUNNING EXPERIMENT WITH DBSCAN EPSILON: $EPSILON MINCLUSTER: $MIN_CLUSTER_SIZE and FUZZY THRESHOLD $FUZZY_THRESHOLD
python3 ../code/ClusteringMetrics.py -c $INPUT_FILE