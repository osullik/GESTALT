# Code for Concept Mapping in Python

#System Imports

#Library Imports
import numpy as np

#User Imports

class ConceptMapper():
    
    def __init__(self):
        pass 

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


    def getSearchOrder(self, queryMatrix):
        '''
        NB: This function partially written by ChatGPT in response to the following prompt:
            "write me some python code that will traverse a matrix from the top left corner  
            to the bottom right cornerThat is, round 1 will visit [0,0], round 2 will visit 
            [0,1],[1,0] and [1,1], round 3 will visit [0,2],[1,2],[2,0],[2,1] and [2,2] etc"

        getSearchOrder gets the order to search for the query terms in the location grid
        INPUT ARGS: 
            queryMatrix - list of lists  of form [[0,"A"]["B",0]] for a 2x2 matrix with A in the
                top right and B in the bottom left. Blank spaces are held by zeroes.
        Process:
            If the matrix only has a single value in it, return that value
            Otherwise step incrementally from the top left corner to the bottom right corner
            When a non-zero value is found, append it to the list to be returned
        OURTPUT:
            traversed - list of strings - list of the names of objects to traverse. 

        '''
       
        print("\n\n===========================\n")
        searchList = []
        print("Query Matrix is:")
        print(queryMatrix)

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
        
        print("\nITERATING in the ", direction, "direction")
        print("Search terms", toFind)
        print("Matrix:\n\n",matrix)

        if direction not in ["northToSouth", "westToEast"]:
            exit(direction,"is not a valid search direction")

        #baseCase:
            #The last remaining object is in the matrix; or not 

        if len(matrix) == 1:
            try:
                if len(matrix[0]) ==1:
                    if matrix[0][0] == toFind[0]:
                        return True
                    else:
                        return False
            except IndexError:
                pass

        if len(toFind) == 1:                                                        #Base Case; exhaustive search of pruned matrix. 
            print("Base Case")
            for northToSouth in matrix:
                 for westToEast in northToSouth:
                     if westToEast == toFind[0]:
                         return True
            return False
        else:
            print("Not base case")
            found = False
            
            if direction == "northToSouth":                                           #Prune everything north of the north most query term. 
                #print("going N to S looking for", toFind[0])
                for i in range(0, len(matrix)):                                         #Walk north to south through the matrix to figure out where to prune from. 
                    #print("got to row", i)
                    for j in range(0,len(matrix[i]),1):
                        #print('got to column', j)
                        if matrix[i][j] == toFind[0]:
                            found = True
                            northMostIndex = i
                            break
                        else:
                            pass
                    if found==True:
                        break
                
                if found ==False:
                    return False
                #print(northMostIndex)
                newMatrix = matrix[northMostIndex:,:].copy()                        #make a copy of the matrix to recurse on
                
                toFind.pop(0)                                            #update the list of search terms               
                return self.searchMatrix(newMatrix, toFind, "westToEast")
                #else:
                #    return False


            else:
                print("going W to E", "looking for ", toFind[0])
                found = False
                for i in range(0,len(matrix)):                                   #Walk west to East through matrix to prune everything west of the west most query term
                    #print("got to row", i)
                    for j in range(0, len(matrix)):
                       #print("got to column",j)
                        if matrix[j][i] == toFind[0]:
                            #print("INDEX EW:", matrix[j][i])
                            westMostIndex = i
                            found=True
                            break
                    if found==True:
                        break
                    
                if found == False:
                    #print("returning false")
                    return False
                newMatrix = matrix[:,westMostIndex:].copy()                         #Make a pruned copy to recurse on
               
                toFind.pop(0)                                             #Update the search list                
                return self.searchMatrix(newMatrix, toFind, "northToSouth")
                #else:
                #    return False

    def createConceptMap():

        # Get a data structure (DF?) for a location that contains its objects, their names, their lats and their longs
        # sort into two lists, one by long (west to east), one by lat, North to South
        # use the indexes of objects construct a grid, inserting their name as Grid[longIndex][latIndex]
        # Returns the grid 

        pass


        