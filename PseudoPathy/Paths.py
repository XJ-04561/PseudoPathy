

from typing import Any
from PseudoPathy.Globals import *
import PseudoPathy.Globals as Globals

class Path: pass
class PathGroup: pass

class Path(str, Pathy):
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

	@property
	def directory(self):
		return DirectoryPath(os.path.split(self)[0]) if "." in os.path.split(self)[1][1:] else self
	
	@property
	def file(self):
		return FilePath(os.path.split(self)[1]) if "." in os.path.split(self)[1][1:] else None

	@overload
	def __new__(cls, /, p=".", *paths, purpose="r"): ...
	def __new__(cls, /, p=".", *paths, purpose=None):

		if paths or isinstance(p, str):
			joined = pJoin(p, *paths)
		elif type(p) is cls:
			if purpose is not None:
				p.defaultPurpose = purpose
			return p
		elif isinstance(p, (Iterable, Iterator)):
			joined = pJoin(*p)
		else:
			joined = p
			
		if cls is not Path:
			pass
		elif pIsFile(joined): # or "." in os.path.split(joined)[-1][1:]:
			cls = FilePath
		elif pIsDir(joined):
			cls = DirectoryPath
			
		obj = super().__new__(cls, joined)
		obj.defaultPurpose = purpose if purpose is not None else "r"
		return obj
	
	def __add__(self, right):
		if isinstance(right, Path):
			return type(right)(str.__add__(self, right), purpose=self.defaultPurpose)
		elif isinstance(right, str):
			return Path(str.__add__(self, right), purpose=self.defaultPurpose)
		else:
			return NotImplemented

	def __radd__(self, left):
		if isinstance(left, str):
			return type(self)(str.__add__(left, self), purpose=self.defaultPurpose)
		else:
			return NotImplemented
		
	def __sub__(self, right):
		return type(self)(str.__add__(self.rstrip(os.path.sep), right), purpose=self.defaultPurpose)

	def __truediv__(self, right):
		if isinstance(right, Path):
			return type(right)(self, right, purpose=getattr(right, "defaultPurpose", self.defaultPurpose))
		else:
			return Path(self, right, purpose=getattr(right, "defaultPurpose", self.defaultPurpose))
	
	def __rtruediv__(self, left):
		return type(self)(left, self, purpose=self.defaultPurpose)

	def __or__(self, right : Path|PathGroup):
		from PseudoPathy.Group import PathGroup
		if not isinstance(right, str) and isinstance(right, (Iterable, Iterator)):
			return PathGroup([self] + list(right), purpose=getattr(right, "defaultPurpose", self.defaultPurpose))
		else:
			return PathGroup([self, right], purpose=getattr(right, "defaultPurpose", self.defaultPurpose))
	
	def __ror__(self, left : Path|PathGroup):
		from PseudoPathy.Group import PathGroup
		if not isinstance(left, str) and isinstance(left, (Iterable, Iterator)):
			return PathGroup(list(left) + [self], purpose=self.defaultPurpose or getattr(left, "defaultPurpose", None))
		else:
			return PathGroup([left, self], purpose=self.defaultPurpose or getattr(left, "defaultPurpose", None))
		
	def __iter__(self) -> list[Path]:
		return iter([self])
	
	def __contains__(self, item):
		return pExists(self / item)
	
	def __getitem__(self, path : str, purpose:str=None) -> str:
		if type(path) in [slice, int]:
			return str.__getitem__(self, path)
		if not pExists(self / path):
			return None
		if pAccess(self / path, purpose or self.defaultPurpose):
			return Path(self / path, purpose=purpose or self.defaultPurpose)
		return None
	
	def __format__(self, fs):
		if fs.endswith("s"):
			fs = fs[:-1]
			try:
				return f"{stat.filemode(os.stat(self).st_mode)} {str(self).ljust(int('0'+fs[1:])-11) if fs.startswith('<') else str(self).rjust(int('0'+fs[1:])-11)}"
			except:
				return f"---------- {str(self).ljust(int('0'+fs[1:])-11) if fs.startswith('<') else str(self).rjust(int('0'+fs[1:])-11) if fs.startswith('>') else str(self).center(int('0'+fs[1:])-11)}"
		else:
			return format(str(self), fs)
	
	def find(self, path : str="", purpose : str=None):
		return self.__getitem__(path, purpose=purpose)

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

