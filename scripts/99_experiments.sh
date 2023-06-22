#createConceptMaps.sh

#Activate the venv
source ../gestalt_env/bin/activate

#Common Variables:
INPUT_DIRECTORY="../data/output/datacollection"
OUTPUT_DIRECTORY="../data/output/ownershipAssignment/wineries_only"
INPUT_FILE="../data/output/ownershipAssignment/DBSCAN_PredictedLocations.csv"

# Clean out Existing data:
echo DELETING OLD DATA
rm -r ../data/output/dataCollection
mkdir ../data/output/dataCollection

# Add in only the known data

echo = = = = = = = = = RUNNING EXPERIMENTS FOR HAND LABELLED DATA ONLY = = = = = = = = = 

sh 10_ingestKML.sh
sh 50_queryLocations.sh

# Common Varaibles
EPSILON=0.000015696123058
MIN_CLUSTER_SIZE=3

#Variables for Iteration1

FUZZY_THRESHOLD=0.0
python3 ../code/gestalt.py --ownershipAssignment dbscan --inputDirectory $INPUT_DIRECTORY --outputDirectory $OUTPUT_DIRECTORY --epsilon $EPSILON --numClusters $MIN_CLUSTER_SIZE --fuzzy_threshold $FUZZY_THRESHOLD
ECHO RUNNING EXPERIMENT WITH DBSCAN EPSILON: $EPSILON MINCLUSTER: $MIN_CLUSTER_SIZE and FUZZY THRESHOLD $FUZZY_THRESHOLD
#python3 ../code/ClusteringMetrics.py -c $INPUT_FILE

#Variables for Iteration2
FUZZY_THRESHOLD=0.5
python3 ../code/gestalt.py --ownershipAssignment dbscan --inputDirectory $INPUT_DIRECTORY --outputDirectory $OUTPUT_DIRECTORY --epsilon $EPSILON --numClusters $MIN_CLUSTER_SIZE --fuzzy_threshold $FUZZY_THRESHOLD
ECHO RUNNING EXPERIMENT WITH DBSCAN EPSILON: $EPSILON MINCLUSTER: $MIN_CLUSTER_SIZE and FUZZY THRESHOLD $FUZZY_THRESHOLD
#python3 ../code/ClusteringMetrics.py -c $INPUT_FILE

#Variables for Iteration3
FUZZY_THRESHOLD=1.0
python3 ../code/gestalt.py --ownershipAssignment dbscan --inputDirectory $INPUT_DIRECTORY --outputDirectory $OUTPUT_DIRECTORY --epsilon $EPSILON --numClusters $MIN_CLUSTER_SIZE --fuzzy_threshold $FUZZY_THRESHOLD
ECHO RUNNING EXPERIMENT WITH DBSCAN EPSILON: $EPSILON MINCLUSTER: $MIN_CLUSTER_SIZE and FUZZY THRESHOLD $FUZZY_THRESHOLD
#python3 ../code/ClusteringMetrics.py -c $INPUT_FILE

#Variables for Iteration4
FUZZY_THRESHOLD=1.5
python3 ../code/gestalt.py --ownershipAssignment dbscan --inputDirectory $INPUT_DIRECTORY --outputDirectory $OUTPUT_DIRECTORY --epsilon $EPSILON --numClusters $MIN_CLUSTER_SIZE --fuzzy_threshold $FUZZY_THRESHOLD
ECHO RUNNING EXPERIMENT WITH DBSCAN EPSILON: $EPSILON MINCLUSTER: $MIN_CLUSTER_SIZE and FUZZY THRESHOLD $FUZZY_THRESHOLD
#python3 ../code/ClusteringMetrics.py -c $INPUT_FILE

#Variables for Iteration5
FUZZY_THRESHOLD=2.0
python3 ../code/gestalt.py --ownershipAssignment dbscan --inputDirectory $INPUT_DIRECTORY --outputDirectory $OUTPUT_DIRECTORY --epsilon $EPSILON --numClusters $MIN_CLUSTER_SIZE --fuzzy_threshold $FUZZY_THRESHOLD
ECHO RUNNING EXPERIMENT WITH DBSCAN EPSILON: $EPSILON MINCLUSTER: $MIN_CLUSTER_SIZE and FUZZY THRESHOLD $FUZZY_THRESHOLD
#python3 ../code/ClusteringMetrics.py -c $INPUT_FILE

