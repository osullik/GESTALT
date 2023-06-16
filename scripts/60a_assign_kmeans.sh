#assign_mmeans.sh

#shell script to automate the invocation of KMeans ownershop assignment. 

#Variables (update these to change the python script that runs)
INPUT_DIRECTORY="../data/output/datacollection"
OUTPUT_DIRECTORY="../data/output/ownershipAssignment"
NUMCLUSTERS=6


#Activate the venv
source ../gestalt_env/bin/activate

#Run the script
python3 ../code/gestalt.py --ownershipAssignment kmeans --inputDirectory $INPUT_DIRECTORY --outputDirectory $OUTPUT_DIRECTORY -n $NUMCLUSTERS
