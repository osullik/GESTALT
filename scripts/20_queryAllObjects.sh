#queryAllObjects.sh

#shell script to automate the collection of all node (objects) from within a bounding box in OSM; assumes it is being run from the GESTALT/scripts directory

#Variables (update these to change the python script that runs)

BB_LL="-31.90009882641578"
BB_LR="115.96168231510637"
BB_TL="-31.77307863942101" 
BB_TR="116.05029961853784"
SEARCHTERM1="allobjects"
OUTPUTFILE="../data/output/dataCollection/objects_"  #note .json extension will be applied by python script


#Activate the venv
source ../gestalt_env/bin/activate

#Run the script
python3 ../code/gestalt.py -qo -b $BB_LL $BB_LR $BB_TL $BB_TR -s $SEARCHTERM1 -o $OUTPUTFILE