import sys
sys.path.append(f"{sys.path[0]}/../")
import lexer
import unittest


class TestReturnContinueBreak(unittest.TestCase):
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

    def test_return(self):
        res, err= lexer.run("<test>", 'fnc main(); let a = 100; return a; end;')
        res, err= lexer.run("<test>", 'main()')
        self.assertEqual(str(res), '100')
        
    def test_continue_break(self):
        res, err= lexer.run("<test>", 'let a= []')
        res, err= lexer.run("<test>", 'for i=0 to 10 then; if i==4 then continue else if i==8 then break; let a=a+i;end')
        res, err= lexer.run("<test>", 'a')
        self.assertEqual(str(res), '0,1,2,3,5,6,7')


        
    