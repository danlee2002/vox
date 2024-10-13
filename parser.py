from typing import Union
from interpreter import Interpreter
from tokens import TokenType, Tokens
from Expr import Expr, Binary, Grouping, Literal, Unary

class Parser:

    def __init__(self, tokens: list[Tokens]):
        self.tokens = tokens
        self.current = 0
        self.interpreter = Interpreter()
    
    def parse(self):
        try:
            return self.expression()
        except SyntaxError:
            return None
        
    def expression(self) -> Expr:
        return self.equality()
    
    def equality(self) -> Expr:
        expr = self.comparison()
        while self.verify(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            operator = self.previous()
            right = self.comparison()
            expr = Binary(expr, operator, right)
        return expr 

    def verify(self,*types: TokenType) -> bool:
        for typeval in types:
            if self.check(typeval):
                self.advance()
                return True 
        return False 
    
    def check(self, type: TokenType) -> bool:
        if self.is_at_end():
            return False
        return self.peek().type == type

    def peek(self) -> Tokens:
        return self.tokens[self.current]
    
    def is_at_end(self) -> bool:
        return self.tokens[self.current].type == TokenType.EOF
    
    def advance(self) -> Tokens:
        if not self.is_at_end():
            self.current+=1
        return self.previous()
    
    def previous(self) -> Tokens:
        return self.tokens[self.current-1]
    
    def comparison(self) -> Expr:
        expr = self.term()
        while self.verify(TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL):
            operator = self.previous()
            right = self.term()
            expr = Binary(expr, operator, right)
        return expr 
    
    def term(self) -> Expr:
        expr = self.factor()
        while self.verify(TokenType.SLASH, TokenType.PLUS):
            operator = self.previous()
            right = self.factor()
            expr = Binary(expr, operator, right)
        return expr
    
    def factor(self) -> Expr:
        expr = self.unary()
        while self.verify(TokenType.BANG, TokenType.STAR):
            operator = self.previous()
            right = self.unary()
            expr =  Binary(expr, operator, right) 
        return expr

    def unary(self) -> Expr:
        if self.verify(TokenType.BANG, TokenType.MINUS):
            operator = self.previous()
            right = self.unary()
            expr =  Unary(operator, right) 
            return expr
        return self.primary()
    
    def primary(self) -> Expr:
        if self.verify(TokenType.FALSE):
            return Literal(False)
        if self.verify(TokenType.TRUE):
            return Literal(True)
        if self.verify(TokenType.NIL):
            return Literal(None)
        if self.verify(TokenType.NUMBER, TokenType.STRING):
            return Literal(self.previous().literal)
        if self.verify(TokenType.LEFT_PAREN):
            expr = self.expression()
            self._consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return Grouping(expr)
        self.interpreter.parse_error(self.peek(), 'Expect Expression.')

    def _consume(self, type: TokenType, message: str) -> Union[Tokens,None]:
        if self.check(type):
            return self.advance()
        self.interpreter.parse_error(self.peek(),message)
        
    
    def synchronize(self):
        self.advance()
        while not self.is_at_end():
            if self.previous.type() == TokenType.SEMICOLON:
                return 

            match self.peek.type:
                case TokenType.CLASS:
                    return 
                case TokenType.FUN:
                    return 
                case TokenType.FOR:
                    return 
                case TokenType.IF:
                    return 
                case TokenType.WHILE:
                    return
                case TokenType.PRINT:
                    return 
                case TokenType.RETURN:
                    return 
            self.advance() 
                