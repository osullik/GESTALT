#assign_dbscan.sh

#shell script to automate the invocation of DBSCAN ownershop assignment. 

#Variables (update these to change the python script that runs)
INPUT_DIRECTORY="../data/output/datacollection"
OUTPUT_DIRECTORY="../data/output/ownershipAssignment"
# Epsilon here = 0.1/6371 (i.e. approx 180m in lat/long)
EPSILON=0.000015696123058
MIN_CLUSTER_SIZE=3

#Activate the venv
source ../gestalt_env/bin/activate

#Run the script
python3 ../code/gestalt.py --ownershipAssignment dbscan --inputDirectory $INPUT_DIRECTORY --outputDirectory $OUTPUT_DIRECTORY --epsilon $EPSILON --numClusters $MIN_CLUSTER_SIZE
