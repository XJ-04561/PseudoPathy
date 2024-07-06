
from PseudoPathy import *
from PseudoPathy.ShortHands import pSep

def test_compatibility():
	import os
	abspath = os.path.abspath("/")
	userpath = os.path.expanduser("~")

	assert Path(abspath) == abspath
	assert Path(userpath) == userpath


	assert Path(abspath) / "Hello" == os.path.join(abspath, "Hello")
	assert Path(userpath) / "Hello" == os.path.join(userpath, "Hello")
	assert Path(abspath) + "Hello" == abspath + "Hello"
	assert Path(abspath, "") - "Hello" == abspath.rstrip(pSep) + "Hello"

	import sys
	execDir, execFile = os.path.split(sys.executable)
	assert PathGroup([sys.executable, os.path.split(sys.executable)[0]]) == (Path(sys.executable) | Path(os.path.split(sys.executable)[0]))
	assert PathGroup(
		[execDir,
		os.path.split(execDir)[0]]
		).find(execFile) == sys.executable

def test_appdirs():
	
	lib = SoftwareLibrary()

	for attr in filter(lambda x : not x.startswith("_"), object.__dir__(lib)):
		assert hasattr(lib, attr), f"SoftwareLibrary does not have access to expected attribute {attr!r}"
		if attr in ["AUTHOR_NAME", "VERSION_NAME"]: continue
		assert getattr(lib, attr) is not None, f"SoftwareLibrary attribute {attr!r} is None"

def test_print():

	class MyLibrary(SoftwareLibrary):
		SOFTWARE_NAME = "MyApp"
		VERSION_NAME = "ALPHA"

	lib = MyLibrary()
	print(lib)
	assert True
