

try:
	from PseudoPathy.Globals import *
	from PseudoPathy.Group import PathGroup
except:
	from PseudoPathy.Globals import *
	from Group import PathGroup

class Path(str):
	""""""

	defaultPurpose : str

	def __new__(cls, *paths, purpose="r"):
		if cls is Path:
			if pIsFile(paths[-1]):
				cls = FilePath
			else:
				cls = DirectoryPath
		
		obj = super(Path, cls).__new__(cls, pSuperAbs(pJoin(*paths)))
		obj.defaultPurpose = purpose
		return obj
	
	def __add__(self, right):
		return Path(str.__add__(self.rstrip(pSep), right), purpose=self.defaultPurpose)

	def __gt__(self, right):
		return Path(self, right, purpose=getattr(right, "defaultPurpose", None) or self.defaultPurpose)
	
	def __lt__(self, left):
		return Path(left, self, purpose=self.defaultPurpose)

	def __or__(self, right : Path|PathGroup):
		return PathGroup(self, *right, purpose=getattr(right, "defaultPurpose", None) or self.defaultPurpose)
	
	def __ror__(self, left : Path|PathGroup):
		return PathGroup(*left, self, purpose=self.defaultPurpose or getattr(left, "defaultPurpose", None))
		
	def __iter__(self) -> list[Path]:
		return iter([self])
	
	def __getitem__(self, path : str, purpose:str=None) -> str:
		if type(path) in [slice, int]:
			return str.__getitem__(self, path)
		else:
			if purpose is None:
				purpose = self.defaultPurpose
			if os.path.exists(self > path):
				if all(os.access(self > path, PERMS_LOOKUP_OS[p]) for p in purpose):
					return Path(self > path, purpose=purpose)
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
	"""Will remove iteslf and its contents using shutil.rmtree in a try-except with ignore_errors=True.
	All DisposablePath instances can be disabled (Making them just a copy of `Path`) by setting
	PseudoPathy.Globals.DISPOSE=False."""

	def __del__(self):
		if DISPOSE:
			try:
				shutil.rmtree(self, ignore_errors=True)
			except:
				LOGGER.warning(f"Failed to remove content of directory: '{self}'")
