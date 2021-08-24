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

    def test_math_pi(self):
        res, err= lexer.run("<test>", "Math_pi")
        self.assertEqual(str(res), "3.141592653589793")