#Variables for Iteration6
FUZZY_THRESHOLD=2.5
python3 ../code/gestalt.py --ownershipAssignment dbscan --inputDirectory $INPUT_DIRECTORY --outputDirectory $OUTPUT_DIRECTORY --epsilon $EPSILON --numClusters $MIN_CLUSTER_SIZE --fuzzy_threshold $FUZZY_THRESHOLD
ECHO RUNNING EXPERIMENT WITH DBSCAN EPSILON: $EPSILON MINCLUSTER: $MIN_CLUSTER_SIZE and FUZZY THRESHOLD $FUZZY_THRESHOLD
#python3 ../code/ClusteringMetrics.py -c $INPUT_FILE

#Variables for Iteration7
FUZZY_THRESHOLD=3.0
python3 ../code/gestalt.py --ownershipAssignment dbscan --inputDirectory $INPUT_DIRECTORY --outputDirectory $OUTPUT_DIRECTORY --epsilon $EPSILON --numClusters $MIN_CLUSTER_SIZE --fuzzy_threshold $FUZZY_THRESHOLD
ECHO RUNNING EXPERIMENT WITH DBSCAN EPSILON: $EPSILON MINCLUSTER: $MIN_CLUSTER_SIZE and FUZZY THRESHOLD $FUZZY_THRESHOLD
#python3 ../code/ClusteringMetrics.py -c $INPUT_FILE

#Variables for Iteration8

FUZZY_THRESHOLD=3.5
python3 ../code/gestalt.py --ownershipAssignment dbscan --inputDirectory $INPUT_DIRECTORY --outputDirectory $OUTPUT_DIRECTORY --epsilon $EPSILON --numClusters $MIN_CLUSTER_SIZE --fuzzy_threshold $FUZZY_THRESHOLD
ECHO RUNNING EXPERIMENT WITH DBSCAN EPSILON: $EPSILON MINCLUSTER: $MIN_CLUSTER_SIZE and FUZZY THRESHOLD $FUZZY_THRESHOLD
#python3 ../code/ClusteringMetrics.py -c $INPUT_FILE

#Variables for Iteration9
FUZZY_THRESHOLD=4.0
python3 ../code/gestalt.py --ownershipAssignment dbscan --inputDirectory $INPUT_DIRECTORY --outputDirectory $OUTPUT_DIRECTORY --epsilon $EPSILON --numClusters $MIN_CLUSTER_SIZE --fuzzy_threshold $FUZZY_THRESHOLD
ECHO RUNNING EXPERIMENT WITH DBSCAN EPSILON: $EPSILON MINCLUSTER: $MIN_CLUSTER_SIZE and FUZZY THRESHOLD $FUZZY_THRESHOLD
#python3 ../code/ClusteringMetrics.py -c $INPUT_FILE

#Variables for Iteration10
FUZZY_THRESHOLD=4.5
python3 ../code/gestalt.py --ownershipAssignment dbscan --inputDirectory $INPUT_DIRECTORY --outputDirectory $OUTPUT_DIRECTORY --epsilon $EPSILON --numClusters $MIN_CLUSTER_SIZE --fuzzy_threshold $FUZZY_THRESHOLD
ECHO RUNNING EXPERIMENT WITH DBSCAN EPSILON: $EPSILON MINCLUSTER: $MIN_CLUSTER_SIZE and FUZZY THRESHOLD $FUZZY_THRESHOLD
#python3 ../code/ClusteringMetrics.py -c $INPUT_FILE

#Variables for Iteration11
FUZZY_THRESHOLD=100
python3 ../code/gestalt.py --ownershipAssignment dbscan --inputDirectory $INPUT_DIRECTORY --outputDirectory $OUTPUT_DIRECTORY --epsilon $EPSILON --numClusters $MIN_CLUSTER_SIZE --fuzzy_threshold $FUZZY_THRESHOLD
ECHO RUNNING EXPERIMENT WITH DBSCAN EPSILON: $EPSILON MINCLUSTER: $MIN_CLUSTER_SIZE and FUZZY THRESHOLD $FUZZY_THRESHOLD
#python3 ../code/ClusteringMetrics.py -c $INPUT_FILE

