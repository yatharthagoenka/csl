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

    def test_list(self):
        res, err= lexer.run("<test>", '[1,2, "string", true]')
        self.assertEqual(str(res), '1,2,string,1')

    def test_list_add(self):
        res, err= lexer.run("<test>", "[1,2]+4")
        self.assertEqual(str(res), "1,2,4") 

    def test_list_remove(self):
        res, err= lexer.run("<test>", "[1,2,8,6]-2")
        self.assertEqual(str(res), "1,2,6") 
        
    def test_list_concat(self):
        res, err= lexer.run("<test>", "[1,2]*[3,5]")
        self.assertEqual(str(res), "1,2,3,5") 

    def test_list_get(self):
        res, err= lexer.run("<test>", "[1,2,5,4]/2")
        self.assertEqual(str(res), "5") 
        
    def test_list_len(self):
        res, err= lexer.run("<test>", "let a = [1,2,3,4,5]")
        res, err= lexer.run("<test>", "len(a)")
        self.assertEqual(str(res), "5") 
        
    
