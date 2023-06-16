#queryFlickr.sh

#shell script to automate the download and object extraction of objects from FLICKR

#Variables (update these to change the python script that runs)

#TODO:

    # Move parameters to here from queryFlickrAPI 
    # Add an argParser to queryFlickrAPI

#Activate the venv
source ../gestalt_env/bin/activate

#Increase the max file limit so that the object detection can run:

ulimit -n 2500

#Run the script
python3 ../code/queryFlickr.py -p -if $INPUTFILE -o $OUTPUTFILE
