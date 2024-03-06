
try:
	from PseudoPathy._globals import *
	from PseudoPathy.Paths import Path, FilePath, DirectoryPath, DisposablePath
	from PseudoPathy.Group import PathGroup
except:
	from _globals import *
	from Paths import Path, FilePath, DirectoryPath, DisposablePath
	from Group import PathGroup

class MinimalPathLibrary:
	"""Same functionalities as PathLibrary, but with no default directories and groups."""
	_lib : dict[str,Path]
	
	def __init__(self, *args, **kwargs):
		object.__setattr__(self, "_lib", {})
		for name, path in kwargs.items():
			if type(path) in [Path, DirectoryPath, FilePath, DisposablePath, PathGroup]:
				self._lib[name] = path
			else:
				try:
					if pIsFile(path):
						self._lib[name] = FilePath(path)
					else:
						self._lib[name] = DirectoryPath(path)
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
		return object.__getattribute__(self, "_lib").items()

	def __getitem__(self, key):
		return self.__getattribute__(key)
	
	def __setitem__(self, key, value):
		self._lib[key] = value
	
	def __getattr__(self, name):
		return self._lib[name]
	
	def __setattr__(self, name, value):
		self._lib[name] = value

	def __repr__(self):
		return "<{}.{} at 0x{:0>16}>".format(__name__, type(self).__name__, hex(id(self))[2:])
	
	def __str__(self):
		# Works nicely, don't question it.
		ret = ["Directories in Library at 0x{:0>16}:\n".format(hex(id(self))[2:])]
		for name in sorted(self._lib.keys()):
			ret.append( f"\t{name:<24} = {self._lib[name]}")
		return "\n".join(ret)

	def access(self, path, mode : str="rwx", create : bool=False):
		'''Throws appropriate errors if access is not possible.'''
		
		if not os.path.exists(path):
			if create:
				LOGGER.debug("Path does not exist, creating it instead: '{}'".format(path))
				os.makedirs(path)
			else:
				LOGGER.error("Path does not exist: '{}'".format(path))
				raise FileNotFoundError("Path does not exist: '{}'".format(path))
		
		if not all(os.access(path, PERMS_LOOKUP_OS[c]) for c in mode):
			LOGGER.error("Missing {perms} permissions for path: '{path}'".format(path=path, perms="+".join([PERMS_LOOKUP[c] for c in mode if not self.perms[path][c]])))
			raise PermissionError("Missing {perms} permissions for path: '{path}'".format(path=path, perms="+".join([PERMS_LOOKUP[c] for c in mode if not self.perms[path][c]])))
		
		return True
	
	def accessible(self, path, mode : str="rwx", create : bool=False):
		'''Returns True/False for the accessibility question.'''
		
		if not os.path.exists(path):
			if create:
				LOGGER.debug("Path does not exist, creating it instead: '{}'".format(path))
				os.makedirs(path)
			else:
				LOGGER.debug("Path does not exist: '{}'".format(path))
				return False
		
		if not all(os.access(path, PERMS_LOOKUP_OS[c]) for c in mode):
			LOGGER.debug("Missing {perms} permissions for path: '{path}'".format(path=path, perms="+".join([PERMS_LOOKUP[c] for c in mode if not self.perms[path][c]])))
			return False
		
		return True

class PathLibrary(MinimalPathLibrary):
	"""
		This structure allows for defining file managing as well and making sure that directory and file path
		information is simply passed around by handing around the same 'Library'.

		Contains some default paths for (and called as) workDir, userDir, installDir. All of which can be overriden by assignment.
		os functions are used for default workDir and userDir. sys and os is used for installDir.

		Also contains 
	"""
	
	commonGroups : PathLibrary[PathGroup]

	@property
	def workDir(self):		return self._lib.get("workDir") or DirectoryPath(pAbs(os.path.expandvars(os.curdir)))
	@property
	def userDir(self):		return self._lib.get("userDir") or DirectoryPath(pExpUser("~"))
	@property
	def installDir(self):	return self._lib.get("installDir") or sys.argv[0]
	@cached_property
	def commonGroups(self):
		return MinimalPathLibrary(
			locals=PathGroup(self.workDir, self.userDir),
			personal=PathGroup(self.userDir, self.workDir),
			shared=PathGroup(self.installDir, self.userDir, self.workDir)
		)
	
	def __str__(self):
		# Works nicely, don't question it.
		ret = ["Directories in Library at 0x{:0>16}:\n".format(hex(id(self))[2:])]
		ret.append( f"\t{'workDir':<24} = {self.workDir}")
		ret.append( f"\t{'userDir':<24} = {self.userDir}")
		ret.append( f"\t{'installDir':<24} = {self.installDir}")
		ret.append("")
		for name in sorted(self._lib.keys()):
			if name == "workDir" or name == "userDir" or name == "installDir": continue
			ret.append( f"\t{name:<24} = {self._lib[name]}")
		return "\n".join(ret)