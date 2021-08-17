import sys
sys.path.append(f"{sys.path[0]}/../")
import lexer
import unittest


class TestBoolian(unittest.TestCase):
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

    def test_if(self):
        res, err= lexer.run("<test>", "if 2*3==6 then 6 else if 5-4==1 then 9 else 60+9")
        self.assertEqual(str(res), "6")

    def test_else_if(self):
        res, err= lexer.run("<test>", "if 2*3==7 then 6 else if 5-4==1 then 9 else 60+9")
        self.assertEqual(str(res), "9")

    def test_else(self):
        res, err= lexer.run("<test>", "if 2*3==7 then 6 else if 5-3==1 then 9 else 60+9")
        self.assertEqual(str(res), "69")