echo = = = = = = = = = RUNNING EXPERIMENTS FOR ALL DATA = = = = = = = = = 

OUTPUT_DIRECTORY="../data/output/ownershipAssignment/combined"
EPSILON=0.000015696123058
MIN_CLUSTER_SIZE=3

sh 10_ingestKML.sh
sh 20_queryAllObjects.sh
sh 40_ingestFlickrObjects.sh
sh 51_queryAllLocations.sh

#Variables for Iteration1
FUZZY_THRESHOLD=0.0
python3 ../code/gestalt.py --ownershipAssignment dbscan --inputDirectory $INPUT_DIRECTORY --outputDirectory $OUTPUT_DIRECTORY --epsilon $EPSILON --numClusters $MIN_CLUSTER_SIZE --fuzzy_threshold $FUZZY_THRESHOLD
ECHO RUNNING EXPERIMENT WITH DBSCAN EPSILON: $EPSILON MINCLUSTER: $MIN_CLUSTER_SIZE and FUZZY THRESHOLD $FUZZY_THRESHOLD
#python3 ../code/ClusteringMetrics.py -c $INPUT_FILE

#Variables for Iteration2
FUZZY_THRESHOLD=0.5
python3 ../code/gestalt.py --ownershipAssignment dbscan --inputDirectory $INPUT_DIRECTORY --outputDirectory $OUTPUT_DIRECTORY --epsilon $EPSILON --numClusters $MIN_CLUSTER_SIZE --fuzzy_threshold $FUZZY_THRESHOLD
ECHO RUNNING EXPERIMENT WITH DBSCAN EPSILON: $EPSILON MINCLUSTER: $MIN_CLUSTER_SIZE and FUZZY THRESHOLD $FUZZY_THRESHOLD
#python3 ../code/ClusteringMetrics.py -c $INPUT_FILE

#Variables for Iteration3
FUZZY_THRESHOLD=1.0
python3 ../code/gestalt.py --ownershipAssignment dbscan --inputDirectory $INPUT_DIRECTORY --outputDirectory $OUTPUT_DIRECTORY --epsilon $EPSILON --numClusters $MIN_CLUSTER_SIZE --fuzzy_threshold $FUZZY_THRESHOLD
ECHO RUNNING EXPERIMENT WITH DBSCAN EPSILON: $EPSILON MINCLUSTER: $MIN_CLUSTER_SIZE and FUZZY THRESHOLD $FUZZY_THRESHOLD
#python3 ../code/ClusteringMetrics.py -c $INPUT_FILE

#Variables for Iteration4
FUZZY_THRESHOLD=1.5
python3 ../code/gestalt.py --ownershipAssignment dbscan --inputDirectory $INPUT_DIRECTORY --outputDirectory $OUTPUT_DIRECTORY --epsilon $EPSILON --numClusters $MIN_CLUSTER_SIZE --fuzzy_threshold $FUZZY_THRESHOLD
ECHO RUNNING EXPERIMENT WITH DBSCAN EPSILON: $EPSILON MINCLUSTER: $MIN_CLUSTER_SIZE and FUZZY THRESHOLD $FUZZY_THRESHOLD
#python3 ../code/ClusteringMetrics.py -c $INPUT_FILE

#Variables for Iteration5
FUZZY_THRESHOLD=2.0
python3 ../code/gestalt.py --ownershipAssignment dbscan --inputDirectory $INPUT_DIRECTORY --outputDirectory $OUTPUT_DIRECTORY --epsilon $EPSILON --numClusters $MIN_CLUSTER_SIZE --fuzzy_threshold $FUZZY_THRESHOLD
ECHO RUNNING EXPERIMENT WITH DBSCAN EPSILON: $EPSILON MINCLUSTER: $MIN_CLUSTER_SIZE and FUZZY THRESHOLD $FUZZY_THRESHOLD
#python3 ../code/ClusteringMetrics.py -c $INPUT_FILE

