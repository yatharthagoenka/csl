import sys
sys.path.append(f"{sys.path[0]}/../")
import lexer
import unittest


class TestFunction(unittest.TestCase):
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

    def test_add(self):
        res, err= lexer.run("<test>", "fnc add(a,b)->a+b")
        res, err= lexer.run("<test>", "add(100, 70)")
        self.assertEqual(str(res), "170")

    def test_assign_func_to_var(self):
        res, err= lexer.run("<test>", "let sub = fnc fun(a,b)->a-b")
        res, err= lexer.run("<test>", "sub(100,90)")
        self.assertEqual(str(res), "10")

    def test_recursive_function(self):
        res, err= lexer.run("<test>", "fnc fun(a,b)-> if a<=0 then b else fun(a-b,b-1)")
        res, err= lexer.run("<test>", "fun(1000, 101)")
        self.assertEqual(str(res), "90")

