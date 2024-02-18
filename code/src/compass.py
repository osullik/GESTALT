import numpy as np

from canvas import Canvas

class ConceptMap():
    def __init__(self, points):
        # Create point grid
        pass

    def prune(self, direction):
        pass




class COMPASS_OO_Search():
    '''
    The COMPASS_OO_Search is a matrix based method for resolving directional 
    spatial patttern matching queriy Canvases against a database of objects.
    '''
    def __init__(self, database_points):
        # Make db canvas
        # Make db CM
        pass

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

