
from PseudoPathy.Globals import *
from PseudoPathy.Paths import Path, FilePath, DirectoryPath, DisposablePath
from PseudoPathy.Group import PathGroup

def createTemp(path : Path|PathGroup, prefix : str="", ext : str=None):
	"""Finds a randomized name that does not already exist in the given directory. If a directory is created, then the directory is created as well."""
	if type(path) not in [Path, DirectoryPath, FilePath, DisposablePath, PathGroup]:
		if pIsFile(path):
			path = FilePath(path)
		else:
			path = DirectoryPath(path)
	elif type(path) is PathGroup:
		path = path.writable
	outPath = getUniqueName(path, prefix=prefix, ext=ext)
	try:
		pMakeDirs(outPath)
	except:
		return None
	return outPath

def getUniqueName(path : Path, prefix : str="", ext : str=None):
	"""Finds a randomized name that does not already exist in the given directory."""
	n=0
	while n < 1000000 and os.path.exists(path > (newName := "{}_{}{}{}".format(prefix, *random.random().as_integer_ratio(), "."+ext.lstrip(".") if ext is not None else ""))):
		n+=1
	if not n < 1000000:
		raise FileExistsError(f"Could not generate random file/directory name for path='{path}' after {n} attempts")
	return path > newName