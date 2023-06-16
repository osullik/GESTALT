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
        print("Query Matrix is:\n", queryMatrix)

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

        

        
    #def searchMatrix(self, matrix, toFind: list, northTerm: str, westTerm: str, direction: str):
    def searchMatrix(self, matrix: np.array, searchMatrix:np.array, direction: str):
        '''
        searches a location for the relative relationships between its objects; an approximation to return ANY matching cofiguration of objects matching the search query
        INPUT ARGS:
            matrix  - a numpy matrix / array of arrays of form [[EW List],[EW List]]. i.e. Outer array is the grid from N to S, inner lists are the objects W to E in each row. Defines the Object locations. 
            toFind - list of strings - a list of the objects not yet found by or search. 
            northTerm - string - the known northern most object in the searchTerms
            westTerm - string -the known western most object in the searchTerms
            direction - string with premissible values "northSouth" and "westEast" - defines the orientation of the pruning (northSouth means it prunes Rows, eastWest means it prunes Columns)
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
        print("NORTH:", northTerm, "WEST:", westTerm)
        print("Matrix:\n\n",matrix)

        #baseCase:
            #The last remaining object is in the matrix; or not 

        if len(matrix) == 0:
           return True

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
            
            if direction == "northSouth":                                           #Prune everything north of the north most query term. 
                for i in range(0, len(matrix)):                                         #Walk north to south through the matrix to figure out where to prune from. 
                    for j in range(0,len(matrix[i]),1):
                        print("INDEX NS:", matrix[i][j])
                        if matrix[i][j] == northTerm:
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
                newMatrix = matrix[northMostIndex+1:,:].copy()                        #make a copy of the matrix to recurse on
                
                toFind.remove(northTerm)                                            #update the list of search terms
                newNorth = self.getNewTerms(newMatrix,toFind,"northSouth")
                newWest = westTerm
               
                #if newNorth is not None:                                            #Reurse unless there is an error that won't let us. 
                return self.searchMatrix(newMatrix, toFind, newNorth, newWest, "westEast")
                #else:
                #    return False


            else:
                found = False
                for i in range(0,len(matrix), 1):                                   #Walk west to East through matrix to prune everything west of the west most query term
                    for northToSouth in matrix:
                        if northToSouth[i] == westTerm:
                            print("INDEX EW:", northToSouth[i])
                            westMostIndex = i
                            break
                        else:
                            pass
                    if found==True:
                        break
                if found == False:
                    return False
                newMatrix = matrix[:,westMostIndex+1:].copy()                         #Make a pruned copy to recurse on
               
                toFind.remove(westTerm)                                             #Update the search list
                newWest = self.getNewTerms(newMatrix,toFind,"westEast")
                newNorth = northTerm
                
                #if newWest is not None:                                             #Recurse unless we've run out of search terms in the matrix (i.e. we pruned out all viable options)
                return self.searchMatrix(newMatrix, toFind, newNorth, newWest, "northSouth")
                #else:
                #    return False

        