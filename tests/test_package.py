
from PseudoPathy import *
from PseudoPathy.PathShortHands import pSep

"""
Path
FilePath
DirectoryPath
UniqueFilePath

PathList
PathGroup

PathLibrary
SoftwareLibrary

Functions
PathShortHands
"""

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
	assert PathGroup(sys.executable, os.path.split(sys.executable)[0]) == (Path(sys.executable) | Path(os.path.split(sys.executable)[0]))
	assert PathGroup(
		execDir,
		os.path.split(execDir)[0]
		).find(execFile) == sys.executable

# def test_alias():
# 	from PseudoPathy.Globals import Alias
# 	class A:
# 		a = 2
	
# 	class B(A):
# 		b = Alias["a"] # type: ignore
	
# 	assert A().a == 2, 	   f"A().a == 2 -> {A().a=} == {2=}"
# 	assert B().a == A().a, f"B().a == A().a -> {B().a=} == {A().a=}"
# 	assert B().b == A().a, f"B().b == A().a -> {B().b=} == {A().a=}"

# 	class C(B):
# 		c = Alias["b"] # type: ignore
	
# 	assert C().a == A().a, f"C().a == A().a -> {C().a=} == {A().a=}"
# 	assert C().b == A().a, f"C().b == A().a -> {C().b=} == {A().a=}"
# 	assert C().c == A().a, f"C().c == A().a -> {C().c=} == {A().a=}"

# def test_path_alias():
# 	import os
# 	class A:
# 		a = Path("C:\\", "Users", "fresor", "Documents")
	
# 	class B(A):
# 		b = PathAlias["a"]
	
# 	assert A().a == "C:\\Users\\fresor\\Documents", f"A().a == 'C:{os.sep}Users{os.sep}fresor{os.sep}Documents' -> {A().a=} == 'C:{os.sep}Users{os.sep}fresor{os.sep}Documents'"
# 	assert B().a == A().a, f"B().a == A().a -> {B().a=} == {A().a=}"
# 	assert B().b == A().a, f"B().b == A().a -> {B().b=} == {A().a=}"

# 	class C(B):
# 		c = PathAlias["b"]
	
# 	assert C().a == A().a, f"C().a == A().a -> {C().a=} == {A().a=}"
# 	assert C().b == A().a, f"C().b == A().a -> {C().b=} == {A().a=}"
# 	assert C().c == A().a, f"C().c == A().a -> {C().c=} == {A().a=}"

# 	class D:
# 		d = str(Path("C:\\", "Users", "fresor", "Documents"))
	
# 	class E(D):
# 		d = PathAlias("d")
	
# 	assert E().d == Path("C:\\", "Users", "fresor", "Documents")#, f'E().d == Path("C:", os.sep, "Users", "fresor", "Documents") -> {E().d=} == {Path("C:", os.sep, "Users", "fresor", "Documents")=}'

def test_appdirs():
	
	lib = SoftwareLibrary()

	for attr in filter(lambda x : not x.startswith("_"), object.__dir__(lib)):
		assert hasattr(lib, attr), f"SoftwareLibrary does not have access to expected attribute {attr!r}"
		if attr in ["AUTHOR_NAME", "VERSION_NAME"]: continue
		assert getattr(lib, attr) is not None, f"SoftwareLibrary attribute {attr!r} is None"
	
def test_library():
	import os

	class MyLibrary(SoftwareLibrary):
		SOFTWARE_NAME = "MyApp"
		VERSION_NAME = "ALPHA"

	lib = MyLibrary()
	
	for attr in lib.baseDirs:
		assert hasattr(lib, attr), f"SoftwareLibrary does not have access to expected attribute {attr!r}"
		assert getattr(lib, attr) is not None, f"SoftwareLibrary attribute {attr!r} is None"
		assert getattr(lib, attr).endswith(os.path.join("MyApp", "ALPHA")), f'SoftwareLibrary attribute incorrectly named. Should end in {os.path.join("Fredrik Sörensen", "MyApp", "ALPHA")!r} but full path was {getattr(lib, attr)!r} is None'

def test_print():

	class MyLibrary(SoftwareLibrary):
		SOFTWARE_NAME = "MyApp"
		VERSION_NAME = "ALPHA"

	lib = MyLibrary()
	print(lib)
	assert True
