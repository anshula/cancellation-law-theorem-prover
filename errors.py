class CoqError(Exception):
    """ Raised when coqtop prints 'Error' in its response """
    pass

class UndoError(Exception):
	""" 
	Raised when agent tries to undo one of the first four actions
	That is, when it tries to undo defining initial variables, assumptions, goals, and defn of the theorem
	"""
	pass