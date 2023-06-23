# GESTALT Project:

# INSTRUCTIONS FOR USE

## Prepare the environment: 

Writing this assuming the use of HomeBrew, so some changes will need to be made if you are working on another system. 

Download the python distribution that is compatible with Tkinker; we use **python-tk@3.11**

    brew install python-tk@3.11

Clone the Git Repo: 

    https://github.com/osullik/GESTALT.git

Navigate to the root of that project ~/GESTALT/

    cd GESTALT

create a virtual environment using the requirements.txt

    python -m venv gestalt_env

You now need to like Tkinter to your venv, [This slack overflow post](https://stackoverflow.com/questions/15884075/tkinter-in-a-virtualenv) is helpful, but assuming you installed as above use (dependent on your version): 

    cd gestalt_env/lib

    ln -s /opt/homebrew/Cellar/python-tk@3.11/3.11.4

[optional] if unsure of your versions, use the following command to list out your python versions in homebrew: 

    brew list | grep "python"

change back to the root directory

    cd ../..

and activate your virtual environment 

    source gestalt_env/bin/activate

install the requirements for the venv: 

    pip install -r code/requrements.txt

if you're not intending to collect all the data yourself you'll need to download the data folder and replace the existing data folder with it

    [Google Drive Link](https://drive.google.com/drive/folders/1-YSaEZ9dwJy6IG7oMcPr12XJrsQIi_ox?usp=drive_link)

With all this in place you're ready to start working with GESTALT!

## End to End Experiments

To demonstrate the utility of GESTALT and allow for the replication of our results, we offer two bash scripts to build and execute GESTALT for each respective datatset. 

To get the files from FLICKR you need API Keys. API access can be requested [here](https://www.flickr.com/services/api/misc.api_keys.html). You then need to add them to your local environment variables with commands

        flickr_key=<your_api_key_here>
        flickr_secret=<your_secret_key_here>

To use the end-to-end scripts, navigate to the scripts folder from the root directory **IMPORTANT: The scripts use relative directory addressing and all assume that they are being executed from within the GESTALT/scripts directory**: 

        cd scripts

### Swan Valley Wineries:

        99a_ingestSwanValley.sh	

### DC:

        99b_IngestDC.sh

Note that after you have run the shell scritps for the first time you may want to comment out the lines that invokes the querying of FLICKR - the results will be stored after a single run. 

## Running components
Note that depending on which experiment you are running you will need to modify the paths in the 'individual' scripts below. 

### Data Collection

Navigate to the scripts folder from the root directory **IMPORTANT: The scripts use relative directory addressing and all assume that they are being executed from within the GESTALT/scripts directory**: 

        cd scripts

To extract the KML files run the following command (note: you can add or subtract additional KML files following the instructions in the script)

        sh 10_ingestKML.sh

The JSON outputs of the KML files will reside in *GESTALT/data/output/dataCollection*

To extract all objects within a bounding box from the overpass API use the following (noting that you can edit the bounding box and in the shell file):

        sh 20_queryAllObjects.sh

The JSON output of the query will reside in *GESTALT/data/output/dataCollection/osm_:bbox:_allobjects.json* (whrre :bbox: is the bounding box the objects are found in.)

To get the files from FLICKR you need API Keys. API access can be requested [here](https://www.flickr.com/services/api/misc.api_keys.html). You then need to add them to your local environment variables with commands

        flickr_key=<your_api_key_here>
        flickr_secret=<your_secret_key_here>

then you can access the flickr and download all relevant images using:

        sh 30_queryFlickr.sh

and to extract the objects fro, them run: 

        sh 40_ingestFlickrObjects.sh

To extract the locations with specific search terms from the Openstreetmaps overpass API use the following (noting that you can edit the bounding box and search terms in the shell file):

        sh 50_queryLocations.sh

The JSON output of the query will reside in *GESTALT/data/output/dataCollection/:osmsearchTermList:.json* (where :osmsearchTermList is the concatenated list of all search terms)

This completes the data collection phase

### Ownership Assignment 
The ownership assignment analyses the collected data, and determines which objects belong to which location. To run these steps, do: 

        sh 60a_assign_kmeans.sh

        sh 60b_assign_dbscan.sh

These will output their results to: *GESTALT/data/output/owneshipAssignment/KMEANS_PredictedLocations.csv* and *GESTALT/data/output/owneshipAssignment/DBSCAN_PredictedLocations.csv* respectively

### Concept Mapping
The concept mapping takes the predicted loctations of each objects and creates a grid representation of the locaiton to be used in searching. to execute it, run: 

        sh 61_createConceptMaps.sh

### Search

To activate the search functions run:

        sh 70_searchGestalt.sh

## User Interface

        python ../code/UI.py