#Variables for Iteration6
FUZZY_THRESHOLD=2.5
python3 ../code/gestalt.py --ownershipAssignment dbscan --inputDirectory $INPUT_DIRECTORY --outputDirectory $OUTPUT_DIRECTORY --epsilon $EPSILON --numClusters $MIN_CLUSTER_SIZE --fuzzy_threshold $FUZZY_THRESHOLD
ECHO RUNNING EXPERIMENT WITH DBSCAN EPSILON: $EPSILON MINCLUSTER: $MIN_CLUSTER_SIZE and FUZZY THRESHOLD $FUZZY_THRESHOLD
#python3 ../code/ClusteringMetrics.py -c $INPUT_FILE

#Variables for Iteration7
FUZZY_THRESHOLD=3.0
python3 ../code/gestalt.py --ownershipAssignment dbscan --inputDirectory $INPUT_DIRECTORY --outputDirectory $OUTPUT_DIRECTORY --epsilon $EPSILON --numClusters $MIN_CLUSTER_SIZE --fuzzy_threshold $FUZZY_THRESHOLD
ECHO RUNNING EXPERIMENT WITH DBSCAN EPSILON: $EPSILON MINCLUSTER: $MIN_CLUSTER_SIZE and FUZZY THRESHOLD $FUZZY_THRESHOLD
#python3 ../code/ClusteringMetrics.py -c $INPUT_FILE

#Variables for Iteration8
EPSILON=0.000015696123058
MIN_CLUSTER_SIZE=3
FUZZY_THRESHOLD=3.5
python3 ../code/gestalt.py --ownershipAssignment dbscan --inputDirectory $INPUT_DIRECTORY --outputDirectory $OUTPUT_DIRECTORY --epsilon $EPSILON --numClusters $MIN_CLUSTER_SIZE --fuzzy_threshold $FUZZY_THRESHOLD
ECHO RUNNING EXPERIMENT WITH DBSCAN EPSILON: $EPSILON MINCLUSTER: $MIN_CLUSTER_SIZE and FUZZY THRESHOLD $FUZZY_THRESHOLD
#python3 ../code/ClusteringMetrics.py -c $INPUT_FILE

#Variables for Iteration9
FUZZY_THRESHOLD=4.0
python3 ../code/gestalt.py --ownershipAssignment dbscan --inputDirectory $INPUT_DIRECTORY --outputDirectory $OUTPUT_DIRECTORY --epsilon $EPSILON --numClusters $MIN_CLUSTER_SIZE --fuzzy_threshold $FUZZY_THRESHOLD
ECHO RUNNING EXPERIMENT WITH DBSCAN EPSILON: $EPSILON MINCLUSTER: $MIN_CLUSTER_SIZE and FUZZY THRESHOLD $FUZZY_THRESHOLD
#python3 ../code/ClusteringMetrics.py -c $INPUT_FILE

#Variables for Iteration10
FUZZY_THRESHOLD=4.5
python3 ../code/gestalt.py --ownershipAssignment dbscan --inputDirectory $INPUT_DIRECTORY --outputDirectory $OUTPUT_DIRECTORY --epsilon $EPSILON --numClusters $MIN_CLUSTER_SIZE --fuzzy_threshold $FUZZY_THRESHOLD
ECHO RUNNING EXPERIMENT WITH DBSCAN EPSILON: $EPSILON MINCLUSTER: $MIN_CLUSTER_SIZE and FUZZY THRESHOLD $FUZZY_THRESHOLD
#python3 ../code/ClusteringMetrics.py -c $INPUT_FILE

#Variables for Iteration11
FUZZY_THRESHOLD=100
python3 ../code/gestalt.py --ownershipAssignment dbscan --inputDirectory $INPUT_DIRECTORY --outputDirectory $OUTPUT_DIRECTORY --epsilon $EPSILON --numClusters $MIN_CLUSTER_SIZE --fuzzy_threshold $FUZZY_THRESHOLD
ECHO RUNNING EXPERIMENT WITH DBSCAN EPSILON: $EPSILON MINCLUSTER: $MIN_CLUSTER_SIZE and FUZZY THRESHOLD $FUZZY_THRESHOLD
#python3 ../code/ClusteringMetrics.py -c $INPUT_FILE