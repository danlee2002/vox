from Expr import Expr, Binary, Grouping, Literal, Unary
from typing import Any, Union
from tokens import TokenType, Tokens
class AstPrinter:
    def print(self, expr: Union[Expr, Any]) -> str:
        return expr.accept(self)

    def visit_binary(self, expr: Binary) -> str:
        return self.parenthesize(expr.operator.lexme, expr.left, expr.right)
 
    def visit_grouping(self, expr: Grouping) -> str:
        return self.parenthesize('group', expr.expression)

    def visit_literal(self, expr: Literal) -> str:
        if expr.value is None:
            return 'nil'
        return str(expr.value)

    def visit_unary(self, expr: Unary) -> str:
        return self.parenthesize(expr.operator.lexme, expr.right)

    def parenthesize(self, name: Any, *exprs: Union[Expr, None]) -> str:
        builder = []
        builder.append(f'({name}')
        for expr in exprs:
            if not expr:
                print("Expression Cannot Be None")
                break
            builder.append(f' {expr.accept(self)}')
        builder.append(')')
        return ''.join(builder)

