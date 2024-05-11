
from PseudoPathy.Globals import *
from PseudoPathy.Paths import Path

import re
# formatPattern = re.compile("^(?P<filler>.)??(?P<direction>[<^>])?(?P<length>[0-9]+)?[.]?(?P<precision>[0-9]+)?(?P<type>[a-z])?$")
_formatPat = re.compile(r"(\d+)[\[](.+?)[\]]")

_LINE_SKIP = object()

class PathGroup:
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
	
	@property
	def writable(self): return self.create(purpose="w")
	@property
	def readable(self): return self.find(purpose="r")
	@property
	def executable(self): return self.find(purpose="x")
	@property
	def fullPerms(self): return self.create(purpose="rwx")

	def __init__(self, *paths : tuple[str], purpose="r"):
		from PseudoPathy.Paths import Path
		self.defaultPurpose = purpose
		self._roots = [p if isinstance(p, Path) else Path(p) for p in paths]

	def __or__(self, right):
		if type(right) is PathGroup:
			return PathGroup(*self._roots, *right._roots, purpose=right.defaultPurpose)
		else:
			return PathGroup(*self._roots, right, purpose=self.defaultPurpose)
	
	def __ror__(self, left):
		if type(left) is PathGroup:
			return PathGroup(*left._roots, *self._roots, purpose=left.defaultPurpose+self.defaultPurpose)
		else:
			return PathGroup(left, *self._roots, purpose=self.defaultPurpose)
		
	def __ior__(self, right):
		if type(right) is PathGroup:
			self._roots += right._roots
		else:
			self._roots.append(right)
	
	def __add__(self, right):
		return PathGroup(*[r + right for r in self._roots], purpose=self.defaultPurpose)
	
	def __iadd__(self, right):
		for i in range(len(self._roots)):
			self._roots[i] = self._roots[i] + right

	def __sub__(self, right):
		return PathGroup(*[r - right for r in self._roots], purpose=self.defaultPurpose)
	
	def __isub__(self, right):
		for i in range(len(self._roots)):
			self._roots[i] = self._roots[i] - right

	def __truediv__(self, right):
		return PathGroup(*(r / right for r in self._roots), purpose=self.defaultPurpose)
	
	def __rtruediv__(self, left):
		if type(left) is PathGroup: return NotImplemented
		return PathGroup(*(left / r for r in self._roots), purpose=self.defaultPurpose)
	
	def __itruediv__(self, right):
		self._roots = [r / right for r in self._roots]
	
	def __contains__(self, path : str):
		for r in self._roots:
			if os.path.exists(r / path):
				return True
		return False
	
	def __iter__(self):
		return iter(self._roots)

	def __str__(self, indentSize=1, indentChar="  "):
		indent = indentChar * indentSize
		ret = [f"PathGroup at 0x{id(self):0>16x}:"]
		for p in self._roots:
			ret.append(f"{indent} | {format(p, '<'+str(80-len(indent)-3))}")
		return "\n".join(ret)

	def __format__(self, fs):
		m = _formatPat.match(fs)
		if m is not None:
			indentSize, indentChar = m.groups()
			return self.__str__(indentSize=indentSize, indentChar=indentChar)
		else:
			return self.__str__()

	def __getitem__(self, path : str, purpose:str=None) -> Path:
				
		for r in self._roots:
			if pAccess(r / path, purpose or self.defaultPurpose):
				return Path(r / path)
		return None

	def __eq__(self, other):
		if type(other) != type(self):
			return False
		return self._roots == other._roots
	
	def endswith(self, string : str):
		return all(r.endswith(string) for r in self._roots)

	def find(self, path : str="", purpose : str=None):
		'''Looks for path in the group of directories and returns first found path.'''
		return self.__getitem__(path, purpose=purpose)

	def findall(self, path : str="", purpose : str=None):
		return [Path(r / path) for r in self._roots if pAccess(r / path, purpose or self.defaultPurpose)]
	
	def create(self, path : str="", purpose : str=None, others : str="r") -> Path:
		'''Should not be used to create files, only directories!'''
		# Try to find existing path for purpose(s).
		for r in self._roots:
			if pAccess(r / path, purpose or self.defaultPurpose):
				return r / path
		# Try to make a path for purpose(s).
		for r in self._roots:
			if (out := r.create(path=path, purpose=purpose or self.defaultPurpose, others=others)) is not None:
				return out
		return None

