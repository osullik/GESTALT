# Code for Concept Mapping in Python

#System Imports
import json 
#Library Imports
import numpy as np
import pandas as pd

#User Imports

class ConceptMapper():
    
    def __init__(self):
        pass 

    def getRelativeLocation(self, locationDict: dict, midpoint:tuple):

        #print("midpoint", midpoint)
        
        quadrantDict = {}
        quadrantDict["northwest"] = []
        quadrantDict["northeast"] = []
        quadrantDict["southwest"] = []
        quadrantDict["southeast"] = []

        #print(locationDict)
        #print("Location Centroid:", "("+str(midpoint[0])+","+str(midpoint[1])+")")
        for obj in locationDict.keys():
            
            #print("Found",locationDict[obj]['name'],"("+locationDict[obj]['latitude']+","+locationDict[obj]['longitude']+")")
            
            if float(locationDict[obj]['latitude']) < midpoint[1]:              #NW is top left cnr
                if float(locationDict[obj]['longitude']) <= midpoint[0]:
                    quadrantDict["southwest"].append(locationDict[obj]['name'])
                else:
                    quadrantDict["southeast"].append(locationDict[obj]['name'])
            else:
                if float(locationDict[obj]['longitude']) <= midpoint[0]:
                    quadrantDict["northwest"].append(locationDict[obj]['name'])
                else:
                    quadrantDict["northeast"].append(locationDict[obj]['name'])

        #for key in quadrantDict.keys():
            #print(key, quadrantDict[key])
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
        NB: This function partially written by ChatGPT in response to the following prompt:
            "write me some python code that will traverse a matrix from the top left corner  
            to the bottom right cornerThat is, round 1 will visit [0,0], round 2 will visit 
            [0,1],[1,0] and [1,1], round 3 will visit [0,2],[1,2],[2,0],[2,1] and [2,2] etc"

        getSearchOrder gets the order to search for the query terms in the location grid
        INPUT ARGS: 
            longList - list that holds the west to east order
        Process:
            If the matrix only has a single value in it, return that value
            Otherwise step incrementally from the top left corner to the bottom right corner
            When a non-zero value is found, append it to the list to be returned
        OURTPUT:
            traversed - list of strings - list of the names of objects to traverse. 

        '''

        traversed = []
        lon = longSortedList.copy()
        lat = latSortedList.copy()

        #print("LONLIST", longSortedList)
        #print("LATLIST", latSortedList)

        assert len(lon) == len(lat), 'Latiude and Longitude lists must be of equal size!'
        #print("SORTING OUT", len(lon), "ITEMS INTO THE CORRECT ORDERT")

        '''
        for i in range(0, len(latSortedList)):
            if i %2 == 0:
                obj = lat.pop(0)
            else:
                obj = lon.pop(0)
            
            if obj not in traversed:
                traversed.append(obj)
        '''
        #Get the search order

        direction = "N"

        while (len(traversed) < len(longSortedList)):

            try:
                if direction == "N":
                    obj = lat.pop(0)
                    #print("POPPING:", obj)
                    if obj not in traversed:
                        traversed.append(obj)
                        #print("APPENDING N", obj)
                        direction = 'W'
            except IndexError as e:
                pass

            try:
                if direction == "W":
                    obj = lon.pop(0)
                    #print("POPPING:", obj)
                    if obj not in traversed and direction=="W":
                        traversed.append(obj)
                        #print("APPENDING W", obj)
                        direction = "N"
            except IndexError as e:
                pass


                
        #print("\tTRAVERSED ORDER:", traversed)
        #print("SUCCESSFULLY SORTED", len(traversed), "ITEMS INTO CORRECT")
        return(traversed)
       
        '''
        #print("\n\n===========================\n")
        searchList = []
        #print("Query Matrix is:")
        #print(queryMatrix)

        if len(queryMatrix) == 1:
            try:
                if len(queryMatrix[0]) ==1:
                    return queryMatrix
            except IndexError:
                pass

        rows = len(queryMatrix)
        cols = len(queryMatrix[0])



        
        # Calculate the total number of rounds required to traverse the matrix
        rounds = rows + cols - 1
        traversed = []

        for r in range(rounds):
            # Determine the row and column indices for the current round

            for i in range(r + 1):
                j = r - i

                # Check if the indices are within the matrix boundaries
                if i < rows and j < cols:
                    if queryMatrix[i][j] != 0:
                         # Append non-zero elements to the list of order we will search them
                        traversed.append(queryMatrix[i][j])
        
        return traversed
        '''
        

        
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
        
        #print("\nITERATING in the ", direction, "direction")
        #print("Search terms", toFind)
       
        #print("Matrix:\n\n",matrix)

        if direction not in ["northToSouth", "westToEast"]:
            exit(direction,"is not a valid search direction")

        #baseCase:
            #The last remaining object is in the matrix; or not 

        #if len(matrix) == 1:
        #    try:
        #        if len(matrix[0]) ==1:
        #            if matrix[0][0] == toFind[0]:
        #                return True
        #            else:
        #                return False
        #    except IndexError:
        #        pass



        if len(toFind) == 1:                                                        #Base Case; exhaustive search of pruned matrix. 
            #print("Base Case")
            for northToSouth in matrix:
                 for westToEast in northToSouth:
                     if str(westToEast) == str(toFind[0]):
                         #print("exhaustive search true, found", toFind[0])
                         return True
            return False
        else:
            #print("Not base case")
            found = False
            
            if direction == "northToSouth":                                           #Prune everything north of the north most query term. 
                #print("going N to S looking for", toFind[0])
                for i in range(0, len(matrix)):                                         #Walk north to south through the matrix to figure out where to prune from. 
                    #print("got to row", i)
                    for j in range(0,len(matrix[i])):
                        try:
                            #print('got to column', j)
                            #print("TYPES:", type(matrix[i][j]),type(toFind))
                            if str(matrix[i][j]) == str(toFind[0]):
                                #print("pruned")
                                #print("looking for", toFind[0],"found", matrix[i][j], "at", i,j )
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
                #print(northMostIndex)
                newMatrix = matrix[northMostIndex:,:].copy()                        #make a copy of the matrix to recurse on
                #print("NEW MATRIX")
                #print(newMatrix)
                toFind.pop(0)                                            #update the list of search terms               
                #print("RECURSE NS to WE")

                recurse_found= self.searchMatrix(newMatrix, toFind, "westToEast")
                if recurse_found == False:
                    return False
                else:
                    return True
            
                #else:
                #    return False


            else:
                #print("going W to E", "looking for ", toFind[0])
                found = False
                for i in range(0,len(matrix)):                                   #Walk west to East through matrix to prune everything west of the west most query term
                    #print("got to row", i)
                    for j in range(0, len(matrix)):
                       #print("got to column",j)
                        try:
                            if str(matrix[j][i]) == str(toFind[0]):
                                #print("pruned")
                            #print("looking for", toFind[0],"found", matrix[i][j], "at", i,j  )
                                #print("INDEX EW:", matrix[j][i])
                                westMostIndex = i
                                found=True
                                break
                        except IndexError:
                            return False
                    if found==True:
                        break

                    
                if found == False:
                    #print("returning false")
                    return False
                newMatrix = matrix[:,westMostIndex:].copy()                         #Make a pruned copy to recurse on
               
                toFind.pop(0)                                             #Update the search list                
                #print("RECURSE WE to NS")
                recurse_found = self.searchMatrix(newMatrix, toFind, "northToSouth")
                if recurse_found == False:
                    return False
                else:
                    return True
                #else:
                #    return False

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
        
        #print("DATAFRAME WHEN CREATE CONCEPT MAP FIRST GETS IT")
        #print(sourceData_df)
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
            longitude_df = location_df.copy()
            latitude_df = location_df.copy()

            location_df['longitude'] = (location_df['longitude'].astype(float))+180
            location_df['latitude'] = (location_df['latitude'].astype(float))+180

            longitude_df.sort_values(by=['longitude'], 
                                    #ascending=False,
                                    inplace=True)        #Values higher than 0 are further east
            

            # For the long and Lat, sort from north to south. TODO: Implement checks for hemispheric differences. 
        

            #Case longitude all pos (East Hemisphere)
            longitudeOrder = []
            for idx, row in longitude_df.iterrows():
                longitudeOrder.append(idx)
                #print(location,row['name'],row["longitude"])

            #Case latitide all neg (Southern Hemisphere)
            latitude_df.sort_values(by=['latitude'], 
                                    ascending=False, 
                                    inplace=True)           # The closer to 0, the further North negative latitude is
            latitudeOrder = []
            for idx, row in latitude_df.iterrows():   
                latitudeOrder.append(idx)
                #print(location,row['name'],row["latitude"])

            #print("LONGITUDE ORDER ON FIRST SORT")
            #print(longitudeOrder)
            #print("LATITUDE ORDER ON FIRST SORT")
            #print(latitudeOrder)
            

            #Create a grid full of zeros of the dimension numObjects x numObjects
            gridToReturn = np.zeros((len(longitudeOrder),len(latitudeOrder)),dtype=object)

            #Using the lat and long lists, work out what index of the matrix the object belong at & add it
            for i in range(0,len(longitudeOrder)):
                j = latitudeOrder.index(longitudeOrder[i])
                gridToReturn[j][i] = location_df.loc[int(longitudeOrder[i])]['name']    #J is long, i is lat
                #print("long:",i,"lat",j)

            #print("GRID TO RETURN ON FIRST CREATION")
            #print(gridToReturn)

            #Show your work
            #print(location)
            #print(location_dict[location])
            #print(gridToReturn)
            labelledLongOrder = []
            labelledLatOrder = []
            #Add to the dict that will store it all 

            for i in range(0, len(longitudeOrder)):
                labelledLongOrder.append(longitude_df.loc[int(longitudeOrder[i])]['name'])
            for i in range(0, len(latitudeOrder)):
                labelledLatOrder.append(latitude_df.loc[int(latitudeOrder[i])]['name'])

            #print("LABELLED LONGITUDE ORDER ON FIRST SORT")
            #print(labelledLongOrder)
            #print("LABELLED LATITUDE ORDER ON FIRST SORT")
            #print(labelledLatOrder)

            if cm_type == "query":
                toReturn[location] = (gridToReturn, (labelledLongOrder, labelledLatOrder))
            else:
                toReturn[location] = gridToReturn

        return toReturn
    
    def createLocationCentricDict(self,inputFile:str, locationsFile:str, input_df=None):

        if inputFile is not None: 
            sourceData_df = pd.read_csv(inputFile)[['name','longitude','latitude','predicted_location']]
        elif input_df is not None:
            sourceData_df = input_df
        else:
            exit("Unable to find dataframe. Please check your CSV / Dataframe and Try again")

        conceptDict = {}
        for idx, row in sourceData_df.iterrows():
            #print(row)
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

        with open(locationsFile, 'r') as inFile:
            locationsDict = json.load(inFile)
        
        flatLocations = self.flattenLocationDict(locationsDict)
        #print(flatLocations)
        for concept in conceptDict.keys():
            #print("CONCEPT", concept)
            #print(conc[concept])
            #print(conceptDict[concept])
            #print(flatLocations[concept]['longitude'])
            #print(flatLocations[concept]['latitude'])
            try:
                relativeLocationsDict[(concept)] = self.getRelativeLocation(conceptDict[concept],
                                                                      ((flatLocations[concept]["longitude"]),
                                                                        (flatLocations[concept]["latitude"])))
            except KeyError:
                pass
            #print(relativeLocationsDict)
        return relativeLocationsDict
    
    def flattenLocationDict(self, locationDict:dict) -> dict:
        flattenedDict = {}
        for locID in locationDict:
            #print("LOC ID", locID)
            #print('name', locationDict[locID]["name"])
            try:
                flattenedDict[locationDict[locID]['name']]["name"] = locationDict[locID]['name']
            except KeyError:
                flattenedDict[locationDict[locID]['name']] = {}
                flattenedDict[locationDict[locID]['name']]["name"] = locationDict[locID]['name']
            flattenedDict[locationDict[locID]['name']]["latitude"] = locationDict[locID]['latitude']
            flattenedDict[locationDict[locID]['name']]["longitude"] = locationDict[locID]['longitude']
        #print(flattenedDict)
        return(flattenedDict)



