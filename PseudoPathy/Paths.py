

from typing import Any
from PseudoPathy.Globals import *
import PseudoPathy.Globals as Globals


PATH_SPLIT_PATTERN = re.compile((
	r"['][^']*?[']"
	r"|[\"][^\"]*?[\"]"
	r"|^[^/'\"]+(?=[/])?"
	r"|^/"
	r"|(?<=[/])[^/'\"]+?$"
	r"|(?<=[/]).*?(?=[/])"
).replace("/", os.sep))

class Path(Pathy, str):
	""""""

	defaultPurpose : str
	segments : tuple[str]

	writable : "Path"
	"""The first path with writing permissions. If none exists, then tries to create one (Given that at least one path is not existent on the system)"""
	readable : "Path"
	"""The first path with reading permissions."""
	executable : "Path"
	"""The first path with execution permissions."""
	fullPerms : "Path"
	"""The first path with full permissions. If none exists, then tries to create one (Given that at least one path is not existent on the system)"""
	exists : bool
	"""Whether the directory/file exists on the system."""

	@property
	def writable(self): return self.find(purpose="w") or self.create(purpose="w")
	@property
	def readable(self): return self.find(purpose="r")
	@property
	def executable(self): return self.find(purpose="x")
	@property
	def fullPerms(self): return self.create(purpose="rwx")

	@property
	def hasMagic(self) -> bool:
		return glob.has_magic(self)

	@property
	def filemode(self) -> str:
		return stat.filemode(self.stat.mode)
	
	@property
	def stat(self) -> Stat:
		return Stat(self)
	@property
	def lstat(self) -> LStat:
		return LStat(self)
	
	@property
	def exists(self): return pExists(self)

	@property
	def directory(self):
		return DirectoryPath(os.path.split(self)[0]) if "." in os.path.split(self)[1][1:] else self
	
	@property
	def file(self):
		return FilePath(os.path.split(self)[1]) if "." in os.path.split(self)[1][1:] else None

	@overload
	def __new__(cls, /, p=".", *paths, purpose="r", escape : bool=False): ...
	def __new__(cls, /, p=".", *paths, purpose=None, escape : bool=False):

		if type(p) is cls and not paths:
			if escape:
				obj = super().__new__(cls, glob.escape(p))
				obj.segments = tuple(PATH_SPLIT_PATTERN.findall(obj))
				obj.defaultPurpose = purpose if purpose is not None else "r"
				return obj
			if purpose is not None:
				p.defaultPurpose = purpose
			return p
		elif paths or isinstance(p, str):
			joined = pJoin(p, *paths)
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
		obj.segments = tuple(PATH_SPLIT_PATTERN.findall(obj))
		obj.defaultPurpose = purpose if purpose is not None else "r"
		return obj
	
	def __add__(self, right):
		if isinstance(right, Path):
			return type(right)(*self.segments[:-1], self.segments[-1]+right, purpose=self.defaultPurpose)
		elif isinstance(right, str):
			return Path(str.__add__(self, right), purpose=self.defaultPurpose)
		else:
			return NotImplemented

	def __radd__(self, left):
		if not isinstance(left, str):
			return NotImplemented
		elif pIsAbs(self):
			return type(self)(self.segments[0], left+(self.segments[1] if len(self.segments) > 1 else ""), *self.segments[2:], purpose=self.defaultPurpose)
		else:
			return type(self)(left+self.segments[0], *self.segments[2:], purpose=self.defaultPurpose)
		
	def __sub__(self, right):
		return type(self)(str.__add__(self.rstrip(os.path.sep), right), purpose=self.defaultPurpose)

	def __truediv__(self, right):
		if right is None:
			return self
		elif isinstance(right, Path):
			return type(right)(self, right, purpose=getattr(right, "defaultPurpose", self.defaultPurpose))
		else:
			return Path(self, right, purpose=getattr(right, "defaultPurpose", self.defaultPurpose))
	
	def __rtruediv__(self, left):
		return type(self)(left, self, purpose=self.defaultPurpose)

	def __or__(self, right : "Path|PathGroup"):
		from PseudoPathy.Groups import PathGroup
		if not isinstance(right, str) and isinstance(right, (Iterable, Iterator)):
			return PathGroup([self] + list(right), purpose=getattr(right, "defaultPurpose", self.defaultPurpose))
		else:
			return PathGroup([self, right], purpose=getattr(right, "defaultPurpose", self.defaultPurpose))
	
	def __ror__(self, left : "Path|PathGroup"):
		from PseudoPathy.Groups import PathGroup
		if not isinstance(left, str) and isinstance(left, (Iterable, Iterator)):
			return PathGroup(list(left) + [self], purpose=self.defaultPurpose or getattr(left, "defaultPurpose", None))
		else:
			return PathGroup([left, self], purpose=self.defaultPurpose or getattr(left, "defaultPurpose", None))
		
	def __iter__(self) -> list["Path"]:
		return iter([self])
	
	def __contains__(self, item):
		return True if next(glob.iglob(self / item), None) is not None else False
	
	# def __getitem__(self, segmentIndex : int|slice) -> str:
	# 	return self.segments[segmentIndex]
	
	def __format__(self, fs):
		if fs.endswith("s"):
			return f"{self.filemode} {format(str(self), fs[:-1])}"
		else:
			return format(str(self), fs)
	
	def escape(self):
		return type(self)(self, purpose=self.defaultPurpose, escape=True)

	def find(self, path : str=None, *, purpose : str=None) -> "PathList|Path|None":
		
		path = self / path
		if pAccess(path, purpose or self.defaultPurpose):
			return path
		elif res := sorted(list(filter(lambda x:pAccess(x, purpose or self.defaultPurpose), glob.iglob(os.path.expandvars(os.path.expanduser(str(path))), recursive=True)))):
			return PathList(res) if len(res) > 1 else Path(res[0])
		else:
			return None

	def prepend(self, path):
		return path / self

	def append(self, path):
		return self / path

	def create(self, path : str=None, purpose : str=None, others : str="r") -> "Path|None":
		'''Should not be used to create files, only directories!'''
		purpose = purpose or self.defaultPurpose
		path = self / path
		
		if pAccess(path, purpose):
			return path
		
		if pBackAccess(self, "w"): # Try to make a path for purpose(s).
			try:
				pMakeDirs(path)
				return path
			except:
				pass
		else:
			LOGGER.debug(f"pBackAccess({self!r}, \"w\") is False")
		return None

	def format(self, *args, **kwargs):
		return type(self)(str.format(self, *args, **kwargs))

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
		return ".".join(list(itertools.dropwhile(lambda x:x=="", self.file.split(".")))[1:])
	@property
	def name(self) -> str:
		return ".".join([*itertools.takewhile(lambda x:x=="", self.file.split(".")), next(filter(None, self.file.split(".")), "")])
	
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

try:
	from PseudoPathy.Groups import PathGroup
	from PseudoPathy.Lists import PathList, DirectoryList, FileList
except ImportError:
	pass