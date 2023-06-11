# GESTALT/code/queryFlickr.py

# System Imports
import os, sys
import requests
import json
import glob

#Library Imports
import flickrapi
from PIL import Image
from PIL.ExifTags import TAGS
from ultralytics import YOLO
from pathlib import Path

# User File Imports


class PhotoDownloader():
    '''
    Class to hold the objects and methods relating to querying the FlickrAPI for the GESTALT Project
    INPUT ARGS:
        Nil
    FUNCTIONS: 
        -
        -
        -
    OUTPUTS:
        Photos downloaded from the flickrAPI within a given bounding box into the data/photos directory
        A JSON dump of metadata affiliated with those photos into the same directory.
    '''

    def __init__(self):
        #Get API keys from environment variables. (API access can be requested here: https://www.flickr.com/services/api/misc.api_keys.html)
        self._api_key = os.getenv('flickr_key')
        self._api_secret = os.getenv('flickr_secret')
        #Initialize the FlickrAPI object
        self._flickr = flickrapi.FlickrAPI(self._api_key, self._api_secret, format='parsed-json')
    
    #Functions

    def constructURL(self, photo):
        '''
        constructs a URL compatible with the flickrAPI based on a 'photo' returned by the search function
        INPUT ARGS: 
            photo - dictionary - describing a single photo returned from the flickr API
        PROCEDURE:
            given the relevant fields in the photo result passed to the function, construct the url to that photo on flickr. 
        OUTPUT:
            returnTuple - tuple, consisiting of: 
                photoid - string - the unique identifier of the photo in flickr's database
                url - string - the URL to access the photo described in the input parameter
                secret - string - the 'secret' parameter extracted from the input photo description (used to access files on the flickr servers)
        '''     

        server_id = photo['server']
        photo_id = photo['id']
        secret = photo['secret']
        size = "b"

        url = "https://live.staticflickr.com/{serverid}/{id}_{secret}_{sizesuffix}.jpg".format(serverid=server_id, id=photo_id, secret=secret, sizesuffix=size)

        returnTuple = (photo['id'], secret, url)
        return returnTuple


    def getMetadata(self, photoId, photoSecret):
        '''
        constructs a dictionary containing relevant data about the photo being downloaded. 
        INPUT ARGS:
            apiObject - flickrAPI object - the flickr API query tool
            photoID - string - the unique identifier of a photo on flickr's servers
            photoSecret - string - a secret identifier used to access photos on flickr's servers
        PROCESS:
            Create the dictionary to store the results
            Query the API for the EXIF data and the GEO data 
                nb some GPS data is in the EXIF, but we found it to be truncated and inconsistent
            Parse out the relevant fields of the EXIF and GEO data into the dictionary
        OUTPUT:
            photoData - dictionary with keys [photo_bearing_ref, photo_bearing, photo_data, longitude, latitude]    
                nb: some additional keys are added later
                nb: Initialized to NULL - used later in error checking
        '''
    

        photoData = {}                                                  # Initialize dictionary to hold results
        photoData["photo_bearing_ref"] = "NULL"
        photoData["photo_bearing"] = "NULL"
        photoData["photo_date"] = "NULL"
        photoData["longitude"] = "NULL"
        photoData["latitude"] = "NULL"

        try:
            exif = self._flickr.photos.getExif(photo_id=photoId,                  # Query the flickr API for EXIF data
                                        secret=photoSecret)
            
            for ex in exif['photo']['exif']:                                # Parse the relevant EXIF data
                if ex['tag'] == "GPSImgDirection":
                    photoData["photo_bearing"] = (ex['raw']['_content'])
                if ex['tag'] == "GPSImgDirectionRef":
                    photoData["photo_bearing_ref"] = (ex['raw']['_content'])
                if ex['tag'] == "DateTimeOriginal":
                    photoData["photo_date"] = (ex['raw']['_content'])
        except:
            print("Unable to get EXIF for", photoId)
                
        
        geo = self._flickr.photos.geo.getLocation(api_key=self._api_key,            # Query the flickr API for GEO Data
                                                    photo_id=photoId,
                                                    extras="geo,dateTaken")        
                                                                        # Parse the relevant GEO data
        
        photoData["longitude"] = geo['photo']['location']['longitude']
        photoData["latitude"] = geo['photo']['location']['latitude']



        return(photoData)

    def searchBoundingBox(self, LL_LON, LL_LAT, TR_LON, TR_LAT):
        '''
        Searches the flickr API for images within a given bounding box
        INPUT ARGS: 
            LL_LON - string - the longitude for the lower left corner of the bounding box. Will be between -180 and +180
            LL_LAT - string - the latitude for the lower left corner of the bounding box. Will be between -90 and +90
            TR_LON - string - the longitude for the top right corner of the bounding box. Will be between -180 and +180.
            TR_LAT - string - the latitude for the top right corner of the bounding box. Will be between -90 and +90. 
        PROCESS:
            Create the bounding box string and query the API with it
        OUTPUT:
            returnTuple - tuple - contains: 
                photos - dict - the results of the query
                b_box_dict - dict - a dictionary of bounding box values for use by later functions. 
        '''
        
        b_box_dict = {
            "LL_LON":LL_LON,
            "LL_LAT":LL_LAT,
            "TR_LON":TR_LON,
            "TR_LAT":TR_LAT
        }

        b_box = LL_LON+","+LL_LAT+","+TR_LON+","+TR_LAT
        
        print("\n\n==========QUERYING FLICKR==========\n")
        print("b_box:", b_box)

        results = {}

        results[1] = self._flickr.photos.search(bbox=b_box,
                                            safe_search=1,
                                            content_type=1,
                                            has_geo=1,
                                            min_taken_date="2020-01-01 00:00:00")

        print("NUM PAGES", int(results[1]['photos']['pages']))
        for i in range(1,int(results[1]['photos']['pages'])+1):
            results[i] = self._flickr.photos.search(bbox=b_box,
                                            safe_search=1,
                                            content_type=1,
                                            has_geo=1,
                                            min_taken_date="2020-01-01 00:00:00",
                                            page=i)                                        
             
            
        returnTuple = (results, b_box_dict)
        return returnTuple


    def processQueryResults(self, queryResults, outputDirectory):
        '''
        processes the results of a bounding box query to the Flickr API
        INPUT ARGS:
            outputDirectory - string - filepath to the output directory
        PROCESSES: 
            Check the output directory exists
            Step through each photo, get its metadata and save it to file
            Combine all metadata to a JSON and dump to same file

        OUTPUTS: 
            Photo Files Outputted to the outputDirectory
            JSON file with photo Metadata to the Output Directory
        '''


        try:                                                            #Make the output directory
            os.makedirs(outputDirectory)
        except FileExistsError:
            #already Exists
            pass

        imageMetadata = {}                                              #Init the metadata dict
            
        #print("PROCESSING {num_results} images returned from the query".format(num_results=len(queryResults['photos']['photo'])))
        
        #print(photos)
        #print("Photos:", photos.keys())
        #print("Photos Keys:", photos['photos'].keys())

        print("QUERY RESULTS:",queryResults.keys())

        with open("helpme.json", 'w') as out:
            #print("Dumping metadata to", metadataFile )
            json.dump(queryResults, out, indent=4)
            
        for page in queryResults.keys():
            print("page:", page)
            #print("page keys:", page.keys())    
            for photo in photos[page]['photos']['photo']:                         #Loop through each photo in the query results
                
                photo_id, photoSecret, photoURL = self.constructURL(photo)       #construct the URL to get the photos from the search results
                print("EXTRACTING PHOTO", photo_id)
        
                photoFile = requests.get(photoURL)                          #Download and save the photo
                photoFileName = outputDirectory+"/"+photo_id+".jpg"
                
                imageMetadata[photo_id] = self.getMetadata(photo_id, photoSecret)    #Extract the image metadata
                imageMetadata[photo_id]['URL'] = photoURL                       #Add URL to the metadata

                with open(photoFileName, "wb") as out:                          #Save the file to the output directory
                    out.write(photoFile.content)


        metadataFile = outputDirectory+"/metadata.json"                     #Save the metadata to the output directory 
        with open(metadataFile, 'w') as out:
            print("Dumping metadata to", metadataFile )
            json.dump(imageMetadata, out, indent=4)


        
    def detect_tags_from_jpgs_in_directory(self, directory_name, json_filename):

        print("RUNNING YOLO TO DETECT OBJECTS IN COLLECTED PHOTOS\n")
        # Find all jpegs in the directory
        list_of_img_files = glob.glob(os.path.join(directory_name,"*.jpg"))

        # Read in json file
        json_dict = json.load(open(json_filename+".json"))

        # Instantiate model
        model = YOLO("yolov8m.pt")

        # Run images through model and get results
        results = model.predict(list_of_img_files, verbose=False)

        # Check that we got results for every image
        assert len(results) == len(list_of_img_files)

        # Loop over each image
        for idx in range(len(list_of_img_files)):
            file_id = Path(list_of_img_files[idx]).stem  # extract filename without path or extension
            result = results[idx]
            tags = []
            coords = []
            probs = []
            # Loop over each object detected in the image
            for box in result.boxes:
                class_id = result.names[box.cls[0].item()]
                cords = box.xyxy[0].tolist()
                cords = [round(x) for x in cords]
                conf = round(box.conf[0].item(), 2)

                tags.append(class_id)  # object type like person or bench
                coords.append(cords)  # coordinates in the image like [121, 632, 207, 732]
                probs.append(conf)  # confidence score like 0.81
            
            try:
                json_dict[file_id].update({"objects":tags, "coordinates":coords, "probabilities":probs})
            except KeyError:
                print("NOT FOUND:",file_id,"\n Tags:",tags,"\n coords:", coords, "\n probs", probs)

        return json.dumps(json_dict,indent=4)


if __name__ == '__main__':

    #NOTE - THIS CODE ASSUMES IT IS BEING RUN FROM THE GESTALT DIRECTORY. SOMETHING LIKE:
    # python code/queryFlickr.py

    #TODO - Add Arg Parser

    LL_LAT="-31.90009882641578"
    LL_LON="115.96168231510637"
    TR_LAT="-31.77307863942101" 
    TR_LON="116.05029961853784"

    outputDirectory = "data/photos/"+LL_LON+"_"+LL_LAT+"_"+TR_LON+"_"+TR_LAT
    
    downer = PhotoDownloader()
    #photos, b_box_dict = downer.searchBoundingBox(LL_LON, LL_LAT, TR_LON, TR_LAT)
    #downer.processQueryResults(photos,outputDirectory)


    #directory_name = "../data/photos/115.96168231510637_-31.90009882641578_116.05029961853784_-31.77307863942101"
    #json_filename = "../data/photos/115.96168231510637_-31.90009882641578_116.05029961853784_-31.77307863942101/metadata"   
    
    
    json_file = outputDirectory+"/metadata"
    output = downer.detect_tags_from_jpgs_in_directory(outputDirectory, json_file)
    with open(json_file+"_objects.json", "w") as out:
        out.write(output)

