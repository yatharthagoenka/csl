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
        res, err= lexer.run("<test>", "let a = 0")
        pass

    def tearDown(self):
        # Runs after every test
        pass

    def test_for_loop(self):
        res, err= lexer.run("<test>", "for i=1 to 101 then let a=a+i")
        res, err= lexer.run("<test>", "a")
        self.assertEqual(str(res), "5050")

    def test_for_loop_with_step(self):
        res, err= lexer.run("<test>", "for i=0 to 500 inc 5 then let a=a+1")
        res, err= lexer.run("<test>", "a")
        self.assertEqual(str(res), "100")

    def test_while_loop(self):
        res, err= lexer.run("<test>", "while a<1000 then let a=a+3")
        res, err= lexer.run("<test>", "a")
        self.assertEqual(str(res), "1002")
