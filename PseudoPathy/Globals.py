

import os, shutil, random, sys, logging
from functools import cached_property
from typing import overload, Literal, Container, Any
from platformdirs import AppDirs

def camelize(string : str):
	return string[0] + string[1:].replace("_", " ").title().replace(" ", "")

class Camelized(type):
	def __init__(self, className, bases, namespace):
		namespace = namespace | {camelize(name):value for name, value in filter(lambda x : not x[0].startswith("_"), namespace.items())}
		for base in bases:
			namespace = namespace | {camelize(name):value for name, value in filter(lambda x : not x[0].startswith("_"), base.items())}
		super().__init__(className, bases, namespace)

class SoftwareDirs(AppDirs, metaclass=Camelized):
	@property
	def SOFTWARE_NAME(self):
		return self.appname
	
	@SOFTWARE_NAME.setter
	def SOFTWARE_NAME(self, value):
		self.appname = value
	
	@SOFTWARE_NAME.deleter
	def SOFTWARE_NAME(self):
		self.appname = ""
	
	def __getattribute__(self, name: str) -> Any:
		from Paths import DirectoryPath
		if name.endswith("Dir"):
			return DirectoryPath(super().__getattribute__(name))
		else:
			return super().__getattribute__(name)
	
	siteCacheDir : str
	userCacheDir : str
	siteConfigDir : str
	userConfigDir : str
	iterConfigDir : str
	siteDataDir : str
	userDataDir : str
	iterDataDir : str
	siteRuntimeDir : str
	userRuntimeDir : str
	userDocumentsDir : str
	userLogDir : str
	userStateDir : str


random.seed()

def unCapitalize(string):
	return f"{string[0].lower()}{string[1:]}"

class PathPermMeta(type):
	def __instancecheck__(self, instance: Any) -> bool:
		return getattr(instance, unCapitalize(self.__name__), None) is not None or os.access(str(instance), mode=self.code)

class Readable(metaclass=PathPermMeta):
	code : int = 4
class Writable(metaclass=PathPermMeta):
	code : int = 2
class Executable(metaclass=PathPermMeta):
	code : int = 1
class FullPerms(metaclass=PathPermMeta):
	code : int = 7

LOGGER = logging.Logger("PseudoPathy")
"""`logging.Logger` object to use."""

DISPOSE : bool = True

USER_DIRECTORY = os.path.expanduser("~")

# OS Alibis
from PseudoPathy.PathShortHands import pSep, pJoin, pExists, pIsAbs, pIsFile, pIsDir, pExpUser, pAbs, pNorm, pReal, pDirName, pName, pExt, pAccess, pBackAccess, pMakeDirs, PERMS_LOOKUP_OS, PERMS_LOOKUP

## Library Globals

COMMON_GROUPS_DOCSTRING = """
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

PATH_LIBRARY_DOCSTRING = """
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