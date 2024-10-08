from enum import Enum
from interpreter import Interpreter
import interpreter
class TokenType(Enum):
    # Single-character tokens
    LEFT_PAREN = "LEFT_PAREN"
    RIGHT_PAREN = "RIGHT_PAREN"
    LEFT_BRACE = "LEFT_BRACE"
    RIGHT_BRACE = "RIGHT_BRACE"
    COMMA = "COMMA"
    DOT = "DOT"
    MINUS = "MINUS"
    PLUS = "PLUS"
    SEMICOLON = "SEMICOLON"
    SLASH = "SLASH"
    STAR = "STAR"
    # One or two character tokens
    BANG = "BANG"
    BANG_EQUAL = "BANG_EQUAL"
    EQUAL = "EQUAL"
    EQUAL_EQUAL = "EQUAL_EQUAL"
    GREATER = "GREATER"
    GREATER_EQUAL = "GREATER_EQUAL"
    LESS = "LESS"
    LESS_EQUAL = "LESS_EQUAL"
    # Literals
    IDENTIFIER = "IDENTIFIER"
    STRING = "STRING"
    NUMBER = "NUMBER"
    # Keywords
    AND = "AND"
    CLASS = "CLASS"
    ELSE = "ELSE"
    FALSE = "FALSE"
    FUN = "FUN"
    FOR = "FOR"
    IF = "IF"
    NIL = "NIL"
    OR = "OR"
    PRINT = "PRINT"
    RETURN = "RETURN"
    SUPER = "SUPER"
    THIS = "THIS"
    TRUE = "TRUE"
    VAR = "VAR"
    WHILE = "WHILE"
    # End of file
    EOF = "EOF"

class Tokens:
    def __init__(self, tokentype: TokenType, lexme: str, literal, line: int):
        self.type = tokentype
        self.lexme = lexme 
        self.literal = literal
        self.line = line

    def __str__(self) -> str:
        return f'{self.type} {self.lexme} {self.literal} {self.line}' 

class Scanner:
    def __init__(self, source: str, interpreter: Interpreter):
        self.source = source
        self.tokens: list[Tokens] = []
        self.start = 0
        self.current = 0
        self.line = 1
        self.interpreter = interpreter
        self.keywords = {
            'and': TokenType.AND,
            'class': TokenType.CLASS,
            'else': TokenType.ELSE,
            'false': TokenType.FALSE,
            'for': TokenType.FOR,
            'fun': TokenType.FUN,
            'if': TokenType.IF,
            'nil': TokenType.NIL,
            'or': TokenType.OR,
            'print': TokenType.PRINT,
            'super': TokenType.SUPER,
            'this': TokenType.THIS,
            'true': TokenType.TRUE,
            'var': TokenType.VAR,
            'while': TokenType.WHILE
        }

    def scanTokens(self) -> list[Tokens]:
        while (not self.isAtEnd()):
            self.start = self.current
            self.scanToken()
        self.tokens.append(Tokens(TokenType.EOF, "", None, self.line))
        return self.tokens
    
    def scanToken(self):
        char = self.advance() 
        match char: 
            case '(': self.addToken(TokenType.LEFT_PAREN)
            case ')': self.addToken(TokenType.RIGHT_PAREN)
            case '{': self.addToken(TokenType.LEFT_BRACE)
            case '}': self.addToken(TokenType.RIGHT_BRACE)
            case ',': self.addToken(TokenType.COMMA)
            case '-': self.addToken(TokenType.MINUS)
            case '.': self.addToken(TokenType.DOT)
            case '-': self.addToken(TokenType.MINUS)
            case '+': self.addToken(TokenType.PLUS)
            case ';': self.addToken(TokenType.SEMICOLON)
            case '*': self.addToken(TokenType.STAR)
            case '!': self.addToken(TokenType.BANG_EQUAL if self.verify('=') else TokenType.BANG)
            case '=': self.addToken(TokenType.EQUAL_EQUAL if self.verify('=') else TokenType.EQUAL)
            case '<': self.addToken(TokenType.LESS_EQUAL if self.verify('=') else TokenType.LESS) 
            case '>': self.addToken(TokenType.GREATER_EQUAL if self.verify('=') else TokenType.GREATER) 
            case '/': 
                if self.verify('/'):
                    while self.peek() != '\n' and not self.isAtEnd(): 
                        self.advance()
                # if self.verify('*'):
                #     while not self.isAtEnd():
                else:
                    self.addToken(TokenType.SLASH)
            case ' ': pass
            case '\r': pass 
            case '\t': pass 
            case '\n': self.line+=1
            case '"': self.string(self.interpreter)
            case char if char.isdigit(): self.number()
            case char if char.isalpha(): 
                self.identifier()
            case '_':
                self.identifier()
            case _: 
                self.interpreter.error(self.line, "Unexpected Character.")

    def string(self, interpreter: Interpreter):
        while (self.peek() != '"' and not self.isAtEnd()):
            if self.peek() == '\n': 
                line+=1
            self.advance()
        if (self.isAtEnd()):
            interpreter.error(self.line, "Unterminated String")
            return 
        self.advance()
        value = self.source[self.start + 1: self.current -1]
        self.addToken(TokenType.STRING, value)
    
    def identifier(self):
        while self.peek().isalnum():
            self.advance()
       
        string = self.source[self.start: self.current]
        if string in self.keywords:
            self.addToken(self.keywords[string], string)
            return 
        self.addToken(TokenType.IDENTIFIER, string)

    def number(self):
        while self.peek().isdigit():
            self.advance()
        if self.peek() == '.' and self.peekNext().isdigit():
            self.advance()
        while self.peek().isdigit():
            self.advance()
        self.addToken(TokenType.NUMBER, self.source[self.start: self.current])

    def verify(self, expected: str) -> bool:
        if self.isAtEnd(): return False
        if self.source[self.current] != expected: 
            return False
        self.current+=1
        return True 

    def peek(self):
        if self.isAtEnd(): 
            return '\0'
        return self.source[self.current]

    def peekNext(self):
        if self.current + 1 >= len(self.source): 
            return '\0'
        return self.source[self.current + 1]

    def advance(self) -> str:
        source = self.source[self.current]
        self.current+=1
        return source 
    
    def addToken(self, type: TokenType, literal = None):
        text = self.source[self.start: self.current]
        self.tokens.append(Tokens(type, text, literal, self.line))

    def isAtEnd(self) -> bool:
        return self.current >= len(self.source)
    
  
