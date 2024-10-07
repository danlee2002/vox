from enum import Enum 
from interpreter import Intrepreter 
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
        return f'{self.type} {self.lexme} {self.literal}' 


class Scanner:
    def __init__(self, source: str, interpreter: Intrepreter):
        self.source = source
        self.tokens: list[Tokens] = []
        self.start = 0
        self.current = 0
        self.line = 1
        self.interpreter = interpreter

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
            case '!': ...
            case '_': self.interpreter.error(self.line, "Unexpected Character.")






    def advance(self):
        return self.source[self.current]
        self.current+=1
    
    
    def addToken(self, type: TokenType, literal = None):
        text = self.source[self.start: self.current]
        self.tokens.append(Tokens(type, text, literal, self.line))

    
    
    def isAtEnd(self) -> bool:
        return self.current >= len(self.source)
        
