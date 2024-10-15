
import sys
import os 
from typing import Union, Any
from tokens import Tokens, TokenType
import Expr 
from AstPrinter import AstPrinter
class Interpreter:
    def __init__(self):
        self.haderror = False 
        
    def run(self, string):
        from scanner import Scanner
        from parser import Parser
        scan= Scanner(string, self)
        tokens = scan.scanTokens()
        parser = Parser(tokens)
        expression = parser.parse()
        print(type(expression))
        result = self.evaluate(expression)
        if self.haderror:
            return 
        printer = AstPrinter()
        print(result)
        sys.stdout.write(f'{printer.print(expression)}\n')
        
    def error(self, line: int, message: str):
        self.report(line, "",message)

    def parse_error(self, token: Tokens, message: str):
        if token.type == TokenType.EOF:
            self.report(token.line, ' at end', message)
        else:
            self.report(token.line, f'at "{token.lexme}"', message)

    def report(self,line: int, where: str, message: str):
        sys.stdout.write(f'[line {line}] Error {where}" {message}')
        self.haderror = True
  
    def runFile(self, scriptname: str):
        with open(scriptname, 'rb') as file:
            bytecontent = file.read()
        string = bytecontent.decode(os.device_encoding(0) or 'utf-8')
        self.run(string)
        if self.haderror: 
            sys.exit(65)

    def runPrompt(self):
        while True:
            sys.stdout.write(">>> ")
            sys.stdout.flush()
            line = sys.stdin.readline().strip()
            if not line: break
            self.run(line)
            self.haderror = False 
            sys.stdout.write(line + '\n')
            sys.stdout.flush()
                
    def interpret(self):
        n = len(sys.argv) - 1
        if n > 1:
            sys.stdout.write("Vox: Script")
            sys.exit(64)
        elif n == 1:
            self.runFile(sys.argv[1])
        else:
            self.runPrompt()

    def visit_literal(self, expr: Expr.Literal):
        return expr.value
    
    def visit_grouping(self, expr: Expr.Grouping):
        return self.evaluate(expr)
    
    def visit_unary(self, expr: Expr.Unary):
        right = self.evaluate(expr.right)
        match expr.operator.type:
            case TokenType.MINUS:
                return -float(right)
            case TokenType.BANG:
                return not self.is_truthy(right)

        return None 
    
    def visit_binary(self, expr: Expr.Binary):
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)
        print(left)
        print(right)
        match expr.operator.type:
            case TokenType.MINUS:
                return float(left) - float(right)
            case TokenType.PLUS:
                return left + right
            case TokenType.SLASH:
                return left/right
            case TokenType.STAR:
                return left * right 
            case TokenType.GREATER:
                return left > right
            case TokenType.GREATER_EQUAL:
                return left >= right
            case TokenType.LESS:
                return left < right
            case TokenType.LESS_EQUAL:
                return left <= right
            case TokenType.BANG_EQUAL:
                return left != right
            case TokenType.EQUAL_EQUAL:
                return left == right 
            case _:
                return None 
                
    def is_truthy(self, object) -> bool:
        if object is None:
            return False 
        if isinstance(object, bool):
            return object
        return True
    
    def evaluate(self, expr: Union[Expr.Expr,None]) -> Any:
        if not expr:
            return None 
        return expr.accept(self)



if __name__ == '__main__':
    interpreter = Interpreter()
    interpreter.interpret()
