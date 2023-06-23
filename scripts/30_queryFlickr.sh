#queryFlickr.sh

#shell script to automate the download and object extraction of objects from FLICKR

#Variables (update these to change the python script that runs)

LL_LAT="-31.90009882641578"
LL_LON="115.96168231510637"
TR_LAT="-31.77307863942101" 
TR_LON="116.05029961853784"

OUTPUTDIRECTORY="../data/SV/photos/"  #note .json extension will be applied by python script


#Activate the venv
source ../gestalt_env/bin/activate

#Increase the max file limit so that the object detection can run:

ulimit -n 1000

#Check env variables: 

echo "your FLICKR API Key is:" $flickr_key
echo "your FLICKR Secret key is:" $flickr_secret

#Run the script
python3 ../code/gestalt.py -pd -b $LL_LON $LL_LAT $TR_LON $TR_LAT -od $OUTPUTDIRECTORY

