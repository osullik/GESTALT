import pytest
import sys
import os
import pickle
import numpy as np

from compass import ConceptMap
from compass import COMPASS_OO_Search

class TestConceptMap:
    @pytest.fixture
    def setup_CM(self):
        data_path = os.path.join('..','..','data', 'SV', 'output', 'ownershipAssignment', 'DBSCAN_PredictedLocations_FT=0.0.csv')
        with open(data_path, "r") as inFile:
            print(inFile.readline())
            CM = ConceptMap(None)  # Needs to get a subset of the input data to make a CM
        yield CM
        del CM

    def test_init(self, setup_CM):
        CM_path = os.path.join('..','..','data', 'SV', 'output', 'concept_mapping', 'ConceptMaps_DBSCAN_PredictedLocations_FT=0.0.pkl')
        with open(CM_path, "rb") as inFile:
            conceptMaps = pickle.load(inFile)
            old_faber_CM = conceptMaps['Faber Vineyard']
        # assert setup_CM == old_faber_CM

    

class TestCOMPASS_OO_Search:
    @pytest.fixture
    def setup_COMPASS_OO_Search(self):
        test_searcher = COMPASS_OO_Search(None)  # TODO: make this an actual data value
        yield test_searcher
        del test_searcher

    def test_search_order1(self, setup_COMPASS_OO_Search):
        latlist, longlist = ["A"], ["A"]
        assert setup_COMPASS_OO_Search.get_search_order(longlist, latlist) == ["A"]

    def test_search_order2(self, setup_COMPASS_OO_Search):
        latlist, longlist = ["A","B"], ["A","B"]
        assert setup_COMPASS_OO_Search.get_search_order(longlist, latlist) == ["A","B"]

    def test_search_order3(self, setup_COMPASS_OO_Search):
        latlist, longlist = ["A","B"], ["B","A"]
        assert setup_COMPASS_OO_Search.get_search_order(longlist, latlist) == ["A","B"]

    def test_search_order4(self, setup_COMPASS_OO_Search):
        latlist, longlist = ["A","B","C"], ["C","B","A"]
        assert setup_COMPASS_OO_Search.get_search_order(longlist, latlist) == ["A","C","B"]
