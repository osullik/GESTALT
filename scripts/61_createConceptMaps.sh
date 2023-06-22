#createConceptMaps.sh

#shell script to automate the invocation of DBSCAN ownershop assignment. 

#Variables (update these to change the python script that runs)
INPUT_FILE="../data/output/ownershipAssignment/DBSCAN_PredictedLocations.csv"
OUTPUT_DIRECTORY="../data/output/concept_mapping"
LOCATIONS_FILE="../data/output/dataCollection/locations_-31.90009882641578115.96168231510637-31.77307863942101116.05029961853784_alllocations.json"

#Activate the venv
source ../gestalt_env/bin/activate

#Run the script
python3 ../code/gestalt.py -ccm --inputFile $INPUT_FILE --outputDirectory $OUTPUT_DIRECTORY --fileSource $LOCATIONS_FILE