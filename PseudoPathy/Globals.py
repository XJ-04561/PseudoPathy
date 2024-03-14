

import os, shutil, random, sys, __main__
from functools import cached_property
random.seed()



class DummyLogger:
	"""A dummy logger for all Path derived objects to log to, except it does not
	perform logging. To enable logging you simply assign a working logger to the
	'logger' attribute of the Path class."""
	def debug(self, *args, **kwargs): pass
	def info(self, *args, **kwargs): pass
	def warning(self, *args, **kwargs): pass
	def error(self, *args, **kwargs): pass
	def critical(self, *args, **kwargs): pass


PERMS_LOOKUP = {"r":"read", "w":"write", "x":"execute"}
"""Dictionary for lookup of full names for permission type initials using lower case initials as keys. ie. `"r"` -> `"read"`, `"w"` -> `"write"`, or `"x"` -> `"execute"`."""
PERMS_LOOKUP_OS = {"r":os.R_OK, "w":os.W_OK, "x":os.X_OK}
"""Dictionary for lookup of `os` permission types using lower case initials as keys. ie. `"r"`, `"w"`, or `"x"`."""
LOGGER = DummyLogger()
"""`logging.Loggger` object to use."""
DISPOSE : bool = True
"""Whether `DisposablePath` objects should shutil.rmtree(self) when deleted/trash-collected."""
PROGRAM_DIRECTORY = os.path.join(os.environ.get("programFiles") or "/srv", os.path.splitext(__main__.__file__.split(os.path.sep)[-2])[0]) if hasattr(__main__, "__file__") else os.path.normpath(".")
"""Directory used as `installDir`"""

# OS Alibis
from PseudoPathy.PathShortHands import pSep, pJoin, pExists, pIsAbs, pIsFile, pExpUser, pAbs, pNorm, pDirName, pName, pExt, pBackAccess, pMakeDirs

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