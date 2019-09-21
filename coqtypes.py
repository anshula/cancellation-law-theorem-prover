
class GroupElement:
	def __init__(self, name, group):
		self.name = name
		self.group = group
		self.type = group.U

	def to_coq(self):
		pass

class Group:
	def __init__(self, name):
		self.name = name
		self.U = Variable("U")
		self.operation = "op {}".format(name)
		self.inverse = "inv {}".format(name)
		self.identity = "id {}".format(name)
		
	def load_properties(self):
		pass

	def multiply(self, elt1, elt2):
		# assume self and other are part of same group
		new = GroupElement("{} {} {}".format(self.operation, elt1.name, elt2.name), self)
		return new

	def inverse(self, element):
		inv = GroupElement("{} {}".format(self.inverse, elt.name), self)
		return inv

	def identity(self, elt):
		return elt 

	def to_coq_declare(self):
		return "Variable {}:group U. ".format(self.name)

	def to_coq(self):
		return self.name

	def __repr__(self):
		return "Group {}".format(self.name)

class Variable:
	def __init__(self, name, coqtype="U"):
		self.name = name
		self.type = coqtype
		# self.supersets = [Group]

	def to_coq_declare(self):
		return "Variable {}:{}. ".format(self.name, self.type)

	def to_coq(self):
		return self.name

	def __repr__(self):
		return self.name

class Subgoal:
	def __init__(self, statement):
		self.statement = statement

	def __str__(self):
		return self.statement

	def __repr__(self):
		return self.__str__()




