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

install the requirements: 

    pip install -r code/requrements.txt

and activate your virtual environment once installation is complete 

    source gestalt_env/bin/activate

if you're not intending to collect all the data yourself you'll need to download the data folder and replace the existing data folder with it

    [Google Drive Link](https://drive.google.com/drive/folders/1-YSaEZ9dwJy6IG7oMcPr12XJrsQIi_ox?usp=drive_link)

With all this in place you're ready to start working with GESTALT!

## Data Collection

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

## Ownership Assignment 
The ownership assignment analyses the collected data, and determines which objects belong to which location. To run these steps, do: 

        sh 60a_assign_kmeans.sh

        sh 60b_assign_dbscan.sh

These will output their results to: *GESTALT/data/output/owneshipAssignment/KMEANS_PredictedLocations.csv* and *GESTALT/data/output/owneshipAssignment/DBSCAN_PredictedLocations.csv* respectively

## Concept Mapping
The concept mapping takes the predicted loctations of each objects and creates a grid representation of the locaiton to be used in searching. to execute it, run: 

        sh 61_createConceptMaps.sh

## Search

To activate the search functions run:

        sh 70_searchGestalt.sh

# TODO: 

- [ ] Codebase 
    - [X] Refactor Data Collection into its own file (27 May)
    - [X] Refactor Ownership Assignment into its own file (06 Jun)
    - [X] Refactor Concept Mapping into its own file
    - [X] Refactor Search into its own file
    - [ ] Refactor visualisation into its own file (i.e. auto-generate graphs). 
    - [X] Refactor queryFlickr into the DataCollection file

- [ ] Dataset
    - [ ] Label the remainder of the Swan Valley Wineries
    - [ ] Label a medium-density dataset
    - [ ] Label a high-density dataset

- [ ] Data Collection
    - [X] Refactor DataCollector to accept multiple seach terms (08 Jun)
    - [X] Refactor DataCollector to return all named objects within a boundingBox (08 Jun)
    - [ ] [OPTIONAL]Trial Object Detection on Street-view Imagery from OSM for object geo estimates
    - [X] Trial Object Detection on user-contributed Imagery from Flickr for object geo estimates
    - [ ] Implement naive object geolocation with image orientation and object coordinate information. @nicoleschnieder / @osullik
    - [ ] [OPTIONAL]Trial depth estimation of objects in imagery
    - [ ] [OPTIONAL]Trial Grid alignment of RSI Imagery 
    - [ ] [OPTIONAL]Trial intersection RSI and ground level object detection to improve geo-estimates of objects

- [X] Ownership Assignment **PRIORITY 3**
    - [ ] [OPTIONAL]Implement DVBSCAN
    - [ ] [OPTIONAL]Implement Bounding Polygon membership inference
    - [X] Add probabilites to clustering @nicoleSchneider

- [X] Concept Mapping **PRIORITY 1**
    - [X] Implement Grid-Based Method
        - [X]  Convert a Location into a Grid of Objects @osullik (16 Jun)
        - [X] Convert a query term into an ordered list @osullik (16 Jun)
        - [X] Integrate Grid-Based Method @osullik (16 Jun)
        - [X] Refactor conceptMapper to accept ordered list of inputs @osullik (16 Jun)
    - [ ] [OPTIONAL] Impement Isomorphic Subgraph Method

- [ ] Search **PRIORITY 2**
    - [X] Implement Search of Object membership
        - [X] Implement Inverted Index search; shortlist objects
        - [X] Implement probabilities @nicoleschneider
        - [X] Implement ranking of Results @nicoleschneider
    - [X] Implement Search of Concept Map
        - [X] Implement geospatial search (i.e. look up concept map) @osullik 17 Jun
        - [X] Implement pictoral search interface @nicoleschneider / @osullik 18 Jun
    - [ ] Implement Fuzzy Search @nicoleschneider / @osullik
        - [ ] Implement string similarity lookups
        - [ ] Implement resolution of query terms to OSM object tags
        - [ ] Implement vector embedding lookup for search terms

- [ ] Experiments
    - [ ] Implement a script that runs experiments end-to-end (script of scripts). @osullik / @nicoleschneider
    - [ ] Make ground truth queries
    - [ ] Clustering metrics and comparisons
    - [ ] Precision on larger dataset
    - [ ] Scalability and complexity
    - [ ] Complexity Analysis

- [ ] Write up
    - [ ] Lit Review @osullik
    - [ ] Writing
        - [ ] Tables
        - [ ] Algorithms
        - [ ] System Diagrams



