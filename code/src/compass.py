import numpy as np
import pandas as pd

from canvas import Canvas

class ConceptMap():
    def __init__(self, longitudeOrder, latitudeOrder, location_df, location, query=False):
        # Create a grid full of zeros of the dimension numObjects x numObjects
        self.matrix = np.zeros((len(longitudeOrder),len(latitudeOrder)),dtype=object)

        # Using the lat and long lists, work out what index of the matrix the object belong at & add it
        for i in range(0,len(longitudeOrder)):
            j = latitudeOrder.index(longitudeOrder[i])
            self.matrix[j][i] = location_df.loc[int(longitudeOrder[i])]['name']  # J is long, i is lat

        if query:
            self.compute_search_order()

    def compute_Search_order(self, longitudeOrder, latitudeOrder, location_df):
        self.labelledLongOrder = []
        self.labelledLatOrder = []

        # Add to the dict that will store it all 
        for i in range(0, len(longitudeOrder)):
            self.labelledLongOrder.append(location_df.loc[int(longitudeOrder[i])]['name'])
        for i in range(0, len(latitudeOrder)):
            self.labelledLatOrder.append(location_df.loc[int(latitudeOrder[i])]['name'])

        # # Old code will be expecting the following format out of create_CM if it's a query, with the NS and WE orderings
        #     toReturn[location] = (self.matrix, (self.labelledLongOrder, self.labelledLatOrder))


    def prune(self, direction):
        pass




class COMPASS_OO_Search():
    '''
    The COMPASS_OO_Search is a matrix based method for resolving directional 
    spatial patttern matching queriy Canvases against a database of objects.
    '''
    def __init__(self):
        # Make db canvas
        # Make db CM
        pass

    def make_db_CM(self, obj_loc_df):
        loc_names = obj_loc_df['predicted_location'].unique()
        location_dict = dict()
        for loc in loc_names:
            location_dict[loc] = obj_loc_df[obj_loc_df['predicted_location'] == loc].copy()

        locations = list(location_dict.keys())
                          
        self.db_CM_dict = {}

        for location in locations:
            location_df = location_dict[location]

            # Adding 180 is a workaround for crossing hemispheres so we're not dealing with negatives. 
            location_df['longitude'] = (location_df['longitude'].astype(float))+180
            location_df['latitude'] = (location_df['latitude'].astype(float))+180

            location_df.sort_values(by=['longitude'], inplace=True)  # Values higher than 0 are further east

            # For the long and Lat, sort from north to south. TODO: Implement checks for hemispheric differences. 
            # TODO: Remove the triple copying of the dataframes for longitude and latitude below, is unnessecary
            # Case longitude all pos (East Hemisphere)
            longitudeOrder = []
            for idx, row in location_df.iterrows():
                longitudeOrder.append(idx)

            # Case latitide all neg (Southern Hemisphere)
            location_df.sort_values(by=['latitude'], ascending=False, inplace=True)  # The closer to 0, the further North negative latitude is
            latitudeOrder = []
            for idx, row in location_df.iterrows():   
                latitudeOrder.append(idx)

            self.db_CM_dict[location] = ConceptMap(longitudeOrder, latitudeOrder, location_df, location)

    def get_search_order(self, longSortedList:list, latSortedList:list)->list:
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


    def search(self, query_points):
        # Make query Canvas
        # Make query CM
        # Get search order
        # Call RGS
        pass

    def search_cardinally_invariant(self, query_points):
        # Make query Canvas [q]
        # Get all angles from query Canvas
        # Rotate q by each angle and add to list of Canvases
        # Make a CM per Canvas
        # Call RGS on each CM
        pass

    def recursive_grid_search(self, query_CM, prune_dir):
        pass

