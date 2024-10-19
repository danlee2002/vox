import Expr
from tokens import Tokens
from typing import Any, Union
from abc import ABC, abstractmethod

class Stmt(ABC):
	@abstractmethod
	def accept(self, visitor: "Any") -> str:
		pass
class Expression(Stmt):
	def __init__(self, expression: Expr.Expr):
		self.expression = expression

	def accept(self, visitor: "Any")-> str:
		return visitor.visit_expression(self)

class Print(Stmt):
	def __init__(self, expression: Expr.Expr):
		self.expression = expression

	def accept(self, visitor: "Any")-> str:
		return visitor.visit_print(self)

class Var(Stmt):
	def __init__(self, name: Tokens, initializer: Expr.Expr):
		self.name = name
		self.initializer = initializer

	def accept(self, visitor: "Any")-> str:
		return visitor.visit_var(self)

