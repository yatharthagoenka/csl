import sys
sys.path.append(f"{sys.path[0]}/../")
import lexer
import unittest


class TestLoops(unittest.TestCase):
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

    def test_assign_string(self):
        res, err= lexer.run("<test>", 'let a = "this is string"')
        res, err= lexer.run("<test>", "a")
        self.assertEqual(str(res), '"this is string"')

    def test_string_concat(self):
        res, err= lexer.run("<test>", '"hello"+"world"')
        self.assertEqual(str(res), '"helloworld"')

    def test_string_mulitpy(self):
        res, err= lexer.run("<test>", '"go"*3')
        self.assertEqual(str(res), '"gogogo"')
