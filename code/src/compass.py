import numpy as np
import pandas as pd
from collections import defaultdict 
import gc
import enum

from canvas import Canvas

class Direction(enum.Enum):
    North = 1
    West = 2

    def flip(self):
        if self is Direction.North:
            return Direction.West
        if self is Direction.West:
            return Direction.North

class ConceptMap():
    def __init__(self, longitudeOrder, latitudeOrder, location_df):
        # Create a grid full of zeros of the dimension numObjects x numObjects
        self.matrix = np.zeros((len(longitudeOrder),len(latitudeOrder)),dtype=object)

        # Using the lat and long lists, work out what index of the matrix the object belong at & add it
        for i in range(0,len(longitudeOrder)):
            j = latitudeOrder.index(longitudeOrder[i])
            self.matrix[j][i] = location_df.loc[int(longitudeOrder[i])]['name']  # J is long, i is lat

    def search(self, toFind:list):
        return self.search_matrix(self.matrix.copy(), toFind)

    # TODO: Direction enum with flip fxn; collapse RGS if/elso with aux fxn; prune fxn w/o copy
    def search_matrix(self, matrix, toFind:list, direction:str="northToSouth"):
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
        assert direction in ["northToSouth", "westToEast"], f'invalid search direction: {direction}'

        if len(toFind) == 1:   # Base Case; exhaustive search of pruned matrix. 
            return str(toFind[0]) in matrix
        else:
            found = False

            if direction == "northToSouth":  # Prune everything north of the north most query term. 
                for i in range(0, len(matrix)):  # Walk north to south through the matrix to figure out where to prune from. 
                    for j in range(0,len(matrix[i])):
                        try:
                            if str(matrix[i][j]) == str(toFind[0]):
                                found = True
                                northMostIndex = i
                                break
                        except IndexError:
                            return False
                    if found:
                        break

                if not found:
                    return False

                newMatrix = matrix[northMostIndex:,:].copy()  # make a copy of the matrix to recurse on
                del matrix  # Get rid of old one to preserve memory
                gc.collect()                
                toFind.pop(0)  # update the list of search terms               

                return self.search_matrix(newMatrix, toFind, "westToEast")
            else:  # direction = "westToEast"     
                found = False
                for i in range(0,len(matrix)):  # Walk west to East through matrix to prune everything west of the west most query term
                    for j in range(0, len(matrix)):
                        try:
                            if str(matrix[j][i]) == str(toFind[0]):
                                westMostIndex = i
                                found=True
                                break
                        except IndexError:
                            return False
                    if found:
                        break

                if not found:
                    return False

                newMatrix = matrix[:,westMostIndex:].copy()  # Make a pruned copy to recurse on
                del matrix  # Get rid of old one to preserve memory
                gc.collect()
                toFind.pop(0)  # Update the search list   

                return self.search_matrix(newMatrix, toFind, "northToSouth")





class COMPASS_OO_Search():
    '''
    The COMPASS_OO_Search is a matrix based method for resolving directional 
    spatial patttern matching queriy Canvases against a database of objects.
    '''
    def __init__(self, obj_loc_df):  # Should take db canvas not df
        self.make_db_CM(obj_loc_df)


    def make_db_CM(self, obj_loc_df):
        loc_names = obj_loc_df['predicted_location'].unique()
        location_dict = dict()
        for loc in loc_names:
            location_dict[loc] = obj_loc_df[obj_loc_df['predicted_location'] == loc].copy()

        locations = list(location_dict.keys())
                          
        self.db_CM_dict = {}
        self.long_sorted_objs_by_loc = defaultdict(list)
        self.lat_sorted_objs_by_loc = defaultdict(list)

        for location in locations:
            location_df = location_dict[location]

            # Adding 180 is a workaround for crossing hemispheres so we're not dealing with negatives. 
            location_df['longitude'] = (location_df['longitude'].astype(float))+180
            location_df['latitude'] = (location_df['latitude'].astype(float))+180

            # For the long and Lat, sort from north to south. TODO: Implement checks for hemispheric differences. 
            # Case longitude all pos (East Hemisphere)
            location_df.sort_values(by=['longitude'], inplace=True)  # Values higher than 0 are further east
            for idx, row in location_df.iterrows():
                self.long_sorted_objs_by_loc[location].append(idx)

            # Case latitide all neg (Southern Hemisphere)
            location_df.sort_values(by=['latitude'], ascending=False, inplace=True)  # The closer to 0, the further North negative latitude is
            for idx, row in location_df.iterrows():   
                self.lat_sorted_objs_by_loc[location].append(idx)

            self.db_CM_dict[location] = ConceptMap(self.long_sorted_objs_by_loc[location], self.lat_sorted_objs_by_loc[location], location_df)


    def search(self, query_canvas):
        searchlist = self.get_search_order(query_canvas.get_point_names_x_sorted(), query_canvas.get_point_names_y_sorted())
        return self.search_CM(searchlist)


    def search_CM(self, searchlist):
        matching_locs = []

        for loc in self.db_CM_dict:            
            if self.db_CM_dict[loc].search(searchlist):  # Call CM search
                #print(loc, ": ", self.db_CM_dict[loc].matrix)
                matching_locs.append(loc)

        return matching_locs     


    def search_cardinally_invariant(self, query_points):
        # Make query Canvas [q]
        # Get all angles from query Canvas
        # Rotate q by each angle and add to list of Canvases
        # Make a CM per Canvas
        # Call RGS on each CM
        pass


    def get_search_order(self, longSortedList, latSortedList)->list:
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
   
        direction = "N"  # Starting from the north
        while (len(traversed) < len(longSortedList)):
            try:
                if direction == "N":
                    obj = lat.pop(0)
                    if obj not in traversed:
                        traversed.append(obj)
                        direction = 'W'
            except IndexError as e:       
                pass  # Handle case of trying to pop empty list
            try:
                if direction == "W":
                    obj = lon.pop(0)
                    if obj not in traversed and direction=="W":
                        traversed.append(obj)
                        direction = "N"
            except IndexError as e:
                pass  # Handle case of trying to pop empty list
 
        return(traversed)



    
