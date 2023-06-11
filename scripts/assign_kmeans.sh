#assign_mmeans.sh

#shell script to automate the invocation of KMeans ownershop assignment. 

#Variables (update these to change the python script that runs)
LOCATIONSFILE="../data/output/datacollection/osmwinerybrewery.json"
OBJECTSFILE="../data/output/datacollection/osm_-31.90009882641578115.96168231510637-31.77307863942101116.05029961853784_allobjects.json"
OUTPUTFILE="../data/output/dataCollection/osm"  #note .json extension will be applied by python script
NUMCLUSTERS=6


#Activate the venv
source ../gestalt_env/bin/activate

#Run the script
python3 ../code/gestalt.py --ownershipAssignment kmeans --locationsFile $LOCATIONSFILE --objectsFile $OBJECTSFILE -n $NUMCLUSTERS
