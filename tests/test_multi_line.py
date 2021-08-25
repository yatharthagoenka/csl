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

    def test_for_multiline(self):
        res, err= lexer.run("<test>", '1+2;3*4')
        self.assertEqual(str(res), '3,12')


        
    
