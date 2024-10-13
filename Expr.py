from tokens import Tokens, TokenType
from typing import Any
from abc import ABC, abstractmethod

class Expr(ABC):
	@abstractmethod
	def accept(self, visitor: "AstPrinter") -> str:
		pass
class Binary(Expr):
	def __init__(self, left: Expr, operator: Tokens, right: Expr):
		self.left = left
		self.operator = operator
		self.right = right

	def accept(self, visitor: "AstPrinter")-> str:
		return visitor.visit_binary(self)

class Grouping(Expr):
	def __init__(self, expression: Expr):
		self.expression = expression

	def accept(self, visitor: "AstPrinter")-> str:
		return visitor.visit_grouping(self)

class Literal(Expr):
	def __init__(self, value: Any):
		self.value = value

	def accept(self, visitor: "AstPrinter")-> str:
		return visitor.visit_literal(self)

class Unary(Expr):
	def __init__(self, operator: Tokens, right: Expr):
		self.operator = operator
		self.right = right

	def accept(self, visitor: "AstPrinter")-> str:
		return visitor.visit_unary(self)

