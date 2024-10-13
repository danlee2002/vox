from scanner import TokenType, Tokens
import Expr
from AstPrinter import AstPrinter
if __name__ == "__main__":
    #Create an example expression: (1 + 2) * 3
    a =Expr.Unary(Tokens(TokenType.MINUS, '-', None, 1), Expr.Literal(123))
    b=  Tokens(TokenType.STAR, '*', None, 1)
    c = Expr.Grouping(Expr.Literal(45.67))
    expression = Expr.Binary(a,b,c)
    printer = AstPrinter()
    print(printer.print(expression))  # Should print: (* (- 123) (group 45.67))
