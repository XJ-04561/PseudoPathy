

from PseudoPathy.Globals import *
from PseudoPathy.Paths import Path, FilePath, DirectoryPath
from PseudoPathy.Group import PathGroup
from This import this

_NOT_SET = object()

class PathLibrary:
	"""Same functionalities as SoftwareLibrary, but with no default directories and groups."""
	_lib : dict[str,Path] = _NOT_SET
	
	def __init__(self, *args, **kwargs):
		self._lib = {}
		for name, path in filter(lambda x: x[0] not in self.__dict__, kwargs.items()):
			if type(path) in [Path, DirectoryPath, FilePath, PathGroup]:
				self._lib[name] = path
			else:
				try:
					self._lib[name] = Path(path)
				except:
					# Not acceptable data type for a path.
					pass
	
	def __contains__(self, item):
		if item in self._lib:
			return True
		elif any(self[a] == item for a in dir(self)):
			return True
		else:
			return False
	
	def __iter__(self):
		return iter(self._lib.items())

	def __getitem__(self, key):
		return getattr(self.__getattribute__(key))
	
	def __setitem__(self, key, value):
		setattr(self, key, value)
	
	def __getattr__(self, name):
		return self._lib.get(name)
	
	def __setattr__(self, name, value):
		if name in type(self).__dict__:
			super().__setattr__(name, value)
		else:
			self._lib[name] = value

	def __delitem__(self, key):
		if key in self.__dict__:
			super().__delattr__(key)
		else:
			del self._lib[key]
	
	def __delattr__(self, name):
		if name in self.__dict__:
			super().__delattr__(name)
		else:
			del self._lib[name]
	
	def __str__(self):
		ret = ["Directories in Library at 0x{:0>16}:\n".format(hex(id(self))[2:])]
		for name in sorted(self._lib.keys()):
			p = self._lib[name]
			if type(p) is PathGroup:
				ret.append(f"  |||| {name:<20} {p:<30}")
			else:
				d = "d" if os.path.isdir(p) or (not os.path.isfile(p) and "." not in os.path.split(p.rstrip(os.path.sep))[-1]) else "-"
				
				r = "r" if pAccess(p, "r") else "-"
				w = "w" if pAccess(p, "w") else "-"
				x = "x" if pAccess(p, "x") else "-"
				ret.append(f"  {d+r+w+x} {name:<20} {p:<28}")
		return "\n".join(ret)
	
	def __len__(self):
		return len(self._lib)
	
	def clear(self):
		self._lib = {}

	def access(self, path, mode : str="rwx", create : bool=False):
		'''Throws appropriate errors if access is not possible.'''
		
		if not pExists(path):
			if create:
				LOGGER.debug(f"Path does not exist, creating it instead: '{path}'")
				pMakeDirs(path)
			else:
				LOGGER.error(f"Path does not exist: '{path}'")
				raise FileNotFoundError(f"Path does not exist: '{path}'")
		
		if not all(os.access(path, PERMS_LOOKUP_OS[c]) for c in mode):
			LOGGER.error("Missing {perms} permissions for path: '{path}'".format(path=path, perms="+".join([PERMS_LOOKUP[c] for c in mode if not self.perms[path][c]])))
			raise PermissionError("Missing {perms} permissions for path: '{path}'".format(path=path, perms="+".join([PERMS_LOOKUP[c] for c in mode if not self.perms[path][c]])))
		
		return True
	
	def accessible(self, path, mode : str="rwx", create : bool=False):
		'''Returns True/False for the accessibility question.'''
		
		if not pExists(path):
			if create:
				LOGGER.debug("Path does not exist, creating it instead: '{}'".format(path))
				pMakeDirs(path)
			else:
				LOGGER.debug("Path does not exist: '{}'".format(path))
				return False
		
		if not all(os.access(path, PERMS_LOOKUP_OS[c]) for c in mode):
			LOGGER.debug("Missing {perms} permissions for path: '{path}'".format(path=path, perms="+".join([PERMS_LOOKUP[c] for c in mode if not self.perms[path][c]])))
			return False
		
		return True

class SoftwareLibrary(PathLibrary, SoftwareDirs):
	
	SOFTWARE_NAME : str
	"""This is what you want to override for installation/software-related files to go into a folder named after your Software"""
	
	workDir : str	= os.curdir
	userDir			= USER_DIRECTORY

