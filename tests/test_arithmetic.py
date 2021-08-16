import sys
sys.path.append(f"{sys.path[0]}/../")
import lexer
import unittest


class TestArithmetic(unittest.TestCase):
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

    def test_equation(self):
        res, err= lexer.run("<test>", "-10+(10/5)*5")
        self.assertEqual(str(res), "0.0")

    def test_float(self):
        res, err= lexer.run("<test>", "5/2")
        self.assertEqual(str(res), "2.5")

    def test_pow(self):
        res, err= lexer.run("<test>", "2^10")
        self.assertEqual(str(res), "1024")
