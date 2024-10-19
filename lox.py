
import sys
import os 
from interpreter import Interpreter
from tokens import Tokens, TokenType
from AstPrinter import AstPrinter
from interpreter import Interpreter, RuntimeException
class Lox:
    def __init__(self):
        self.haderror = False 
        self.interpreter = Interpreter()
        
    def run(self, string):
        from scanner import Scanner
        from parser import Parser
        scan= Scanner(string, self)
        tokens = scan.scanTokens()
        # for token in tokens:
        #     print(token)
        parser = Parser(tokens)
        statements = parser.parse()
        self.interpreter.interpret(statements,lox)
        if self.haderror:
            return 
        # printer = AstPrinter()
        # sys.stdout.write(f'{printer.print(statements)}\n')
        
    def error(self, line: int, message: str):
        self.report(line, "",message)

    def run_time_error(self, error: RuntimeException):
         sys.stdout.write(f'{error}\n[line {error.token.line}]')
         self.haderror = True 


    def report(self,line: int, where: str, message: str):
        sys.stdout.write(f'[line {line}] Error {where}" {message}')
        self.haderror = True
  
    def run_file(self, scriptname: str):
        with open(scriptname, 'rb') as file:
            bytecontent = file.read()
        string = bytecontent.decode(os.device_encoding(0) or 'utf-8')
        try:
            self.run(string)
        except RuntimeError as e:
           sys.stdout.write(f"Runtime error: {str(e)}\n") 
        if self.haderror: 
            sys.exit(65)

    def run_prompt(self):
        while True:
            sys.stdout.write(">>> ")
            sys.stdout.flush()
            line = sys.stdin.readline().strip()
            self.run(line)
            self.haderror = False
            sys.stdout.flush()

if __name__ == '__main__':
    lox = Lox()
    n = len(sys.argv) - 1
    if n > 1:
        sys.stdout.write("Vox: Script")
        sys.exit(64)
    elif n == 1:  
        lox.run_file(sys.argv[1])
    else:
        lox.run_prompt()
    