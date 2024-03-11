

from PseudoPathy.Globals import *
from PseudoPathy.Paths import Path, FilePath, DirectoryPath, DisposablePath
from PseudoPathy.Group import PathGroup

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
		return object.__getattribute__(self, "_lib").items()

	def __getitem__(self, key):
		return self.__getattribute__(key)
	
	def __setitem__(self, key, value):
		self._lib[key] = value
	
	def __getattr__(self, name):
		return self._lib.get(name)
	
	def __setattr__(self, name, value):
		self._lib[name] = value

	def __repr__(self):
		return "<{}.{} at 0x{:0>16}>".format(__name__, type(self).__name__, hex(id(self))[2:])
	
	def __str__(self):
		ret = ["Directories in Library at 0x{:0>16}:\n".format(hex(id(self))[2:])]
		for name in sorted(self._lib.keys()):
			ret.append( f"\t{name:<24} = {self._lib[name]!s}")
		return "\n".join(ret)

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

class CommonGroups(MinimalPathLibrary):
	"""
	Meant to easily form `PathGroup` objects with combinations of the three common directories `workDir`,
	`userDir`, and `installDir`. If using the python shell `installDir` will be set at time of import
	to os.path.normpath(".").
	```python
	def __init__(self):
		self.locals=PathGroup(self.workDir, self.userDir)
		self.personal=PathGroup(self.userDir, self.workDir)
		self.shared=PathGroup(self.installDir, self.userDir, self.workDir)
		self.withBackup=PathGroup(self.workDir, self.installDir, self.userDir)

		# Acronymized `PathGroup`s of every combination of the three default directories.
		self.W = PathGroup(self.workDir)
		self.U = PathGroup(self.userDir)
		self.I = PathGroup(self.installDir)
		self.WU = PathGroup(self.workDir, self.userDir)
		self.UW = PathGroup(self.userDir, self.workDir)
		self.WI = PathGroup(self.workDir, self.installDir)
		self.IW = PathGroup(self.installDir, self.workDir)
		self.UI = PathGroup(self.userDir, self.installDir)
		self.IU = PathGroup(self.installDir, self.userDir)
		self.WUI = PathGroup(self.workDir, self.userDir, self.installDir)
		self.WIU = PathGroup(self.workDir, self.installDir, self.userDir)
		self.UWI = PathGroup(self.userDir, self.workDir, self.installDir)
		self.IWU = PathGroup(self.installDir, self.workDir, self.userDir)
		self.UIW = PathGroup(self.userDir, self.installDir, self.workDir)
		self.IUW = PathGroup(self.installDir, self.userDir, self.workDir)
	```
	"""

	locals : PathGroup
	personal : PathGroup
	shared : PathGroup
	withBackup : PathGroup
	
	W : PathGroup
	U : PathGroup
	I : PathGroup
	WU : PathGroup
	UW : PathGroup
	WI : PathGroup
	IW : PathGroup
	UI : PathGroup
	IU : PathGroup
	WUI : PathGroup
	WIU : PathGroup
	UWI : PathGroup
	IWU : PathGroup
	UIW : PathGroup
	IUW : PathGroup

	@property
	def workDir(self):		return self._lib.get("workDir") or DirectoryPath(pAbs(os.curdir))
	@property
	def userDir(self):		return self._lib.get("userDir") or DirectoryPath("~")
	@property
	def installDir(self):	return self._lib.get("installDir") or DirectoryPath(PROGRAM_DIRECTORY)

	@workDir.setter
	def workDir(self, path):	self._lib["workDir"] = Path(path)
	@userDir.setter
	def userDir(self, path):	self._lib["userDir"] = Path(path)
	@installDir.setter
	def installDir(self, path):	self._lib["installDir"] = Path(path)

	def __init__(self, *args, **kwargs):
		super(CommonGroups, self).__init__(self, *args, **kwargs)

		self.locals=PathGroup(self.workDir, self.userDir)
		self.personal=PathGroup(self.userDir, self.workDir)
		self.shared=PathGroup(self.installDir, self.userDir, self.workDir)
		self.withBackup=PathGroup(self.workDir, self.installDir, self.userDir)
		# Acronymized `PathGroup`s of every combination of the three default directories.
		self.W = PathGroup(self.workDir)
		self.U = PathGroup(self.userDir)
		self.I = PathGroup(self.installDir)
		self.WU = PathGroup(self.workDir, self.userDir)
		self.UW = PathGroup(self.userDir, self.workDir)
		self.WI = PathGroup(self.workDir, self.installDir)
		self.IW = PathGroup(self.installDir, self.workDir)
		self.UI = PathGroup(self.userDir, self.installDir)
		self.IU = PathGroup(self.installDir, self.userDir)
		self.WUI = PathGroup(self.workDir, self.userDir, self.installDir)
		self.WIU = PathGroup(self.workDir, self.installDir, self.userDir)
		self.UWI = PathGroup(self.userDir, self.workDir, self.installDir)
		self.IWU = PathGroup(self.installDir, self.workDir, self.userDir)
		self.UIW = PathGroup(self.userDir, self.installDir, self.workDir)
		self.IUW = PathGroup(self.installDir, self.userDir, self.workDir)

