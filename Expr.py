from tokens import Tokens
from typing import Any, Union
from abc import ABC, abstractmethod

class Expr(ABC):
	@abstractmethod
	def accept(self, visitor: "Any") -> str:
		pass
class Assign(Expr):
	def __init__(self, name: Tokens, value: Expr):
		self.name = name
		self.value = value

	def accept(self, visitor: "Any")-> str:
		return visitor.visit_assign(self)

class Binary(Expr):
	def __init__(self, left: Union[Expr,None], operator: Tokens, right: Union[Expr,None]):
		self.left = left
		self.operator = operator
		self.right = right

	def accept(self, visitor: "Any")-> str:
		return visitor.visit_binary(self)

class Grouping(Expr):
	def __init__(self, expression: Union[Expr,None]):
		self.expression = expression

	def accept(self, visitor: "Any")-> str:
		return visitor.visit_grouping(self)

class Literal(Expr):
	def __init__(self, value: object):
		self.value = value

	def accept(self, visitor: "Any")-> str:
		return visitor.visit_literal(self)

class Unary(Expr):
	def __init__(self, operator: Tokens, right: Union[Expr,None]):
		self.operator = operator
		self.right = right

	def accept(self, visitor: "Any")-> str:
		return visitor.visit_unary(self)

class Variable(Expr):
	def __init__(self, name: Tokens):
		self.name = name

	def accept(self, visitor: "Any")-> str:
		return visitor.visit_variable(self)

