

import os, shutil, random, sys, __main__
from functools import cached_property
random.seed()

class Path: pass
class DirectoryPath: pass
class FilePath: pass
class PathGroup:
	def __getitem__(self, key):
		pass
class MinimalPathLibrary:
	def __getitem__(self, key):
		pass
class PathLibrary:
	def __getitem__(self, key):
		pass

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
PROGRAM_DIRECTORY = os.path.normpath(os.path.expanduser(os.path.dirname(__main__.__file__))) if hasattr(__main__, "__file__") else os.path.normpath(".")
"""Directory used as `installDir`"""

# OS Alibis
pSep = os.path.sep
"""os.path.sep"""
pJoin = os.path.join
"""os.path.join"""
pExists = os.path.exists
"""os.path.exists"""
pIsAbs = lambda path: os.path.isabs(os.path.normpath(os.path.expanduser(path)))
"""lambda path: os.path.isabs(os.path.normpath(os.path.expanduser(path)))"""
pIsFile = os.path.isfile
"""os.path.isfile"""
pExpUser = os.path.expanduser
"""os.path.expanduser"""
pAbs = lambda path: os.path.abspath(os.path.expanduser(path))
"""lambda path: os.path.abspath(os.path.expanduser(path))"""
pNorm = lambda path: os.path.normpath(os.path.expanduser(path))
"""lambda path: os.path.normpath(os.path.expanduser(path))"""
pDirName = os.path.dirname
"""os.path.dirname"""
pName = lambda path: os.path.basename(os.path.splitext(path)[0])
"""lambda path: os.path.basename(os.path.splitext(path)[0])"""
pExt = lambda path: os.path.splitext(path)[1]
"""lambda path: os.path.splitext(path)[1]"""
