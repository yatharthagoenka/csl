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

    # Variable must be assigned before using in loop
    def test_assign(self):
        res, err= lexer.run("<test>", "let a = 0")
        self.assertEqual(str(res), "0")

    def test_for_loop(self):
        res, err= lexer.run("<test>", "for i=0 to 5 then let a=a+1")
        self.assertEqual(str(res), "5")

    def test_while_loop(self):
        res, err= lexer.run("<test>", "while a<5 then let a=a+1")
        self.assertEqual(str(res), "5")



