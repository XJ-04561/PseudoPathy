

try:
	from PseudoPathy._globals import *
	from PseudoPathy.Group import PathGroup
except:
	from _globals import *
	from Group import PathGroup

class Path(str):
	""""""

	defaultPurpose : str

	def __new__(cls, *paths, purpose="r"):
		if cls is Path:
			if pIsFile(paths[-1]):
				obj = FilePath(super(Path, cls).__new__(cls, pJoin(*paths)))
			else:
				obj = DirectoryPath(super(Path, cls).__new__(cls, pJoin(*paths)))
		else:
			obj = super(Path, cls).__new__(cls, pJoin(*paths))
		obj.defaultPurpose = purpose
		return obj
	
	def __add__(self, right):
		return DirectoryPath(str.__add__(self.rstrip(pSep), right)) if not pIsFile(right) else FilePath(str.__add__(self.rstrip(pSep), right))

	def __gt__(self, right):
		return Path(self, right)
	
	def __lt__(self, left):
		return Path(left, self)

	def __or__(self, right : Path|PathGroup):
		return PathGroup(self, *right, purpose=right.defaultPurpose or "r")
	
	def __ror__(self, left : Path|PathGroup):
		return PathGroup(*left, self, purpose=self.defaultPurpose or "r")
		
	def __iter__(self) -> list[Path]:
		return [self]
	
	def __getitem__(self, path : str, purpose:str=None) -> str:
		if purpose is None:
			purpose = self.defaultPurpose
		if os.path.exists(self > path):
			if all(os.access(self > path, PERMS_LOOKUP_OS[p]) for p in purpose):
				return FilePath(self > path, purpose=purpose) if pIsFile(path) else DirectoryPath(self > path, purpose=purpose)
		return None

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
