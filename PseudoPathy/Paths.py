

from PseudoPathy.Globals import *

class Path: pass
class PathGroup: pass

class Path(str):
	""""""

	defaultPurpose : str
	@property
	def writable(self): return self.__getitem__("", purpose="w")
	@property
	def readable(self): return self.__getitem__("", purpose="r")
	@property
	def executable(self): return self.__getitem__("", purpose="x")
	@property
	def fullPerms(self): return self.__getitem__("", purpose="rwx")

	def __new__(cls, *paths, purpose="r"):
		if cls is Path:
			if pIsFile(paths[-1]):
				cls = FilePath
			else:
				cls = DirectoryPath
		
		obj = super(Path, cls).__new__(cls, pNorm(pJoin(*paths)))
		obj.defaultPurpose = purpose
		return obj
	
	def __add__(self, right):
		return Path(str.__add__(self.rstrip(pSep), right), purpose=self.defaultPurpose)

	def __gt__(self, right):
		return Path(self, right, purpose=getattr(right, "defaultPurpose", None) or self.defaultPurpose)
	
	def __lt__(self, left):
		return Path(left, self, purpose=self.defaultPurpose)

	def __or__(self, right : Path|PathGroup):
		from PseudoPathy.Group import PathGroup
		return PathGroup(self, *right, purpose=getattr(right, "defaultPurpose", None) or self.defaultPurpose)
	
	def __ror__(self, left : Path|PathGroup):
		from PseudoPathy.Group import PathGroup
		return PathGroup(*left, self, purpose=self.defaultPurpose or getattr(left, "defaultPurpose", None))
		
	def __iter__(self) -> list[Path]:
		return iter([self])
	
	def __getitem__(self, path : str, purpose:str=None) -> str:
		if type(path) in [slice, int]:
			return str.__getitem__(self, path)
		else:
			if purpose is None:
				purpose = self.defaultPurpose
			if pExists(self > path):
				if pAccess(self > path, purpose):
					return Path(self > path, purpose=purpose)
		return None
	
	def create(self, path : str, purpose : str=None) -> Path:
		'''Should not be used to create files, only directories!'''
		if purpose is None:
			purpose = self.defaultPurpose
	
		if pAccess(self > path, purpose):
			return self > path
		
		elif pBackAccess(self, os.W_OK): # Try to make a path for purpose(s).
			try:
				pMakeDirs(self > path)
				return self > path
			except:
				pass # Happens if write permission exists for parent directories but not for lower level directories.
		return None

class DirectoryPath(Path):
	""""""
	
	pass

class FilePath(Path):
	""""""

	ext : str
	@property
	def ext(self):
		return "."+self.rpartition(".")[-1]
	
	def __lshift__(self, value : str):
		"""Creates a version of the `FilePath` with the right string as the file extension. This changes the text
		following the last dot of the file, instead of appending the new file extension behind the old one."""
		return FilePath(self.rsplit(".", 1)[0]+"."+value.lstrip("."))

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

class PathList(list):
	def __new__(cls, *data):
		obj = super(PathList, cls).__new__(cls, *data)
		return obj
	
	def __str__(self):
		return " ".join(self)
	
	def __format__(self, format_spec):
		return " ".join(self)