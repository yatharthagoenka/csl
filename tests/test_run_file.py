import sys
sys.path.append(f"{sys.path[0]}/../")
import lexer
import unittest


class TestRunFile(unittest.TestCase):
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

    def test_run(self):
        res, err= lexer.run("<test>", 'run("tests/test.csl")')
        res, err= lexer.run("<test>", 'a')
        self.assertEqual(str(res), 'hello')
        


        
    