class PathLibrary(MinimalPathLibrary):
	"""
		This structure allows for defining file managing as well and making sure that directory and file path
		information is simply passed around by handing around the same 'Library'.

		Contains some default paths for (and called as) `workDir`, `userDir`, `installDir`. All of which can be overriden by
		assignment.
		`os` functions are used for default workDir and userDir. __main__ is used for installDir, which means that if
		using the python shell `installDir` will be set at time of import to os.path.normpath(".").

		Also contains a default called `commonGroups`, which is a `MinimalPathLibrary` which only contains `PathGroup`
		attributes with different order of priorities to look through `workDir`, `userDir`, and `installDir`.
		They are defined as such:
		```python
		@cached_property
		def commonGroups(self):
			return MinimalPathLibrary(
				locals=PathGroup(self.workDir, self.userDir),
				personal=PathGroup(self.userDir, self.workDir),
				shared=PathGroup(self.installDir, self.userDir, self.workDir),
				withBackup=PathGroup(self.workDir, self.installDir, self.userDir),
				...
			)
		```
		Only the named ones are shown above. All combinations exist as capitalized acronyms of the directories,
		ex: `commonGroups.UWI` will get you a PathGroup with an order of userDir, workDir, installDir.
	"""
	
	commonGroups : CommonGroups

	@property
	def workDir(self):		return self._lib.get("workDir") or DirectoryPath(pAbs(os.curdir))
	@property
	def userDir(self):		return self._lib.get("userDir") or DirectoryPath("~")
	@property
	def installDir(self):	return self._lib.get("installDir") or DirectoryPath(PROGRAM_DIRECTORY)
	
	@workDir.setter
	def workDir(self, path):	self.commonGroups.workDir = self._lib["workDir"] = Path(path)
	@userDir.setter
	def userDir(self, path):	self.commonGroups.userDir = self._lib["userDir"] = Path(path)
	@installDir.setter
	def installDir(self, path):	self.commonGroups.installDir = self._lib["installDir"] = Path(path)
	
	def __init__(self, *args, **kwargs):
		super(PathLibrary, self).__init__(self, *args, **kwargs)
		object.__setattr__(self, "commonGroups", CommonGroups())
	
	def __str__(self):
		# Works nicely, don't question it.
		ret = ["Directories in Library at 0x{:0>16}:\n".format(hex(id(self))[2:])]
		ret.append( f"\t{'workDir':<24} = {self.workDir!s}")
		ret.append( f"\t{'userDir':<24} = {self.userDir!s}")
		ret.append( f"\t{'installDir':<24} = {self.installDir!s}")
		ret.append("")
		for name in sorted(self._lib.keys()):
			if name == "workDir" or name == "userDir" or name == "installDir": continue
			ret.append( f"\t{name:<24} = {self._lib[name]!s}")
		return "\n".join(ret)

