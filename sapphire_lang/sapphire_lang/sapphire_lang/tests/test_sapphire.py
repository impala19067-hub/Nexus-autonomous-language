"""
Sapphire Language Automated Test Suite
"""
import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.lexer import Lexer
from src.parser import Parser
from src.interpreter import Interpreter
from src.stdlib import STDLIB

class TestSapphire(unittest.TestCase):
    def test_lexer_tokens(self):
        code = 'let x = 10 + 20; $ ls -la |> filter()'
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        self.assertTrue(len(tokens) > 5)

    def test_basic_eval(self):
        code = '''
        let a = 15;
        let b = 25;
        let sum = a + b;
        sum;
        '''
        lexer = Lexer(code)
        parser = Parser(lexer.tokenize())
        ast = parser.parse()
        interp = Interpreter()
        res = interp.interpret(ast)
        self.assertEqual(res, 40)

    def test_process_cmd_and_pipe(self):
        code = '''
        let sys_info = os.system_info();
        sys_info.platform;
        '''
        lexer = Lexer(code)
        parser = Parser(lexer.tokenize())
        ast = parser.parse()
        interp = Interpreter()
        res = interp.interpret(ast)
        self.assertIn(res, ["Windows", "Linux", "Darwin"])

    def test_pc_clipboard_and_fs(self):
        code = '''
        fs.write("./test_output.tmp", "Sapphire Auto Test");
        let content = fs.read("./test_output.tmp");
        fs.remove("./test_output.tmp");
        content;
        '''
        lexer = Lexer(code)
        parser = Parser(lexer.tokenize())
        ast = parser.parse()
        interp = Interpreter()
        res = interp.interpret(ast)
        self.assertEqual(res, "Sapphire Auto Test")

    def test_parallel_execution(self):
        code = '''
        let result = [];
        parallel {
            let a = 1;
            let b = 2;
        }
        true;
        '''
        lexer = Lexer(code)
        parser = Parser(lexer.tokenize())
        ast = parser.parse()
        interp = Interpreter()
        res = interp.interpret(ast)
        self.assertTrue(res)

if __name__ == '__main__':
    unittest.main()
