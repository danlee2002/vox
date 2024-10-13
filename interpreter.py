
import sys
import os 
from typing import Optional
from tokens import Tokens, TokenType
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
        if self.haderror:
            return 
        printer = AstPrinter()
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


if __name__ == '__main__':
    interpreter = Interpreter()
    interpreter.interpret()
