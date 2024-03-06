


from _globals import *

""""""
from PseudoPathy.Group import PathGroup

class Path(str):
	""""""

	def __init__(self) -> None:
		pass

	def __new__(cls, *paths):
		obj = super(Path, cls).__new__(cls, pJoin(*paths))
		return obj
	
	def __add__(self, right):
		return DirectoryPath(str.__add__(self.rstrip(pSep), right)) if not pIsFile(right) else FilePath(str.__add__(self.rstrip(pSep), right))

	def __gt__(self, right):
		return DirectoryPath(self, right) if not pIsFile(right) else self.__new__(self, right)
	
	def __lt__(self, left):
		return DirectoryPath(left, self)

	def __or__(self, right):
		if type(right) is PathGroup:
			return PathGroup(self, *right._roots, purpose=right.defaultPurpose)
		else:
			return PathGroup(self, right)
	
	def __ror__(self, left):
		if type(left) is PathGroup:
			return PathGroup(*left._roots, self, purpose=left.defaultPurpose)
		else:
			return PathGroup(left, self)

class DirectoryPath(Path):
	""""""
	
	pass

class FilePath(Path):
	""""""

	pass
	# def __lt__(self, right):
	# 	raise TypeError(f"Attempted to append path to a filepath, this behovior is not currently supported (Allowed). Attempted to combine '{self}' with '{right}'")

class DisposablePath(Path):
	""""""

	def __del__(self):
		if DISPOSE:
			try:
				shutil.rmtree(self, ignore_errors=True)
			except:
				LOGGER.warning(f"Failed to remove content of directory: '{self}'")
