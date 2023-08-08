INVERTED_INDEX=../data/SV/output/ownershipAssignment/DBSCAN_PredictedLocations_FT=0.0.csv
CONCEPT_MAPS=../data/SV/output/concept_mapping/ConceptMaps_DBSCAN_PredictedLocations_FT=0.0.pkl
UI_LOCATIONS=../data/SV/output/concept_mapping/RelativeLocations_DBSCAN_PredictedLocations_FT=0.0.JSON

# Launch UI
echo LAUNCHING UI
python3 ../code/UI.py --inputFile $INVERTED_INDEX --conceptMapFile $CONCEPT_MAPS --locationsFile $UI_LOCATIONS