# GESTALT/scripts/searchGestalt.sh

#shell script to automate the searching of GESTALT

#Variables (update these to change the python script that runs)
    #Search Terms is a string with spaces delimiting search terms
INPUT_FILE="../data/output/ownershipAssignment/DBSCAN_PredictedLocations.csv"
SEARCH_TERMS1="apple wine_barrell"
SEARCH_TERMS2="fork bench bird"
SEARCH_TERMS3="bench bird"
SEARCH_TERMS4="bird"



#Activate the venv
source ../gestalt_env/bin/activate

#Run the script
python3 ../code/gestalt.py --gestaltSearch --inputFile $INPUT_FILE --searchterms $SEARCH_TERMS1
python3 ../code/gestalt.py --gestaltSearch --inputFile $INPUT_FILE --searchterms $SEARCH_TERMS2
python3 ../code/gestalt.py --gestaltSearch --inputFile $INPUT_FILE --searchterms $SEARCH_TERMS3
python3 ../code/gestalt.py --gestaltSearch --inputFile $INPUT_FILE --searchterms $SEARCH_TERMS4
