from ast import Expression
from tokens import TokenType, Tokens
import Expr
from typing import Union, Any
import sys

class RuntimeException(Exception):
    def __init__(self, token: Tokens, message: str):
        super().__init__(message)
        self.token = token

class Interpreter:
    def evaluate(self, expr: Union[Expr.Expr,None]) -> Any:
        if not expr:
            return None 
        return expr.accept(self)
    
    def visit_literal(self, expr: Expr.Literal):
        return expr.value
    
    def visit_grouping(self, expr: Expr.Grouping):
        return self.evaluate(expr.expression)
    
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
        match expr.operator.type:
            case TokenType.MINUS:
                self.check_binary(expr.operator, left, right)
                return float(left) - float(right)
            case TokenType.PLUS:
                self.check_addition(expr.operator, left, right)
                return left + right
            case TokenType.SLASH:
                self.check_binary(expr.operator, left, right)
                return left/right
            case TokenType.STAR:
                self.check_binary(expr.operator, left, right)
                return left * right 
            case TokenType.GREATER:
                self.check_binary(expr.operator, left, right)
                return left > right
            case TokenType.GREATER_EQUAL:
                self.check_binary(expr.operator, left, right)
                return left >= right
            case TokenType.LESS:
                self.check_binary(expr.operator, left, right)
                return left < right
            case TokenType.LESS_EQUAL:
                self.check_binary(expr.operator, left, right)
                return left <= right
            case TokenType.BANG_EQUAL:
                self.check_binary(expr.operator, left, right)
                return left != right
            case TokenType.EQUAL_EQUAL:
                return left == right 
            case _:
                return None 
    
    def check_binary(self, operator: Tokens, left: Any, right: Any):
        if isinstance(left, float) and isinstance(right, float):
            return 
        raise RuntimeException(operator, f'Runtime Exception Operator "{operator.lexme}": Operands must be Number.')
                
    def check_addition(self, operator: Tokens, left: Any, right: Any):
        if isinstance(left, (str, float)) and type(left) == type(right):
            return 
        raise RuntimeException(operator, f'Runtime Exception Operator "{operator.lexme}": Operands must be both Number or String.')
    
    def is_truthy(self, object) -> bool:
        if object is None:
            return False 
        if isinstance(object, bool):
            return object
        return True

    def interpret(self, expr: Expression, Lox):
        try:
            value = self.evaluate(expr)
            sys.stdout.write(f'{value}\n')
        except RuntimeException as e:
            Lox.run_time_error(e)
            
            
