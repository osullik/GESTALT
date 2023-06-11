#ingestFlickrObjects.sh

#shell script to automate the ingestion of all objects from a flickr photo dump to GESTALT 

#Variables (update these to change the python script that runs)

INPUTFILE="../data/photos/115.96168231510637_-31.90009882641578_116.05029961853784_-31.77307863942101/metadata_objects.json"
OUTPUTFILE="../data/output/dataCollection/flickr"  #note .json extension will be applied by python script


#Activate the venv
source ../gestalt_env/bin/activate

#Run the script
python3 ../code/gestalt.py -p -of $INPUTFILE -o $OUTPUTFILE