class DirectoryPath(Path, Directory):
	""""""
	
	@property
	def directory(self) -> "DirectoryPath":
		return self
	
	@property
	def file(self) -> None:
		return None

class FilePath(Path, File):
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
	
	@property
	def directory(self) -> DirectoryPath:
		return DirectoryPath(os.path.split(self)[0])
	
	@property
	def file(self) -> "FilePath":
		return FilePath(os.path.split(self)[1])

class UniqueFilePath(FilePath, Unique):
	"""If the path string given to instantiate is an existing directory, a "tempfile-[RANDOM].tmp" is created. Else if
	the path one step back is an existing directory, the basename of the path is provided as a prefix for the file
	name, and if the basename has a "." in it, everything after the first dot will be used as the file extension.
	Examples:
		Full path exists as a directory:
		"/home/fresor/.local/MyApp/tmp/" -> "/home/fresor/.local/MyApp/tmp/tempfile-[RANDOM].tmp"
		Full path except last segment exists as a directory:
		"/home/fresor/.local/MyApp/tmp/Session-2.txt.zip" -> "/home/fresor/.local/MyApp/tmp/Session-2-[RANDOM].txt.zip"
	"""
	
	def __new__(cls, /, p=".", *paths, purpose="w"):
		import tempfile
		path = pJoin(p, *paths)
		if pIsDir(path):
			dirname, filename = path, "tempfile.tmp"
		elif pIsDir(os.path.split(path)[0]):
			dirname, filename = os.path.split(path)
		else:
			raise NotADirectoryError(f"Neither {path} nor {os.path.split(path)[0]} is an existing directory, thus no unique file can be created there.")
		prefix, ext = os.path.splitext(filename)
		return super().__new__(cls, tempfile.mkstemp(dir=dirname, prefix=prefix+"-[", suffix="]"+ext)[1], purpose=purpose)

class UniqueDirectoryPath(DirectoryPath, Unique):
	"""If path string has a trailing separator (i.e. "/" or "\\") then a directory with a fully random name is created inside of the directory. If no trailing separator exists, then the last """
	
	def __new__(cls, /, p=".", *paths, purpose="w"):
		import tempfile
		path = pJoin(p, *paths)

		if path.endswith(os.path.sep):
			dirname, prefix = path, "tempdir"
		else:
			dirname, prefix = os.path.split(path)
		
		return super().__new__(cls, tempfile.mkdtemp(dir=dirname, prefix=prefix+"-[", suffix="]"), purpose=purpose)

class PathList(tuple):
	"""Is not based on the `list` type, as mutability is not desired, but the name is used for ease of learning for
	lesser experienced maintainers."""
	@overload
	def __new__(cls, iterable): ...
	@overload
	def __new__(cls, *paths): ...
	def __new__(cls, first, *rest):
		if cls is FileList:
			pathCls = FilePath
		elif cls is DirectoryList:
			pathCls = DirectoryPath
		else:
			pathCls = Path
		
		if not rest and not isinstance(first, str):
			paths = tuple(map(pathCls, first))
		else:
			paths = tuple(map(pathCls, (first,) + rest))
		
		if cls is PathList:
			if all(isinstance(p, FilePath) for p in paths):
				return super().__new__(FileList, paths)
			elif all(isinstance(p, DirectoryPath) for p in paths):
				return super().__new__(DirectoryList, paths)
		
		return super().__new__(cls, paths)
	
	def __str__(self):
		return " ".join(self)
	
	def __format__(self, format_spec : str):
		if format_spec.endswith("n"):
			return format(self.name, format_spec.rstrip("n"))
		else:
			return format(" ".join(map(lambda p:"'"+p.strip("'")+"'", self)), format_spec)
	
	def __iter__(self) -> Generator["PathList",None,None]:
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