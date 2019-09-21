
class Expression: 
	def to_variable(self):
		return (name, item)

class IsType(Expression):
	def __init__(self, ClassType, name):
		self.var_name = name
		self.var_value = ClassType(name)

	def to_coq(self):
		pass
		
	def __repr__(self):
		return "{} is a {}".format(self.var_name, self.var_value)

class IsGroupElement(Expression):
	def __init__(self, elt, group):
		self.elt = elt
		self.group = group

	def to_coq(self):
		return "In U (S {}) {}".format(self.group.name, self.elt.name)

	def __repr__(self):
		return "{} ∈ {}".format(self.elt, self.group)

class IsEqual(Expression):
	def __init__(self, left, right):
		self.left = left
		self.right = right

	def to_coq(self):
		return "{} = {}".format(self.left.to_coq(), self.right.to_coq())

	def __repr__(self):
		return "{} = {}".format(self.left, self.right)


class Product(Expression):
	def __init__(self, a, b, operation="op G"):
		self.operation = operation
		self.a = a
		self.b = b

	def to_coq(self):
		return "{} {} {}".format(self.operation, self.a, self.b)

	def __repr__(self):
		return "{} * {}".format(self.a, self.b)


