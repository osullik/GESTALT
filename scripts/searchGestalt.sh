# GESTALT/scripts/searchGestalt.sh

#shell script to automate the searching of GESTALT

#Variables (update these to change the python script that runs)
    #Search Terms is a string with spaces delimiting search terms
INPUT_FILE="../data/output/ownershipAssignment/DBSCAN_PredictedLocations.csv"
SEARCH_TERMS="tree bird"


#Activate the venv
source ../gestalt_env/bin/activate

#Run the script
python3 ../code/gestalt.py --gestaltSearch --inputFile $INPUT_FILE --searchterms $SEARCH_TERMS
