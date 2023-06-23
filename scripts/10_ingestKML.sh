#ingestKML.sh

#shell script to automate the collection extraction of data from KML files; assumes it is being run from the GESTALT/scripts directory

#Variables (update these to change the python script that runs)

KMLFILE1="../data/SV/input/Swan_Valley.kml"
### Add any additional kml files below, then insert them appropriately in the below script following the -f tag
#kmlFile2="../data/Buladelad.kml"
#...
#kmlFileN=

OUTPUTFILENAME="../data/SV/output/experiments/dataCollection/objects_KML" #the python code will append a ".json", don't include it here. 


#Activate the venv
source ../gestalt_env/bin/activate

#Run the Script
python3 ../code/gestalt.py -k -f $KMLFILE1 -o $OUTPUTFILENAME