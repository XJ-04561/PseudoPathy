
from PseudoPathy.Globals import *
from PseudoPathy.Paths import Path

import re
formatPattern = re.compile("^(?P<filler>.)??(?P<direction>[<^>])?(?P<length>[0-9]+)?[.]?(?P<precision>[0-9]+)?(?P<type>[a-z])?$")

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
		ret = ["PathGroup:"]
		for root in self._roots:
			d = "d" if os.path.isdir(root) or (not os.path.isfile(root) and "." not in os.path.split(root.rstrip(os.path.sep))[-1]) else "-"
			
			r = "r" if os.access(root, PERMS_LOOKUP_OS["r"]) else "-"
			w = "w" if os.access(root, PERMS_LOOKUP_OS["w"]) else "-"
			x = "x" if os.access(root, PERMS_LOOKUP_OS["x"]) else "-"

			ret.append(f"  {d}{r}{w}{x} {root}")
		return "\n".join(ret)
	
	def __format__(self, format_spec) -> str:
		ret = ["PathGroup:"]
		match = formatPattern.match(format_spec)
		fill = match["filler"] or " "
		length = match["length"] or 1
		length = int(length)

		for root in self._roots:
			d = "d" if os.path.isdir(root) or (not os.path.isfile(root) and "." not in os.path.split(root.rstrip(os.path.sep))[-1]) else "-"
			
			r = "r" if pAccess(root, "r") else "-"
			w = "w" if pAccess(root, "w") else "-"
			x = "x" if pAccess(root, "x") else "-"

			ret.append(f"{fill*length}{d}{r}{w}{x} {root}")
		return "\n".join(ret)

	def __getitem__(self, path : str, purpose:str=None) -> Path:
		if purpose is None:
			purpose = self.defaultPurpose
		
		for r in self._roots:
			if pAccess(r > path, purpose):
				return Path(r > path)
		return None
	
	def find(self, path : str="", purpose:str=None):
		'''Looks for path in the group of directories and returns first found path.'''
		return self.__getitem__(path, purpose=purpose)

	def forceFind(self, path : str="", purpose:str=None):
		'''Looks for path in the group of directories and returns first found path. Will try to create and return path
		in the group if it does not currently exist.'''
		return self.__getitem__(path, purpose=purpose) or self.create(path=path, purpose=purpose)
	
	def create(self, path : str="", purpose : str=None) -> Path:
		'''Should not be used to create files, only directories!'''
		if purpose is None:
			purpose = self.defaultPurpose
		# Try to find existing path for purpose(s).
		for r in self._roots:
			if pAccess(r > path, purpose):
				return r > path
		# Try to make a path for purpose(s).
		for r in self._roots:
			if pBackAccess(r, "w"):
				try:
					pMakeDirs(r > path)
					return r > path
				except Exception as e:
					# Happens if write permission exists for parent directories but not for lower level directories.
					print(e)
					LOGGER.exception(e, stack_level=logging.DEBUG)
			else:
				LOGGER.debug(f"pBackAccess({r!r}, \"w\") is False")
		return None