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
        test_searcher = COMPASS_OO_Search(None)
        yield test_searcher
        del test_searcher

    def test_search_order(self, setup_COMPASS_OO_Search):
        latlist, longlist = ["A"], ["A"]
        assert setup_COMPASS_OO_Search.get_search_order(longlist, latlist) == ["A"]
