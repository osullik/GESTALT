import pytest
import numpy as np

from compass import COMPASS_OO_Search

class TestConceptMap:
    @pytest.fixture
    def setup_CM(self):
        pass

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