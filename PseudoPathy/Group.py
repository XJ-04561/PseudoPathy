
from PseudoPathy.Globals import *
from PseudoPathy.Paths import Path, FilePath, DirectoryPath

import re
# formatPattern = re.compile("^(?P<filler>.)??(?P<direction>[<^>])?(?P<length>[0-9]+)?[.]?(?P<precision>[0-9]+)?(?P<type>[a-z])?$")
_formatPat = re.compile(r"^(.+?)([<^>])(\d+?)(.*)$")

_LINE_SKIP = object()

class PathGroup(Pathy):
	""""""

	_roots : list[Path]
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
	"""Whether any of the directories/files exist on the system."""

	@property
	def writable(self): return self.create(purpose="w")
	@property
	def readable(self): return self.find(purpose="r")
	@property
	def executable(self): return self.find(purpose="x")
	@property
	def fullPerms(self): return self.create(purpose="rwx")

	@property
	def exists(self): return any(pExists(p) for p in self)

	@property
	def directory(self):
		return PathGroup(r.directory for r in self._roots)
	
	@property
	def file(self):
		return PathGroup(r.file for r in self._roots)
	@overload
	def __new__(cls : type["PathGroup"], paths : Iterable[Union[str, Path, "PathGroup", Iterator]], purpose : str="r"): ...
	def __new__(cls : type["PathGroup"], paths : Iterable[Union[str, Path, "PathGroup", Iterator]], purpose : str=None):
		
		if type(paths) is cls or isinstance(paths, PathGroup) and cls is PathGroup:
			return paths
		
		if isinstance(paths, Path):
			paths = (paths, )
		elif isinstance(paths, str):
			paths = tuple(paths.split(os.pathsep))
		elif not isinstance(paths, (Iterable, Iterator)):
			paths = (paths,)
		elif isinstance(paths, Iterator):
			paths = tuple(paths)

		if cls is not PathGroup:
			obj = super().__new__(cls)
		elif all(isinstance(p, FilePath) for p in paths):
			obj = super().__new__(FileGroup)
		elif all(isinstance(p, DirectoryPath) for p in paths):
			obj = super().__new__(DirectoryGroup)
		else:
			obj = super().__new__(cls)
		
		if isinstance(obj, FileGroup):
			PathClass = FilePath
		elif isinstance(obj, DirectoryGroup):
			PathClass = DirectoryPath
		else:
			PathClass = Path

		obj.defaultPurpose = purpose or getattr(obj, "defaultPurpose", None) or "r"
		obj._roots = [PathClass(p) for p in paths]
		return obj
	
	@final
	def __init__(self, paths : Iterable[Union[str, Path, "PathGroup", Iterator]], purpose : str="r"):
		pass

	def __or__(self, right):
		if type(right) is PathGroup:
			return PathGroup(self._roots + right._roots, purpose=right.defaultPurpose)
		else:
			return PathGroup(self._roots + [right], purpose=self.defaultPurpose)
	
	def __ror__(self, left):
		if type(left) is PathGroup:
			return PathGroup(left._roots + self._roots, purpose=left.defaultPurpose+self.defaultPurpose)
		else:
			return PathGroup([left] + self._roots, purpose=self.defaultPurpose)
		
	def __ior__(self, right):
		if type(right) is PathGroup:
			self._roots += right._roots
		else:
			self._roots.append(right)
	
	def __add__(self, right):
		return PathGroup((r + right for r in self._roots), purpose=self.defaultPurpose)
	
	def __iadd__(self, right):
		for i in range(len(self._roots)):
			self._roots[i] = self._roots[i] + right

	def __sub__(self, right):
		return PathGroup((r - right for r in self._roots), purpose=self.defaultPurpose)
	
	def __isub__(self, right):
		for i in range(len(self._roots)):
			self._roots[i] = self._roots[i] - right

	def __truediv__(self, right):
		return PathGroup((r / right for r in self._roots), purpose=self.defaultPurpose)
	
	def __rtruediv__(self, left):
		if type(left) is PathGroup: return NotImplemented
		return PathGroup((left / r for r in self._roots), purpose=self.defaultPurpose)
	
	def __itruediv__(self, right):
		self._roots = [r / right for r in self._roots]
	
	def __contains__(self, path : str):
		for r in self._roots:
			if os.path.exists(r / path):
				return True
		return False
	
	def __iter__(self):
		return iter(self._roots)

	def __str__(self):
		ret = [f"PathGroup at 0x{id(self):0>16x}:"]
		for p in self._roots:
			ret.append(f" | {p:<50s}")
		return "\n".join(ret)

	def __format__(self, fs):
		m = _formatPat.match(fs)
		if m is not None:
			indentChar, direction, indentSize, mode = m.groups()
			return self.__str__().replace("\n", "\n"+indentChar*indentSize)
		else:
			return self.__str__().replace("\n", "\n  ")

	def __getitem__(self, path : str, purpose:str=None) -> Path:
		from PseudoPathy import FilePath, DirectoryPath
		for r in self._roots:
			out = r / path
			if pAccess(out, purpose or self.defaultPurpose):
				return out
		return None

	def __eq__(self, other):
		if isinstance(other, PathGroup):
			return self._roots == other._roots
		elif isinstance(other, str):
			return self._roots == other.split(os.pathsep)
		else:
			return False
	
	def prepend(self, path):
		return path / self

	def append(self, path):
		return self / path

	def endswith(self, string : str):
		return all(r.endswith(string) for r in self._roots)

	def find(self, path : str="", purpose : str=None):
		'''Looks for path in the group of directories and returns first found path.'''
		return self.__getitem__(path, purpose=purpose)

	def findall(self, path : str="", purpose : str=None):
		return tuple(filter(lambda p:pAccess(p,purpose or self.defaultPurpose), map(Path(path).prepend, self._roots)))
	
	def create(self, path : str="", purpose : str=None, others : str="r") -> Path:
		'''Should not be used to create files, only directories!'''
		# Try to find existing path for purpose(s).
		if path:
			paths = tuple(map(lambda r:r / path, self._roots))
		else:
			paths = self._roots
		
		for p in paths:
			if pAccess(p, purpose or self.defaultPurpose):
				return p
		# Try to make a path for purpose(s).
		for p in paths:
			if (out := p.create(purpose=purpose or self.defaultPurpose, others=others)) is not None:
				return out
		return None

class DirectoryGroup(PathGroup, Directory): pass

class FileGroup(PathGroup, File): pass