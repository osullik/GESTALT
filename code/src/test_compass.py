import pytest
import sys
import os
import pickle
import numpy as np
import pandas as pd

from canvas import Canvas
from compass import Direction
from compass import ConceptMap
from compass import COMPASS_OO_Search

class TestDirection:
    def test_dir_equality(self):
        assert Direction.North != Direction.West

    def test_dir_flip(self):
        assert Direction.North.flip() == Direction.West
        assert Direction.West.flip() == Direction.North

class TestConceptMap:
    @pytest.fixture
    def setup_CM(self):
        data_path = os.path.join('..','..','data', 'SV', 'output', 'ownershipAssignment', 'DBSCAN_PredictedLocations_FT=0.0.csv')
        obj_loc_df = pd.read_csv(data_path, usecols=['name','longitude','latitude','predicted_location'])
        Searcher = COMPASS_OO_Search(obj_loc_df)
        yield Searcher.db_CM_dict['Faber Vineyard']  # This is one CM
        del Searcher.db_CM_dict['Faber Vineyard']

    def test_init(self, setup_CM):
        CM_path = os.path.join('..','..','data', 'SV', 'output', 'concept_mapping', 'ConceptMaps_DBSCAN_PredictedLocations_FT=0.0.pkl')
        with open(CM_path, "rb") as inFile:
            conceptMaps = pickle.load(inFile)
            old_faber_CM = conceptMaps['Faber Vineyard']

        assert (setup_CM.matrix == old_faber_CM).all()

    

class TestCOMPASS_OO_Search:
    @pytest.fixture
    def setup_COMPASS_OO_Search(self):
        data_path = os.path.join('..','..','data', 'SV', 'output', 'ownershipAssignment', 'DBSCAN_PredictedLocations_FT=0.0.csv')
        obj_loc_df = pd.read_csv(data_path, usecols=['name','longitude','latitude','predicted_location'])
        test_searcher = COMPASS_OO_Search(obj_loc_df)
        yield test_searcher
        del test_searcher

    @pytest.fixture
    def setup_canvas_query(self):
        matrix = np.array( [[ 0, "bus_stop", 0,  0,  0,  0 ],
                            [ 0,  0, 0 ,0, 0, 0 ],
                            [ 0,  0, "parking_lot", 0, 0, 0],
                            [ 0, 0, 0, 0, 0, 0 ],
                            [ 0,  0,  0,  0,  0,  0 ],
                            [0, 0,  0,  0,  0,  "building" ]], dtype=object)
        test_canvas = Canvas(name="testCanvas", center=(2.5,2.5), matrix=matrix, BL=(0,5), BR=(5,5), TL=(0,0), TR=(5,0))
        yield test_canvas
        del test_canvas

    @pytest.mark.parametrize("latlist, longlist, expected", [(["A"],["A"],["A"]), (["A","B"],["A","B"],["A","B"])])
    def test_search_order_simple(self, setup_COMPASS_OO_Search, latlist, longlist, expected):
        assert setup_COMPASS_OO_Search.get_search_order(longlist, latlist) == expected

    @pytest.mark.parametrize("latlist, longlist, expected", [(["A","B"],["B","A"],["A","B"]), (["A","B","C"],["C","B","A"],["A","C","B"])])
    def test_search_order_complex(self, setup_COMPASS_OO_Search, latlist, longlist, expected):
        assert setup_COMPASS_OO_Search.get_search_order(longlist, latlist) == expected

    def test_search_CM(self, setup_COMPASS_OO_Search):
        assert 'Faber Vineyard' in setup_COMPASS_OO_Search.search_CM(['building','retaining_wall'])
        # TODO: verify results are correct

    def test_search(self, setup_COMPASS_OO_Search):
        query_canvas = Canvas(points=[{'name':'building','x':1,'y':1}], center=(5,5), BL=(0,10), TL=(0,0), TR=(10,0), BR=(10,10),)
        assert 'Faber Vineyard' in setup_COMPASS_OO_Search.search(query_canvas)
        # TODO: verify results are correct and need more complex queries

    def test_search_complex(self, setup_COMPASS_OO_Search, setup_canvas_query):
        assert "Little River Winery and Café" in setup_COMPASS_OO_Search.search(setup_canvas_query)
