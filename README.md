# GESTALT Project:

# INSTRUCTIONS FOR USE

## Data Collection

To run the code, first, create the appropriate venv in the root directory of gestalt using the following commands: 

        python3 -m venv gestalt_env

        source gestalt_env/bin/activate

        pip3 install -r requirements.txt

Then, navigate to the scripts folder from the root directory: 

        cd scripts

To extract the KML files run the following command (note: you can add or subtract additional KML files following the instructions in the script)

        sh ingestKML.sh

The JSON outputs of the KML files will reside in *GESTALT/data/output/dataCollection*

To extract the objects from the Openstreetmaps overpass turbo API use the following (noting that you can edit the bounding box and search terms in the shell file):

        sh queryOSM.sh

The JSON output of the query will reside in *GESTALT/data/output/dataCollection/osm.json*

## Ownership Assignment 

## Concept Mapping

## Search

# TODO: 

- [ ] Codebase 
    - [X] Refactor Data Collection into its own file
    - [X] Refactor Ownership Assignment into its own file
    - [ ] Refactor Concept Mapping into its own file
    - [ ] Refactor Search into its own file
    - [ ] Refactor visualisation into its own file. 

- [ ] Dataset
    - [ ] Label the remainder of the Swan Valley Wineries
    - [ ] Label a medium-density dataset
    - [ ] Label a high-density dataset

- [ ] Data Collection
    - [ ] Trial Object Detection on Street-view Imagery from OSM for object geo estimates
    - [ ] Trial Object Detection on user-contributed Imagery from OSM for object geo estimates
    - [ ] Trial depth estimation of objects in imagery
    - [ ] Trial Grid alignment of RSI Imagery 
    - [ ] Trial intersection RSI and ground level object detection to improve geo-estimates of objects

- [ ] Ownership Assignment **PRIORITY 3**
    - [ ] Implement DVBSCAN
    - [ ] Implement Bounding Polygon membership inference

- [ ] Concept Mapping **PRIORITY 1**
    - [ ] Fully Implement Arithmetic-Based method
    - [ ] Implement KD-Tree Method
    - [ ] Implement Graph-Bases method

- [ ] Search **PRIORITY 2**
    - [ ] Implement Bloom Filters for each location
    - [ ] Implement vector embedding lookup for search terms
    - [ ] Implement geospatial search
    - [ ] Implement pictoral search interface

