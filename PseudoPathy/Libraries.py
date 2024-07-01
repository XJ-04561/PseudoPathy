

from PseudoPathy.Globals import *
from PseudoPathy.Paths import Path, FilePath, DirectoryPath
from PseudoPathy.Groups import PathGroup
from PseudoPathy.Utilities import SoftwareDirs

_formatPat = re.compile(r"^(.+?)([<^>])(\d+?)(.*)$")
_LINE_SKIP = object()

class PathLibrary:
	"""Same functionalities as SoftwareLibrary, but with no default directories and groups."""
	
	def __init__(self, *args, **kwargs):
		for name, path in filter(lambda x: x[0] not in self.__dict__, kwargs.items()):
			if type(path) in [Path, DirectoryPath, FilePath, PathGroup]:
				setattr(self, name, path)
			else:
				try:
					setattr(self, name, Path(path))
				except:
					# Not acceptable data type for a path.
					pass
	
	def __contains__(self, item):
		return hasattr(self, item)
	
	def __iter__(self):
		"""Only iterates through the instance-specific entries, not the class-defined ones."""
		return iter(self.__dict__.items())

	def __getitem__(self, key):
		return getattr(self, key)
	
	def __setitem__(self, key, value):
		setattr(self, key, value)

	def __delitem__(self, key):
		delattr(self, key)
	
	def __str__(self):
		ret = [f"Directories in Library at 0x{id(self):0>16x}:"]
		for name, p in chain(map(lambda x:(x, getattr(self, x)), filter(lambda x:not x.startswith("_") and x not in self.__dict__, dir(type(self)))), [(_LINE_SKIP, _LINE_SKIP)], vars(self).items()):
			if p is _LINE_SKIP:
				ret.append(f" ||{'-'*50}")
			elif isinstance(p, (Path, PathGroup, PathLibrary)):
				ret.append(f" || {name:<20} {p:s}")
		return "\n".join(ret)
	
	def __format__(self, fs):
		m = _formatPat.match(fs)
		if m is not None:
			indentChar, direction, indentSize, mode = m.groups()
			return self.__str__().replace("\n", "\n"+indentChar*indentSize)
		else:
			return self.__str__().replace("\n", "\n  ")
	
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

class SoftwareLibrary(PathLibrary, SoftwareDirs): pass