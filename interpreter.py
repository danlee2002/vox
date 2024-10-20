import Stmt
from tokens import TokenType, Tokens
import Expr
from typing import Union, Any
import sys
from error import RuntimeException
from env import Env
class Interpreter:
    def __init__(self):
        self.env = Env()
        
    def evaluate(self, expr: Union[Expr.Expr,None]) -> Any:
        if not expr:
            return None 
        return expr.accept(self)
    
    def visit_assign(self, expr: Expr.Assign):
        value = self.evaluate(expr.value)
        self.env.assign(expr.name,value)
        return value 
    
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
    
    def visit_var(self, stmt: Stmt.Var):
        value = None 
        # print(stmt.initializer)
        if stmt.initializer:
            value = self.evaluate(stmt.initializer)
            print(value)
        
        self.env.define(stmt.name.lexme, value)
        # print(self.env.values)

    def visit_variable(self, expr: Expr.Variable):
        return self.env.get(expr.name)
        


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

    def visit_expression(self, stmt: Stmt.Expression):
       self.evaluate(stmt.expression) 
    
    def visit_print(self, stmt: Stmt.Print):
        value = self.evaluate(stmt.expression)
        sys.stdout.write(f'{self.stringify(value)}\n')

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

    def interpret(self, statements: list[Stmt.Stmt], lox):
        try:
            for statement in statements:
                statement.accept(self)
            
        except RuntimeException as e:
            lox.run_time_error(e)
    
    def stringify(self, object: object) -> str:
        if not object:
            return "nil"
        if isinstance(object, str):
            return object
        if isinstance(object,float):
            text = str(object)
            if text.endswith('.0'): 
                return text[:-2]
            return text 
        return str(object)
