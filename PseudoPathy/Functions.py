
import tempfile, random

import PseudoPathy.Globals as Globals
from PseudoPathy.PathShortHands import *
from PseudoPathy.Paths import Path, FilePath, DirectoryPath
from PseudoPathy.Group import PathGroup, DirectoryGroup, FileGroup

@Globals.overload
def createTemp(dir : FilePath|FileGroup=None, prefix : str=None, suffix : str=None, ext : str=None) -> FilePath: ...
@Globals.overload
def createTemp(dir : DirectoryPath|DirectoryGroup=None, prefix : str=None, suffix : str=None) -> DirectoryPath: ...
def createTemp(dir : Path|PathGroup=None, prefix : str=None, suffix : str=None, ext : str=None) -> FilePath|DirectoryPath:
	"""Creates a temporary directory/file without race-conditions by
	tempfile.TemporaryDirectory or tempfile.TemporaryFile. To create a file,
	use the 'ext' keyword argument without a leading '.'."""
	if isinstance(dir, Globals.Directory):
		return createTempDir(dir, prefix=prefix, suffix=suffix, ext=ext)
	elif isinstance(dir, Globals.File):
		return createTempFile(dir, prefix=prefix, suffix=suffix, ext=ext)
	elif ext:
		createTempFile(dir, prefix=prefix, suffix=suffix, ext=ext)
	else:
		createTempDir(dir, prefix=prefix, suffix=suffix)

def createTempDir(prefix : str=None, suffix : str=None, *, dir : DirectoryPath|DirectoryGroup=None) -> DirectoryPath:
	if isinstance(dir, Globals.Pathy):
		dir = dir.writable
	else:
		pMakeDirs(dir)
	prefix = f"{prefix}-[" if prefix else "["
	suffix = f"]-{suffix}" if suffix else "]"
	outPath = tempfile.TemporaryDirectory(suffix=suffix, prefix=prefix, dir=dir)
	Globals.OPEN_PATHS.append(outPath)
	return DirectoryPath(outPath.name)

def createTempFile(prefix : str=None, suffix : str=None, ext : str=None, *, dir : DirectoryPath|DirectoryGroup=None) -> FilePath:
	if isinstance(dir, Globals.Pathy):
		dir = dir.writable
	else:
		pMakeDirs(dir)
	prefix = f"{prefix}-[" if prefix else "["
	ext = "" if not ext else (ext if ext.startswith(".") else "."+ext)
	suffix = f"]-{suffix}{ext}" if suffix else "]"
	if "." not in suffix:
		suffix += ".tmp"
	outPath = tempfile.NamedTemporaryFile(suffix=suffix, prefix=prefix, dir=dir)
	Globals.OPEN_PATHS.append(outPath)
	return FilePath(outPath.name)

# def getUniqueName(path : Path, prefix : str="", ext : str=None):
# 	"""Finds a randomized name that does not already exist in the given directory."""
# 	n=0
# 	while n < 1000000 and os.path.exists(path / (newName := "{}_{}{}{}".format(prefix, *random.random().as_integer_ratio(), "."+ext.lstrip(".") if ext is not None else ""))):
# 		n+=1
# 	if not n < 1000000:
# 		raise FileExistsError(f"Could not generate random file/directory name for path='{path}' after {n} attempts")
# 	return path / newName