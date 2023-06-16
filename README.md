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

To extract the locations with specific search terms from the Openstreetmaps overpass API use the following (noting that you can edit the bounding box and search terms in the shell file):

        sh queryLocations.sh

The JSON output of the query will reside in *GESTALT/data/output/dataCollection/:osmsearchTermList:.json* (where :osmsearchTermList is the concatenated list of all search terms)

To extract all objects within a bounding box from the overpass API use the following (noting that you can edit the bounding box and in the shell file):

        sh queryAllObjects.sh

The JSON output of the query will reside in *GESTALT/data/output/dataCollection/osm_:bbox:_allobjects.json* (whrre :bbox: is the bounding box the objects are found in.)



## Ownership Assignment 

## Concept Mapping

## Search

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
    - [ ] Trial Object Detection on Street-view Imagery from OSM for object geo estimates
    - [X] Trial Object Detection on user-contributed Imagery from Flickr for object geo estimates
    - [ ] Implement naive object geolocation with image orientation and object coordinate information. @nicoleschnieder / @osullik
    - [ ] Trial depth estimation of objects in imagery
    - [ ] Trial Grid alignment of RSI Imagery 
    - [ ] Trial intersection RSI and ground level object detection to improve geo-estimates of objects

- [ ] Ownership Assignment **PRIORITY 3**
    - [ ] Implement DVBSCAN
    - [ ] Implement Bounding Polygon membership inference
    - [ ] Add probabilites to clustering @nicoleSchneider

- [ ] Concept Mapping **PRIORITY 1**
    - [ ] Fully Implement Arithmetic-Based method
    - [ ] Implement Grid-Based Method
        - [ ] Convert a Location into a Grid of Objects @osullik
        - [ ] Convert a query term into an ordered list @osullik
        - [ ] Integrate Grid-Based Method @osullik
        - [ ] Refactor conceptMapper to accept ordered list of inputs @osullik
    - [ ] Impement Isomorphic Subgraph Method

- [ ] Search **PRIORITY 2**
    - [ ] Implement Search of Object membership
        - [X] Implement Inverted Index search; shortlist objects
        - [ ] Implement probabilities @nicoleschneider
        - [ ] Implement ranking of Results @nicoleschneider
    - [ ] Implement Search of Concept Map
        - [ ] Implement geospatial search (i.e. look up concept map) @osullik
        - [ ] Implement pictoral search interface @nicoleschneider / @osullik
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



