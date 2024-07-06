
from PseudoPathy import PathLibrary, SoftwareLibrary, FilePath, DirectoryPath, Path, PathGroup
from GeekyGadgets.Classy import Default
import time, os

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


def test_software_library():
	
	class MyAppLibrary(SoftwareLibrary):
		SOFTWARE_NAME = "MyTestApp"

		query : tuple[str]

		sessionName = Default["query"](lambda self: f"Session-{time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime())}")

		@Default["workDir", "userDir", "SOFTWARE_NAME"]
		def outDir(self):
			return DirectoryPath(self.workDir, purpose="w") | (self.userDir / self.SOFTWARE_NAME)
		
		@Default["outDir", "sessionName"]
		def resultDir(self):
			return self.outDir.create(self.sessionName)
		
		def __init__(self, query, sessionName=None):
			self.query = query
			if sessionName:
				self.sessionName = sessionName
	
	AL1 = MyAppLibrary(("TestSession_1", "TestSession_2"))
	AL2 = MyAppLibrary(("TestSession_A", "TestSession_B"), sessionName="TestSessionName")

	assert AL1.resultDir is not None
	assert AL2.resultDir is not None

	os.rmdir(AL1.resultDir)
	del AL1.resultDir
	os.rmdir(AL2.resultDir)
	del AL2.resultDir
	
	assert AL1.resultDir is not None
	assert AL2.resultDir is not None
	
	os.rmdir(AL1.resultDir)
	os.rmdir(AL2.resultDir)


	AL3 = MyAppLibrary(("TestSession_1", "TestSession_2"), sessionName="TestSessionName")

	assert AL3.resultDir is not None

	os.rmdir(AL3.resultDir)