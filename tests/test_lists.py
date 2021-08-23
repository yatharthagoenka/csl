import sys
sys.path.append(f"{sys.path[0]}/../")
import lexer
import unittest


class TestLists(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Run once before tests
        pass

    @classmethod
    def tearDownClass(cls):
        # Run once after tests
        pass

    def setUp(self):
        # Runs before every test
        pass

    def tearDown(self):
        # Runs after every test
        pass

    def test_for_list(self):
        res, err= lexer.run("<test>", "[1,2]")
        self.assertEqual(str(res), "[1,2]")

    def test_for_list_add(self):
        res, err= lexer.run("<test>", "[1,2]+4")
        self.assertEqual(str(res), "[1,2,4]") 

    def test_for_list_remove(self):
        res, err= lexer.run("<test>", "[1,2,8,6]-2")
        self.assertEqual(str(res), "[1,2,6]") 
        
    def test_for_list_concat(self):
        res, err= lexer.run("<test>", "[1,2]*[3,5]")
        self.assertEqual(str(res), "[1,2,3,5]") 
        
    
