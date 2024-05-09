

from typing import Any
from PseudoPathy.Globals import *
import PseudoPathy.Globals as Globals

class Path: pass
class PathGroup: pass

class Path(str):
	""""""

	defaultPurpose : str
	writable : Path
	"""The first path with writing permissions. If none exists, then tries to create one (Given that at least one path is not existent on the system)"""
	readable : Path
	"""The first path with reading permissions."""
	executable : Path
	"""The first path with execution permissions."""
	fullPerms : Path
	"""The first path with full permissions. If none exists, then tries to create one (Given that at least one path is not existent on the system)"""
	
	@property
	def writable(self): return self.create(purpose="w")
	@property
	def readable(self): return self.__getitem__("", purpose="r")
	@property
	def executable(self): return self.__getitem__("", purpose="x")
	@property
	def fullPerms(self): return self.create(purpose="rwx")

	def __new__(cls, /, p=".", *paths, purpose="r"):
		joined = pJoin(p, *paths)
		joined = joined.rstrip(pSep) or joined
		if cls is Path:
			if pIsFile(joined):
				cls = FilePath
			elif pIsDir(joined):
				cls = DirectoryPath
		
		obj = super(Path, cls).__new__(cls, joined)
		obj.defaultPurpose = purpose
		return obj
	
	def __add__(self, right):
		return Path(str.__add__(self, right), purpose=self.defaultPurpose)

	def __truediv__(self, right):
		return Path(self, right, purpose=getattr(right, "defaultPurpose", self.defaultPurpose))
	
	def __rtruediv__(self, left):
		return Path(left, self, purpose=self.defaultPurpose)

	def __or__(self, right : Path|PathGroup):
		from PseudoPathy.Group import PathGroup
		return PathGroup(self, *right, purpose=getattr(right, "defaultPurpose", self.defaultPurpose))
	
	def __ror__(self, left : Path|PathGroup):
		from PseudoPathy.Group import PathGroup
		return PathGroup(*left, self, purpose=self.defaultPurpose or getattr(left, "defaultPurpose", None))
		
	def __iter__(self) -> list[Path]:
		return iter([self])
	
	def __contains__(self, item):
		return pExists(self / item)
	
	def __getitem__(self, path : str, purpose:str=None) -> str:
		if type(path) in [slice, int]:
			return str.__getitem__(self, path)
		else:
			if purpose is None:
				purpose = self.defaultPurpose
			if pExists(self / path):
				if pAccess(self / path, purpose):
					return Path(self / path, purpose=purpose)
		return None
	
	def __format__(self, fs):
		try:
			return f"{stat.filemode(os.stat(self).st_mode)} {str(self).ljust(int('0'+fs[1:])-11) if fs.startswith('<') else str(self).rjust(int('0'+fs[1:])-11)}"
		except:
			return f"---------- {str(self).ljust(int('0'+fs[1:])-11) if fs.startswith('<') else str(self).rjust(int('0'+fs[1:])-11) if fs.startswith('>') else str(self).center(int('0'+fs[1:])-11)}"
	
	def create(self, path : str="", purpose : str=None, others : str="r") -> Path:
		'''Should not be used to create files, only directories!'''
		from PseudoPathy.PathShortHands import pPerms
		if purpose is None:
			purpose = self.defaultPurpose
	
		if pAccess(self / path, purpose):
			return self / path
		
		elif pBackAccess(self, "w"): # Try to make a path for purpose(s).
			try:
				pMakeDirs(self / path, mode=pPerms(purpose), others=pPerms(others))
				return self / path
			except:
				pass
		else:
			LOGGER.debug(f"pBackAccess({self!r}, \"w\") is False")
		return None

class DirectoryPath(Path):
	""""""
	
	pass

class FilePath(Path):
	""""""

	ext : str
	@property
	def ext(self):
		return self.rpartition(".")[-1]
	
	def __lshift__(self, value : str):
		"""Creates a version of the `FilePath` with the right string as the file extension. This changes the text
		following the last dot of the file, instead of appending the new file extension behind the old one."""
		return FilePath(self.rsplit(".", 1)[0]+"."+value.lstrip("."))

class UniqueFilePath(Path):
	
	def __new__(cls, /, p=".", *paths, purpose="w"):
		import tempfile
		dir, prefix = os.path.split(pJoin(p, *paths).rstrip(os.path.sep))
		obj = super(UniqueFilePath, cls).__new__(cls, tempfile.mkdtemp(dir=dir, prefix=prefix+"-[", suffix="]"))
		obj.defaultPurpose = purpose
		return obj

class PathList(list):
	def __new__(cls, *data):
		obj = super(PathList, cls).__new__(cls, *data)
		return obj
	
	def __str__(self):
		return " ".join(self)
	
	def __format__(self, format_spec):
		if format_spec.endswith("n"):
			self.nameAlign
		else:
			return "'"+"' '".join(self)+"'"
	
	@cached_property
	def nameAlign(self):
		from PseudoPathy.FileNameAlignment import fileNameAlign
		return fileNameAlign(*[pName(q) for q in self])