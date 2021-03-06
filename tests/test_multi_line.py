import sys
sys.path.append(f"{sys.path[0]}/../")
import lexer
import unittest


class TestMultiLine(unittest.TestCase):
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

    def test_multiline_arithmetic(self):
        res, err= lexer.run("<test>", '1+2;3*4')
        self.assertEqual(str(res), '3,12')

    def test_multiline_loop_with_condition(self):
        res, err= lexer.run("<test>", 'let a=[]')
        res, err= lexer.run("<test>", 'for i=0 to 10 then; if i==4 then append(a,44);end')
        res, err= lexer.run("<test>", 'a')
        self.assertEqual(str(res), '44')


        
    
