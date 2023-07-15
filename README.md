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

# GETTING STARTED:

## Repo Structure:

### Papers
 Contains all files relevant to papers, presentations etc. Primarily LaTeX. Included the bibliography file.

### Code
 Contains all code relevant to the solving the problem at hand. Primarily C, little bit of python. Possibly some assembly, depending how unlucky we get. 

### Data 
 Contains TRIVIAL code examples for testing code only. All large data files are stored externally. 

# Initial Setup

## Working with git
check if you have it installed:

      git --version

if you don't then install it (I recommend using homebrew, since we're all of the superior Mac User subspecies)

      brew install git

If you don't have homebrew then install it with:

      /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

Once you have git up and running you want to use the git clone command to get the repo on your local system:

      git clone https://github.com/osullik/GESTALT.git

Once you've got it replicated on your local you can get to work.

You can add single files, multiple files or directories all at once. ( I caution against using the * wildcard operator). for example if we were working on test.py and code.py we might use

      git add code.py
      git add test.py

or, we could also do

      git add code.py test.py

or assuming that they are the only two files in the directory

      git add .

Once you have added the file to the staging area you need to commit it (that is, on your local system, you create an entry in the version control system). I recommend using the -m tag to add a comment to the commit. The comments should be descriptive and meaningful (imagine you, in a panic at 3am before a demo sorting through 100 commit messages that say "updated code" trying to find the one you actually want)

      git commit -m "Added the hello_world unit test to test.py and the hello_world function to code.py. The unit test passes"

To make those changes to the github page itself use:

      git push 

Sometimes you may get an error when running the push command saying that there are changes you don't yet have on your local machine and that you need to reconcile those first. something like this:
   
      ! [rejected]        main -> main (fetch first)
      error: failed to push some refs to 'https://github.com/osullik/GESTALT.git'
      hint: Updates were rejected because the remote contains work that you do
      hint: not have locally. This is usually caused by another repository pushing
      hint: to the same ref. You may want to first integrate the remote changes
      hint: (e.g., 'git pull ...') before pushing again.
      hint: See the 'Note about fast-forwards' in 'git push --help' for details.

This means that someone else (or you) has modified the github repo and it no longer matches yours. To reconcile those you want to use:

      git pull

All going well, it should not have any merge conflict (i.e. two people editing the same file at the same time). If you manage to hit a merge conflict ping me on here and I'll come help you. It might ask you to add a merge message, if so, just use the same comment you used for your git commit.

If in doubt, check the status with:

      git status

My rule of thumb is to commit whenever you have a new unit-test passing, so that you've got it as a working 'checkpoint'. But more often is better than not often enough.

## Getting Jabref [Optional]
For JABREF, you can install it with homebrew using: 

      brew install --cask jabref 
      


# Ways of Work

## Coding

We'll use git to our advantage, but will work through how we want to handle branching, merges etc and document here. 

We should aim for Test-Driven development. In general: 
- identify a problem
- write a test that fails that problem
- write code to solve the problem
- pass the test
- refactor the code to solve the general case. 

If not fully test-driven, we should at least produce a unit test for each function that we write. As we mature we can add regression testing, integration testing etc. 

### Test Driven Development and Using MinUnit testing library.

Writing unit tests is important for ensuring that our code functions as intended. In a mature state, we should aim to write our tests first and then use the tests to guide how we write our code!

I've found a good little library for testing that I'll step you through how to use. This assumes that we're working in a directory *CodeDir* following our common directory structure, that is, with the files: *myCode.py, test.py* 

      CodeDir/
         myCode.py
         test.py
         
## Collaborative Coding

We will use VSCode liveshare to conduct pair programming. 

To install VSCode I recommend (as always) using homebrew with: 

      brew install --cask visual-studio-code

note that specifying --cask indicates to homebrew that this will be a standalone app, usually with a GUI. 

Once installed you can launch VSCODE from the command line with: 

      code 

Once opened, you'll need to install two extensions to VSCODE by navigating to the extensions menu (or use COMD + SHIFT + X) and searching for: 
- Live Share

To share a file, open your file of interest in the editor and look in the bottom left of the VSCode screen. There will be an option to "live share". Click it. You may need to sign in using github. You then have a link you can send to people to start collaborating!

## Data management 

We'll use Google Drive at the link above Initially, with a TO-DO of finding a better version control system for datasets. 

## Task Tracking

**ALEEZA**
-    [ ] Get Github Account
-    [ ] Send kent / nicole Github Handle
-    [ ] Read GETALT Paper
-    [ ] Confirm whether of not you want to do this project

**KENT**
-    [ ] Add Aleeza to Github
-    [ ] Refactor build scripts & Test from scratch
-    [ ] Send docco of Inputs & outputs
-    [ ] Send Django Docco
-    [X] Send resources for getting started with Git.

**NICOLE**
-    [ ] Create Lab Slack
-    [ ] Arrange Meeting with Prof Samet
-    [ ] Arrange Weekly Check-in time
