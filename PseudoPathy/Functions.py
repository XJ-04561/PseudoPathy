
import tempfile, random

import PseudoPathy.Globals as Globals
from PseudoPathy.PathShortHands import *
from PseudoPathy.Paths import Path, FilePath, DirectoryPath, DisposablePath
from PseudoPathy.Group import PathGroup

def createTemp(dir : Path|PathGroup=None, prefix : str=None, suffix : str=None, ext : str=None):
	"""Creates a temporary directory/file without race-conditions by
	tempfile.TemporaryDirectory or tempfile.TemporaryFile. To create a file,
	use the 'ext' keyword argument without a leading '.'."""
	if dir is None:
		pass
	elif type(dir) not in [Path, DirectoryPath, FilePath, DisposablePath, PathGroup]:
		try:
			pMakeDirs(os.path.dirname(dir))
		except:
			return None
		if pIsFile(dir):
			dir = FilePath(dir)
		else:
			dir = DirectoryPath(dir)
	elif type(dir) is PathGroup:
		dir = dir.writeable
	
	if ext is None:
		outPath = DirectoryPath(tempfile.TemporaryDirectory(suffix=suffix, prefix=prefix, dir=dir).name)
	else:
		outPath = tempfile.TemporaryFile(suffix=suffix+"."+ext, prefix=prefix, dir=dir)
	
	return outPath

# def getUniqueName(path : Path, prefix : str="", ext : str=None):
# 	"""Finds a randomized name that does not already exist in the given directory."""
# 	n=0
# 	while n < 1000000 and os.path.exists(path > (newName := "{}_{}{}{}".format(prefix, *random.random().as_integer_ratio(), "."+ext.lstrip(".") if ext is not None else ""))):
# 		n+=1
# 	if not n < 1000000:
# 		raise FileExistsError(f"Could not generate random file/directory name for path='{path}' after {n} attempts")
# 	return path > newName