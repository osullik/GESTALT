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


    def getNewTerms(self, matrix, searchList: list, direction: str):
        '''
        BUG: THIS CODE DOESN'T SEARCH IN THE ORDER REQUIRED BY THE SEARCH TERMS:

        figures out what the northern-most or western-most search terms in the grid are. Called by SearchMatrix each recursive step to figure out what the new North or West most term is. 
        INPUT_ARGS: 
            matrix  - a numpy matrix / array of arrays of form [[EW List],[EW List]]. i.e. Outer array is the grid from N to S, inner lists are the objects W to E in each row. Defines the Object locations. 
            searchList - list - the list of terms still being searched for
            direction - str - defines the axis of the pruning this iteration. 
        PROCESS:
            For either the NS or WE axis, step a row / column at a time and see if one of the search terms is in there
        OUTPUT: 
            westToEast/northToSouth - string - the value of the object being searched for that is either the most northern or most western,

        '''
        northFound = False
        westFound = False

        if direction == "northSouth":
            for northToSouth in matrix:                                             #Walk matrix north to south
                for westToEast in northToSouth:
                    if westToEast in searchList:
                        return westToEast
        else:
            
            for i in range(0, len(matrix[0]),1):                                       #Walk matrix west to east (length of first element)
                for northToSouth in matrix: 
                    if northToSouth[i] in searchList:
                        return northToSouth[i]
        
        return None


        
    def searchMatrix(self, matrix, toFind: list, northTerm: str, westTerm: str, direction: str):
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

        