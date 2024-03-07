
def runTest():
	import os

	try:
		from PseudoPathy.__init__ import Path, PathLibrary
	except:
		from __init__ import Path, PathLibrary

	p1 = Path(os.path.abspath("/"))
	p2 = Path(os.path.expanduser("~"))
	print("p1 = ", p1)
	print("p2 = ", p2)

	dg1 = p1 | p2
	print("p1 | p2 = ", dg1)

	p3 = p2 > "Documents"
	print("p2 > \"Documents\" = ", p3)

	p4 = p1 + "-Data"
	print("p1 + \"-Data\" = ", p4)

	dg2 = p1 | p2 | p3 | p4
	print("p1 | p2 | p3 | p4 = ", dg2)

	print("dg1 | dg2 = ", dg1 | dg2)

	ex1 = p2 > "myReads.fq"+".log"
	print(ex1)

	lib = PathLibrary()
	print(lib)

if __name__ == "__main__":
	runTest()