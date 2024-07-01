
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

def test_filenameAlignment():
	from PseudoPathy.Paths import Path, DirectoryPath, FilePath, PathList, DirectoryList, FileList
	from PseudoPathy.Alignments import align, align2, alignName
	import os
	curDir, userDir = Path(os.path.realpath(".")), Path(os.path.expanduser("~"))
	file1 = curDir / "myfile_[1].zip"
	file2 = curDir / "myfile_[2].zip"
	fileList = FileList(file1, file2)

	assert align2(file1, file2) == file1[:-7] + "[X].zip", f"{align2(file1, file2)=} == {file1[:-7] + '[X].zip'}"

	assert fileList.name == "myfile", f'{fileList.name} == {"myfile"}'

	expected = (curDir / "myfile").split(":\\")[-1] if os.name == "nt" else (curDir / "myfile")
	expected = "_".join(filter(len, expected.replace("-", "_").replace(".", "_").split(os.path.sep)))
	assert fileList.signature == expected, f"{fileList.signature} == {expected}"

	dir1 = userDir / "Documents" 
	dir2 = userDir / "Documents" 
	dirList = DirectoryList(dir1, dir2)

	assert dirList.name == "Documents", f'{dirList.name} == {"Documents"}'
	
	expected = dir1.split(":\\")[-1] if os.name == "nt" else dir1
	expected = "_".join(filter(len, expected.split(os.path.sep)))
	
	assert dirList.signature == expected, f"{dirList.signature} == {expected}"

	aligned1 = PathList("FSC458_R1.fq", "FSC458_R2.fq")

	assert "FSC458" == aligned1.name, '"FSC458" == PathList("FSC458_R1.fq", "FSC458_R2.fq").name'

	aligned2 = PathList("FSC458.fq", "FSC458(1).fq")

	assert "FSC458" == aligned2.name, '"FSC458" == PathList("FSC458.fq", "FSC458(1).fq").name'
	
	aligned3 = PathList("FSC458.fna", "FSC658-[FSC458_R1].fq", "FSC567-[FSC458_R2].fq")

	assert "FSC458" == aligned3.name, 'PathList("FSC458.fna", "FSC658-[FSC458_R1].fq", "FSC567-[FSC458_R2].fq")'

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
		path = getattr(lib, attr)
		assert path is not None, f"SoftwareLibrary attribute {attr!r} is None"
		if isinstance(path, PathGroup):
			if path._roots:
				path = path._roots[0]
				assert path.endswith(os.path.join("MyApp", "ALPHA")) or \
					(path.strip(os.path.sep).split(os.path.sep)[-3] == "MyApp" and \
					path.strip(os.path.sep).split(os.path.sep)[-1] == "ALPHA" ) or \
						os.path.join(*path.strip(os.path.sep).split(os.path.sep)[:-1]).endswith(os.path.join("MyApp", "ALPHA")), f'SoftwareLibrary attribute incorrectly named. Should end in {os.path.join("MyApp", "ALPHA")!r} but full path was {path!r}'
		elif isinstance(path, str):
			assert path.endswith(os.path.join("MyApp", "ALPHA")) or \
				(path.strip(os.path.sep).split(os.path.sep)[-3] == "MyApp" and \
				path.strip(os.path.sep).split(os.path.sep)[-1] == "ALPHA" ) or \
					os.path.join(*path.strip(os.path.sep).split(os.path.sep)[:-1]).endswith(os.path.join("MyApp", "ALPHA")), f'SoftwareLibrary attribute incorrectly named. Should end in {os.path.join("MyApp", "ALPHA")!r} but full path was {path!r}'

def test_print():

	class MyLibrary(SoftwareLibrary):
		SOFTWARE_NAME = "MyApp"
		VERSION_NAME = "ALPHA"

	lib = MyLibrary()
	print(lib)
	assert True
