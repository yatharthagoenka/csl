import sys
sys.path.append(f"{sys.path[0]}/../")
import lexer
import unittest
from unittest.mock import patch


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

    def test_print_ret(self):
        res, err= lexer.run("<test>", 'print_ret("hello")')
        self.assertEqual(str(res), 'hello')

    @patch('builtins.input', return_value='world')
    def test_input(self, input):
        res, err= lexer.run("<test>", 'input()')
        self.assertEqual(str(res), 'world')

    @patch('builtins.input', return_value='123')
    def test_input_int(self, input):
        res, err= lexer.run("<test>", 'input_int()')
        self.assertEqual(str(res), '123')

    def test_is_num(self):
        res, err= lexer.run("<test>", 'is_num(12)')
        self.assertEqual(str(res), '1')

    def test_is_not_list(self):
        res, err= lexer.run("<test>", 'is_list(12)')
        self.assertEqual(str(res), '0')

    def test_is_list(self):
        res, err= lexer.run("<test>", 'is_list([12])')
        self.assertEqual(str(res), '1')
 
    def test_is_str(self):
        res, err= lexer.run("<test>", 'is_str("go")')
        self.assertEqual(str(res), '1')

    def test_is_func(self):
        res, err= lexer.run("<test>", 'fnc add()->100')
        res, err= lexer.run("<test>", 'is_func(add)')
        self.assertEqual(str(res), '1')

    def test_append(self):
        res, err= lexer.run("<test>", 'let a = []')
        res, err= lexer.run("<test>", 'append(a,21)')
        res, err= lexer.run("<test>", 'a')
        self.assertEqual(str(res), '21')

    def test_pop(self):
        res, err= lexer.run("<test>", 'let a = [1,2,3,4]')
        res, err= lexer.run("<test>", 'pop(a,1)')
        res, err= lexer.run("<test>", 'a')
        self.assertEqual(str(res), '1,3,4')

    def test_extend(self):
        res, err= lexer.run("<test>", 'let a = [1,2,3,4]')
        res, err= lexer.run("<test>", 'extend(a,["str"])')
        res, err= lexer.run("<test>", 'a')
        self.assertEqual(str(res), '1,2,3,4,str')
