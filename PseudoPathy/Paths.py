

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
	exists : bool
	"""Whether the directory/file exists on the system."""

	@property
	def writable(self): return self.create(purpose="w")
	@property
	def readable(self): return self.__getitem__("", purpose="r")
	@property
	def executable(self): return self.__getitem__("", purpose="x")
	@property
	def fullPerms(self): return self.create(purpose="rwx")
	
	@property
	def exists(self): return pExists(self)

	@cached_property
	def directory(self):
		return DirectoryPath(os.path.split(self)[0]) if "." in os.path.split(self)[1][1:] else self
	
	@cached_property
	def file(self):
		return FilePath(os.path.split(self)[1]) if "." in os.path.split(self)[1][1:] else None

	def __new__(cls, /, p=".", *paths, purpose="r"):
		if not paths:
			if isinstance(p, Path):
				if p.defaultPurpose == purpose:
					return p
				else:
					obj = super().__new__(cls if type(p) is Path else type(p), p)
					obj.defaultPurpose = purpose
					return obj
		joined = pJoin(p, *paths)
		if cls is Path:
			if pIsFile(joined) or "." in os.path.split(joined)[-1][1:]:
				cls = FilePath
			elif pIsDir(joined):
				cls = DirectoryPath
		
		obj = super(Path, cls).__new__(cls, joined)
		obj.defaultPurpose = purpose
		return obj
	
	def __add__(self, right):
		return Path(str.__add__(self, right), purpose=self.defaultPurpose)

	def __sub__(self, right):
		return Path(str.__add__(self.rstrip(os.path.sep), right), purpose=self.defaultPurpose)

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
	
	def prepend(self, path):
		return path / self

	def append(self, path):
		return self / path

	def create(self, path : str="", purpose : str=None, others : str="r") -> Path:
		'''Should not be used to create files, only directories!'''
		from PseudoPathy.PathShortHands import pPerms
		if purpose is None:
			purpose = self.defaultPurpose
	
		if pAccess(self / path, purpose):
			return self / path
		
		elif pBackAccess(self, "w"): # Try to make a path for purpose(s).
			try:
				pMakeDirs(self / path)
				return self / path
			except:
				pass
		else:
			LOGGER.debug(f"pBackAccess({self!r}, \"w\") is False")
		return None

class DirectoryPath(Path):
	""""""
	
	@cached_property
	def directory(self) -> Self:
		return self
	
	@cached_property
	def file(self) -> None:
		return None

class FilePath(Path):
	""""""

	@property
	def writable(self): return self.find(purpose="w")
	@property
	def fullPerms(self): return self.find(purpose="rwx")
	@property
	def ext(self) -> str:
		return self.file.partition(".")[-1]
	@property
	def name(self) -> str:
		return self.file.partition(".")[0]
	
	def __lshift__(self, value : str):
		"""Creates a version of the `FilePath` with the right string as the file extension. This changes the text
		following the last dot of the file, instead of appending the new file extension behind the old one."""
		return FilePath(self.rsplit(".", 1)[0]+"."+value.lstrip("."))
	
	@cached_property
	def directory(self) -> DirectoryPath:
		return DirectoryPath(os.path.split(self)[0])
	
	@cached_property
	def file(self) -> Self:
		return FilePath(os.path.split(self)[1])

class UniqueFilePath(Path):
	
	def __new__(cls, /, p=".", *paths, purpose="w"):
		import tempfile
		dir, prefix = os.path.split(pJoin(p, *paths).rstrip(os.path.sep))
		
		return FilePath(tempfile.mkdtemp(dir=dir, prefix=prefix+"-[", suffix="]"), purpose=purpose)

class PathList(tuple):
	"""Is not based on the `list` type, as mutability is not desired, but the name is used for ease of learning for
	lesser experienced maintainers."""
	@overload
	def __new__(cls, iterable): ...
	@overload
	def __new__(cls, *paths): ...
	def __new__(cls, first, *rest):
		if not rest:
			if isinstance(first, str):
				paths = (Path(first),)
			else:
				paths = tuple(map(Path, first))
		else:
			paths = tuple(map(Path, (first,) + rest))
		
		if all(isinstance(p, FilePath) for p in paths):
			return super().__new__(FileList, paths)
		elif all(isinstance(p, DirectoryPath) for p in paths):
			return super().__new__(DirectoryList, paths)
		else:
			return super().__new__(cls, first)
	
	def __str__(self):
		return " ".join(self)
	
	def __format__(self, format_spec : str):
		if format_spec.endswith("n"):
			self.name
		else:
			return "'"+"' '".join(self)+"'"
	
	def __iter__(self) -> Generator[Self,None,None]:
		return super().__iter__()
	
	@cached_property
	def name(self) -> str:
		from PseudoPathy.FileNameAlignment import alignName
		return alignName(tuple(pName(p) for p in self))
	
	@cached_property
	def signature(self) -> str:
		from PseudoPathy.FileNameAlignment import alignSignature
		return alignSignature(self)

class DirectoryList(PathList): pass

class FileList(PathList):
	
	@cached_property
	def signature(self) -> str:
		from PseudoPathy.FileNameAlignment import alignSignature
		return alignSignature(tuple(p.directory / p.name for p in self))