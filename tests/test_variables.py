import sys
sys.path.append(f"{sys.path[0]}/../")
import lexer
import unittest


class TestVariables(unittest.TestCase):
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

    def test_assign(self):
        res, err= lexer.run("<test>", "let a = 5")
        self.assertEqual(str(res), "5")

    def test_operation_with_variable(self):
        res, err= lexer.run("<test>", "a*2")
        self.assertEqual(str(res), "10")

    def test_reassign_var(self):
        res, err= lexer.run("<test>", "let a = a*10")
        self.assertEqual(str(res), "50")


