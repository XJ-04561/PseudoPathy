

from _globals import *

from PseudoPathy.Paths import *

def createTemp(path : Path|PathGroup, prefix : str="", ext : str=None):
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
	newName = "{}_{}{}{}".format(prefix, *random.random().as_integer_ratio(), "."+ext.lstrip(".") if ext is not None else "")
	n=0
	while os.path.exists(path > newName):
		newName = "{}_{}{}{}".format(prefix, *random.random().as_integer_ratio(), "."+ext.lstrip(".") if ext is not None else "")
		if n>1000000-1:
			raise FileExistsError(f"Could not generate random file/directory name for path='{path}' after {n} attempts")
		n+=1
	return path > newName