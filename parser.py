from typing import Union
from lox import Lox
import Stmt
from tokens import TokenType, Tokens
import Expr
from error import ParseError

class Parser:

    def __init__(self, tokens: list[Tokens]):
        self.tokens = tokens
        self.current = 0
        self.lox = Lox()
    
    def parse(self) -> Union[list[Stmt.Stmt],None]:
        statements = []
        while not self.is_at_end():
            statements.append(self.declaration())
        return statements

    def expression(self) -> Union[Expr.Expr, None]:
        return self.assignment()
    
    def assignment(self):
        expr = self.equality()
        if self.verify(TokenType.EQUAL):
            equals = self.previous()
            value = self.assignment()
            if isinstance(expr, Expr.Variable):
                name = expr.name
                return Expr.Assign(name, value)
            self.error(equals,value)
        return expr
    
    def declaration(self):
        try:
            if self.verify(TokenType.VAR):
                return self.var_declaration()
            return self.statement()
        except ParseError: 
            self.synchronize()
    
    
    def var_declaration(self):
        name = self._consume(TokenType.IDENTIFIER, 'Expect Variable Name')
        initializer = None 
        if self.verify(TokenType.EQUAL):
            initializer = self.expression()
        self._consume(TokenType.SEMICOLON, 'Expect ";" after variable declaration.')
        return Stmt.Var(name, initializer)
    
    def error(self, token: Tokens, message: str):
        self.lox.error(token.line, message)
        raise ParseError()

    
    def statement(self):
        if self.verify(TokenType.PRINT):
            return self.print_statement()
        return self.expression_statement()

    def print_statement(self): 
        value = self.expression()
        self._consume(TokenType.SEMICOLON, 'Excpect ";" after value.')
        return Stmt.Print(value)
    
    def expression_statement(self):
        value = self.expression()
        self._consume(TokenType.SEMICOLON, 'Expect ";" after value.')
        return Stmt.Expression(value)

        
    
    def equality(self) -> Union[Expr.Expr, None]:
        expr = self.comparison()
        while self.verify(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            operator = self.previous()
            right = self.comparison()
            expr = Expr.Binary(expr, operator, right)
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
    
    def comparison(self) -> Union[Expr.Expr, None]:
        expr = self.term()
        while self.verify(TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL):
            operator = self.previous()
            right = self.term()
            expr = Expr.Binary(expr, operator, right)
        return expr 
    
    def term(self) -> Union[Expr.Expr, None]:
        expr = self.factor()
        while self.verify(TokenType.MINUS, TokenType.PLUS):
            operator = self.previous()
            right = self.factor()
            expr = Expr.Binary(expr, operator, right)
        return expr
    
    def factor(self) -> Union[Expr.Expr, None]:
        expr = self.unary()
        while self.verify(TokenType.SLASH, TokenType.STAR):
            operator = self.previous()
            right = self.unary()
            expr =  Expr.Binary(expr, operator, right) 
        return expr

    def unary(self) ->  Union[Expr.Expr, None]:
        if self.verify(TokenType.BANG, TokenType.MINUS):
            operator = self.previous()
            right = self.unary()
            expr =  Expr.Unary(operator, right) 
            return expr
        return self.primary()
    
    def primary(self) -> Union[Expr.Expr, None]:
        if self.verify(TokenType.FALSE):
            return Expr.Literal(False)
        if self.verify(TokenType.TRUE):
            return Expr.Literal(True)
        if self.verify(TokenType.NIL):
            return Expr.Literal(None)
        if self.verify(TokenType.NUMBER, TokenType.STRING):
            val = self.previous()
            return Expr.Literal(float(val.literal) if val.type == TokenType.NUMBER else val.literal)
        if self.verify(TokenType.LEFT_PAREN):
            expr = self.expression()
            self._consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return Expr.Grouping(expr)
        if self.verify(TokenType.IDENTIFIER):
            return Expr.Variable(self.previous())
        self.error(self.peek(), 'Expect Expression.')

    def _consume(self, type: TokenType, message: str) -> Union[Tokens,None]:
        if self.check(type):
            return self.advance()
        self.error(self.peek(),message)
        
    def synchronize(self):
        self.advance()
        while not self.is_at_end():
            if self.previous().type == TokenType.SEMICOLON:
                return 
            match self.peek().type:
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
                
