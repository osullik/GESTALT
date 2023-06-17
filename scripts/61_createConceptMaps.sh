#createConceptMaps.sh

#shell script to automate the invocation of DBSCAN ownershop assignment. 

#Variables (update these to change the python script that runs)
INPUT_FILE="../data/output/ownershipAssignment/DBSCAN_PredictedLocations.csv"
OUTPUT_DIRECTORY="../data/output/concept_mapping"

#Activate the venv
source ../gestalt_env/bin/activate

#Run the script
python3 ../code/gestalt.py -ccm --inputFile $INPUT_FILE --outputDirectory $OUTPUT_DIRECTORY