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

    def test_eq_eq(self):
        res, err= lexer.run("<test>", "1==1")
        self.assertEqual(str(res), "1")

    def test_not_eq(self):
        res, err= lexer.run("<test>", "1!=1")
        self.assertEqual(str(res), "0")

    def test_nested(self):
        res, err= lexer.run("<test>", "(1==1) and not (1!=1)")
        self.assertEqual(str(res), "1")

    def test_true_false(self):
        res, err= lexer.run("<test>", "true + false")
        self.assertEqual(str(res), "1")


