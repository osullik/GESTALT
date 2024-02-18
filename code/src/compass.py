from canvas import Canvas



class COMPASS_OO_Search():
    '''
    The COMPASS_OO_Search is a matrix based method for resolving directional 
    spatial patttern matching queriy Canvases against a database of objects.
    '''
    def __init__(self, database_points):
        # Make db canvas
        # Make db CM
        pass

    def search(self, query_points):
        # Make query Canvas
        # Make query CM
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

