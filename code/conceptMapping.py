# Code for Concept Mapping in Python
# Author: Kent O'Sullivan - osullik@umd.edu // github.com/osullik

#System Imports
import json 
import gc
#Library Imports
import numpy as np
import pandas as pd

#User Imports

class ConceptMapper():
    
    def __init__(self):
        pass 

    def getRelativeLocation(self, locationDict: dict, midpoint:tuple):
        '''
        PURPOSE:
            sort objects into NW, NE, SW and SE quadrants based on their relative position
            to a given midpoint. 
        INPUT ARGS:
            locationDict - dict - a dictionary of objects, their names, latitudes and longitudes
            midpoint - tuple of floats - the centre of the location that all of the 
        PROCESS:
            Iterate through each object 
            Detemine which quadrant it is in relative to the location centroid
                Convention: when on a border, we assign it to the north/west side of the border
                    as appropriate. 
        OUTPUT:
            quadrantDict - dict - of form {"northwest":[obj1,obj2...objn],"northeast":[],"southwest":[],"southeast":[] }
        '''
        
        quadrantDict = {}
        quadrantDict["northwest"] = []
        quadrantDict["northeast"] = []
        quadrantDict["southwest"] = []
        quadrantDict["southeast"] = []

        for obj in locationDict.keys():
                        
            if float(locationDict[obj]['latitude']) < midpoint[1]:              #NW is top left cnr
                if float(locationDict[obj]['longitude']) <= midpoint[0]:
                    quadrantDict["southwest"].append(locationDict[obj]['name'])
                    continue
                else:
                    quadrantDict["southeast"].append(locationDict[obj]['name'])
                    continue
            else:
                if float(locationDict[obj]['longitude']) <= midpoint[0]:
                    quadrantDict["northwest"].append(locationDict[obj]['name'])
                    continue
                else:
                    quadrantDict["northeast"].append(locationDict[obj]['name'])
                    continue

        return quadrantDict




    def checkRelativeLocation(self, locationDict: dict, ew_relation: str, ns_relation: str, searchTerm: str) -> bool:
        '''
        A function that is designed to query each object's position relative to the location they belong to; assuming that the location is at the (Long,Lat), NOT nessecrily that it is the centroid object cluster)
        INPUT ARGS:
            locationDict    - dictionary of form {northwest:[objects],northeast[objects],southwest[objects],southeast[objects]} - lists which quadrant the objects are in assuming the location is the origin. 
            ew_relation     - string; valid values are: "east_of" and "west_of" and None, used to determine the relationship of the object in question to the location. 
            ns_relation     - string; valid values are: "north_of" and "south_of" and None, used to determine the relationship of the object in question to the location. 
            searchTerm      - string - the name of an object to search for in relation to the location. 
        PROCESS:
            check if the object appears in each specified relation, return true if it does and false otherwise 
            if one of the dimensions is None, we treat is as an OR relation. I.e. NS = north_of" and EW = None means it could be NE or NW of the location. 
        OUTPUT: 
            True if the object is found in the specified quadrant(s) relative to the house; false otherwise. 
        '''
        
        allConditionsSatisfied = False
        eastWestSatisfied = False
        northSouthSatisfied = False
        

        if ns_relation == "north_of" and ew_relation == None:
            if searchTerm in locationDict["northeast"] or searchTerm in locationDict["northwest"]:
                return True
        elif ns_relation == "north_of" and ew_relation == "west_of":
            if searchTerm in locationDict["northwest"]:
                return True
        elif ns_relation == "north_of" and ew_relation == "east_of":
            if searchTerm in locationDict["northeast"]:
                return True
            
        elif ns_relation == "south_of" and ew_relation == None:
            if searchTerm in locationDict["southeast"] or searchTerm in locationDict["southwest"]:
                return True
            
        elif ns_relation == "south_of" and ew_relation == "west_of":
            if searchTerm in locationDict["southwest"]:
                return True
        
        elif ns_relation == "south_of" and ew_relation == "east_of":
            if searchTerm in locationDict["southeast"]:
                return True
            
        elif ns_relation == None and ew_relation == "west_of":
            if searchTerm in locationDict["southwest"] or searchTerm in locationDict["northwest"]:
                return True
        
        elif ns_relation == None and ew_relation == "east_of":
            if searchTerm in locationDict["southeast"] or searchTerm in locationDict["northeast"]:
                return True
            
        else:
            return False


    def getSearchOrder(self, longSortedList:list, latSortedList:list):
        '''
        PURPOSE:
            getSearchOrder gets the order to search for the query terms in the location grid
        INPUT ARGS: 
            longList - list that holds the west to east order
            latList -  list that holds the north to south order
        PROCESS:
            Starting from the north, append the north-most and west-most values each iteration
            until all items have been added. 
        OURTPUT:
            traversed - list of strings - list of the names of objects to traverse. 

        '''

        traversed = []
        lon = longSortedList.copy()
        lat = latSortedList.copy()

        assert len(lon) == len(lat), 'Latiude and Longitude lists must be of equal size!'
   
    
        direction = "N"                                 #Starting from the north
        while (len(traversed) < len(longSortedList)):

            try:
                if direction == "N":
                    obj = lat.pop(0)
                    if obj not in traversed:
                        traversed.append(obj)
                        direction = 'W'
            except IndexError as e:
                 #Handle case of trying to pop empty list            
                pass

            try:
                if direction == "W":
                    obj = lon.pop(0)
                    if obj not in traversed and direction=="W":
                        traversed.append(obj)
                        direction = "N"
            except IndexError as e:
                 #Handle case of trying to pop empty list
                pass
 
        return(traversed)
       

        

        
    def searchMatrix(self, matrix, toFind: list, direction:str="northToSouth"):
    #def searchMatrix(self, matrix: np.array, searchMatrix:np.array, direction: str):
        '''
        searches a location for the relative relationships between its objects; an approximation to return ANY matching cofiguration of objects matching the search query
        INPUT ARGS:
            matrix  - a numpy matrix / array of arrays of form [[EW List],[EW List]]. i.e. Outer array is the grid from N to S, inner lists are the objects W to E in each row. Defines the Object locations. 
            toFind - list of strings - a list of the objects ordered by "Most north, most west, most north, most west etc...
            direction - string with premissible values "northToSouth" and "westToEast" - defines the orientation of the pruning (northSouth means it prunes Rows, eastWest means it prunes Columns)
        PROCESS:
            Recursively prunes the searchSpace of the matrix to determine if a matching collection of objects exists:
            BASE CASE: 
                SUCCESS: when there is one object remaining in the search list, and it is in the pruned matrix
                FAIL: when there is one object remaining in the search list and it is NOT in the pruned matrix
            ELSE: 
                Prune all rows >= (north of) the most northern term in our search set & remove it from the list of terms to find
                Recurse on the matrix and prune all rows <= (west of) the western most term in our search set and remove it from list of terms to find. 
                Recurse
        OUTPUTS:
            True - if there is a match to the query object configuration
            False - if there is no match,. 
        '''

        if direction not in ["northToSouth", "westToEast"]:                         #Check the direction
            exit(direction,"is not a valid search direction")

        if len(toFind) == 1:                                                        #Base Case; exhaustive search of pruned matrix. 
            for northToSouth in matrix:
                 for westToEast in northToSouth:
                     if str(westToEast) == str(toFind[0]):
                         return True
            return False
        else:
            found = False
            
            #Case that we're walking north to south through the matrix
            if direction == "northToSouth":                                           #Prune everything north of the north most query term. 
                for i in range(0, len(matrix)):                                         #Walk north to south through the matrix to figure out where to prune from. 
                    for j in range(0,len(matrix[i])):
                        try:
                            if str(matrix[i][j]) == str(toFind[0]):
                                found = True
                                northMostIndex = i
                                break
                            else:
                                pass
                        except IndexError:
                            return False
                    if found==True:
                        break

                
                
                if found ==False:
                    return False
                newMatrix = matrix[northMostIndex:,:].copy()                        #make a copy of the matrix to recurse on
                del matrix                                     #Get rid of old one to preserve memory
                gc.collect()                
                toFind.pop(0)                                            #update the list of search terms               

                recurse_found= self.searchMatrix(newMatrix, toFind, "westToEast")
                if recurse_found == False:
                    return False
                else:
                    return True

            #Case where we're walking west to East through the Matrix
            else:       

                found = False
                for i in range(0,len(matrix)):                                   #Walk west to East through matrix to prune everything west of the west most query term
                    for j in range(0, len(matrix)):
                        try:
                            if str(matrix[j][i]) == str(toFind[0]):
                                westMostIndex = i
                                found=True
                                break
                        except IndexError:
                            return False
                    if found==True:
                        break

                    
                if found == False:
                    return False
                newMatrix = matrix[:,westMostIndex:].copy()                         #Make a pruned copy to recurse on
                del matrix                                     #Get rid of old one to preserve memory
                gc.collect()
                toFind.pop(0)                                             #Update the search list                
                recurse_found = self.searchMatrix(newMatrix, toFind, "northToSouth")
                if recurse_found == False:
                    return False
                else:
                    return True

    def createConceptMap(self,inputFile:str=None,input_df=None,cm_type:str="location"):
        '''
        Function to create the 'concept map' of relative object positions in a grid, for querying by the concept mapper
        INPUT ARGS:
            inputFile - string - the path to a file containing the object assignments to be used to create the grids. 
            cm_type - string - either 'location' or 'query'. Informs what to return. 
        PROCESS: 
            # Get a data DF? for a location that contains its objects, their names, their lats and their longs
            # sort into two lists, one by long (west to east), one by lat, North to South
            # use the indexes of objects construct a grid, inserting their name as Grid[longIndex][latIndex]
            # Returns the grid 
        OUTPUT:
            toReturn - grid of Matricies (numpy array of numpy object arrays, 
                        with 0s representing empty space and object Names reprsenting their object type)
                        if it's for a location, just return the concept map, else

            toReturn - a tuple of form (matrix map as described above, ([NorthSouth order], [WestEast order])) 
                        where NorthSouth order is a list of all points from north to south, and westeast is
                        a list of all points from west to east. In the case of a query these are used to 
                        generate the searchOrder for the recursive grid search
        '''

        #Read in File
        if inputFile is not None: 
            sourceData_df = pd.read_csv(inputFile)[['name','longitude','latitude','predicted_location']]
        elif input_df is not None:
            sourceData_df = input_df
        else:
            exit("Unable to find dataframe. Please check your CSV / Dataframe and Try again")
        
        #Prepare vars
        loc_names = sourceData_df['predicted_location'].unique()
        location_dict = dict()
        
        #Create dict of dataframes, indexed on their location
        for loc in loc_names:
            location_dict[loc] = sourceData_df[sourceData_df['predicted_location'] == loc]

        locations = list(location_dict.keys())

        toReturn = {}                                   # Dict to hold the concept maps for each location

        
        for location in locations:
            location_df = location_dict[location]
            #longitude_df = location_df.copy()
            #latitude_df = location_df.copy()

            #Adding 180 is a workaround for crossing hemispheres so we're not dealing with negatives. 
            location_df['longitude'] = (location_df['longitude'].astype(float))+180
            location_df['latitude'] = (location_df['latitude'].astype(float))+180

            location_df.sort_values(by=['longitude'], 
                                    #ascending=False,
                                    inplace=True)        #Values higher than 0 are further east
            

            # For the long and Lat, sort from north to south. TODO: Implement checks for hemispheric differences. 
        
            #TODO: Remove the triple copying of the dataframes for longitude and latitude below, is unnessecary
            #Case longitude all pos (East Hemisphere)
            longitudeOrder = []
            for idx, row in location_df.iterrows():
                longitudeOrder.append(idx)

            #Case latitide all neg (Southern Hemisphere)
            location_df.sort_values(by=['latitude'], 
                                    ascending=False, 
                                    inplace=True)           # The closer to 0, the further North negative latitude is
            latitudeOrder = []
            for idx, row in location_df.iterrows():   
                latitudeOrder.append(idx)


            #Create a grid full of zeros of the dimension numObjects x numObjects
            gridToReturn = np.zeros((len(longitudeOrder),len(latitudeOrder)),dtype=object)

            #Using the lat and long lists, work out what index of the matrix the object belong at & add it
            for i in range(0,len(longitudeOrder)):
                j = latitudeOrder.index(longitudeOrder[i])
                gridToReturn[j][i] = location_df.loc[int(longitudeOrder[i])]['name']    #J is long, i is lat


            labelledLongOrder = []
            labelledLatOrder = []
            #Add to the dict that will store it all 

            for i in range(0, len(longitudeOrder)):
                labelledLongOrder.append(location_df.loc[int(longitudeOrder[i])]['name'])
            for i in range(0, len(latitudeOrder)):
                labelledLatOrder.append(location_df.loc[int(latitudeOrder[i])]['name'])

            #Return the appropriate shape based on input. If it's a query, we need the NS and WE orderings
            #To execute the recursive grid search. 
            if cm_type == "query":
                toReturn[location] = (gridToReturn, (labelledLongOrder, labelledLatOrder))
            else:
                toReturn[location] = gridToReturn

        return toReturn
    
    def createLocationCentricDict(self,inputFile:str, locationsFile:str, input_df=None):
        '''
        PURPOSE: 
            Creates a dictionary of the counts of each type of object in a given location by NW, NW, SW, SE quadrant
        INPUT ARGS:
            inputFile - string - filePath to load the objects to process from. Optional, can also pass from memory, just
                set inputFile to None when invoking. 
            locationsFile - string - filepath to load the location centroids from. 
            input_df - pandas DataFrame - alternative to loading from file
        PROCESS:
            Get the objects to sort into quadrants
            Flatten them into the dictionary format that the sorting function is expecting
            Get the location centroids to sort around from file
            Pass to the sort & collect the output
        OUTPUT:
            relativeLocationsDict, Dict of form {<location_name>:{NW:[obj1,obj2]},{NE:[]},{SW:[]},{SE:[]}}
            
        '''

        #Allow input from file or from a dataframe already in memory
        if inputFile is not None: 
            sourceData_df = pd.read_csv(inputFile)[['name','longitude','latitude','predicted_location']]
        elif input_df is not None:
            sourceData_df = input_df
        else:
            exit("Unable to find dataframe. Please check your CSV / Dataframe and Try again")

        #Create a dictionatry to hold the name, lat and long for each object sorted by location.
        conceptDict = {}
        for idx, row in sourceData_df.iterrows():
            try:
                conceptDict[row['predicted_location']][idx] = {}
            except KeyError:
                conceptDict[row['predicted_location']] = {}
                conceptDict[row['predicted_location']][idx] = {}
            try:
                conceptDict[row['predicted_location']][idx]['name'] = row['name']
            except KeyError:
                conceptDict[row['predicted_location']][idx] = row['name']
                conceptDict[row['predicted_location']][idx]['name'] = row['name']


            conceptDict[row['predicted_location']][idx]['name'] = row['name']
            conceptDict[row['predicted_location']][idx]['longitude'] = row['longitude']
            conceptDict[row['predicted_location']][idx]['latitude'] = row['latitude']

        relativeLocationsDict = {}

        #Get the locations from file
        with open(locationsFile, 'r') as inFile:
            locationsDict = json.load(inFile)
        
        flatLocations = self.flattenLocationDict(locationsDict)

        for concept in conceptDict.keys():
            try:
                relativeLocationsDict[(concept)] = self.getRelativeLocation(conceptDict[concept],
                                                                      ((flatLocations[concept]["longitude"]),
                                                                        (flatLocations[concept]["latitude"])))
            except KeyError:
                pass
        return relativeLocationsDict
    
    def flattenLocationDict(self, locationDict:dict) -> dict:
        '''
        PURPOSE:
            take a nested locationDict and flatten it into a format that can be read by the searching and
            sorting functions
        INPUT ARGS:
            locationDict - dict - A dictionary of locations of the form {<locationID>:{'name':<name>, "longitude":<longitude>. "latitude":<latitude>}}
        PROCESS:
            Load the dict and copy it into another dict in a slightly different format. 
        OUTPUT:
            flattenedDict - dict - of the form {<location_name>:{}"longitude":<longitude>,"latitude":<latitude>}
        '''
        flattenedDict = {}
        for locID in locationDict:

            try:
                flattenedDict[locationDict[locID]['name']]["name"] = locationDict[locID]['name']
            except KeyError:
                #Create the dictionary entry the first time.
                flattenedDict[locationDict[locID]['name']] = {}
                flattenedDict[locationDict[locID]['name']]["name"] = locationDict[locID]['name']

            #Generate the flat representation.
            flattenedDict[locationDict[locID]['name']]["latitude"] = locationDict[locID]['latitude']
            flattenedDict[locationDict[locID]['name']]["longitude"] = locationDict[locID]['longitude']
        return(flattenedDict)



