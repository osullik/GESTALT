#createConceptMaps.sh

#Activate the venv
source ../gestalt_env/bin/activate

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
sh 10_ingestKML.sh
sh 50_queryLocations.sh



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

sh 10_ingestKML.sh
sh 20_queryAllObjects.sh
sh 40_ingestFlickrObjects.sh
sh 51_queryAllLocations.sh

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
