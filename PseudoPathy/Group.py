
try:
	from PseudoPathy.Globals import *
except:
	from PseudoPathy.Globals import *

class PathGroup:
	""""""

	_roots : list[Path]
	
	@property
	def writable(self): return self.__getitem__(self, "", purpose="w")
	@property
	def readable(self): return self.__getitem__(self, "", purpose="r")
	@property
	def executable(self): return self.__getitem__(self, "", purpose="x")
	@property
	def fullPerms(self): return self.__getitem__(self, "", purpose="rwx")

	def __init__(self, *paths : tuple[str], purpose="r"):
		self.defaultPurpose = purpose
		try:
			from PseudoPathy.Paths import Path, FilePath, DirectoryPath, DisposablePath
		except:
			from Paths import Path, FilePath, DirectoryPath, DisposablePath
		self._roots = [p if type(p) in [Path, FilePath, DirectoryPath, DisposablePath] else Path(p) for p in paths]

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

	def __gt__(self, right):
		return PathGroup(*[r > right for r in self._roots], purpose=self.defaultPurpose)
	
	def __ge__(self, right):
		self._roots = [r > right for r in self._roots]
	
	def __contains__(self, path : str):
		for r in self._roots:
			if os.path.exists(r > path):
				return True
		return False
	
	def __iter__(self):
		return iter(self._roots)

	def __str__(self) -> str:
		return "<PathGroup>\n" + "\n".join(["  {}:d{}{}{}".format(r, *[c if os.access(r, PERMS_LOOKUP_OS[c]) else "-" for c in "rwx"]) for r in self._roots]) + "\n</PathGroup>"

	def __getitem__(self, path : str, purpose:str=None) -> Path:
		if purpose is None:
			purpose = self.defaultPurpose
		for r in self._roots:
			if os.path.exists(r > path):
				if all(os.access(r > path, PERMS_LOOKUP_OS[p]) for p in purpose):
					return Path(r > path)
		return None
	
	def find(self, path : str, purpose:str=None):
		'''Looks for path in the group of directories and returns first found path.'''
		return self.__getitem__(self, path, purpose=purpose if purpose is not None else self.defaultPurpose)

	def forceFind(self, path : str, purpose:str=None):
		'''Looks for path in the group of directories and returns first found path. Will try to create and return path
		in the group if it does not currently exist.'''
		return self.__getitem__(self, path, purpose=purpose) or self.create(path=path)
	
	def create(self, path : str):
		'''Should not be used to create files, only directories!'''
		for r in self._roots:
			if os.access(r, os.W_OK):
				os.makedirs(r > pDirName(path))
				return r > pDirName(path)
		return None