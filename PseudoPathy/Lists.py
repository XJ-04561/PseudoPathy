
from PseudoPathy.Globals import *
from PseudoPathy.Paths import Path, FilePath, DirectoryPath

class PathList(Pathy, tuple):
	"""A list of paths used when a collection of paths are coupled in their use. That is to say, they are not a group 
	from which to choose one, but paths which are meant to be used together. An example would be a video-only file and 
	an audio-only file that are to be merged into an `.mp4`. Their `Path` objects can be stored in a `FileList` object 
	so they can be more easily passed around without accidentally separating, along with some other features like 
	getting the common parts of their respective file names, or their paths' common directories.
	
	An example when more than two files are involved could be when a software needs many accompanying files with the 
	query file, or when a large file needs to be split into several smaller part files (Relevant for FAT32 systems or 
	very large data files.)
	
	*Is not based on the `list` type, as mutability is not desired, but the name is used for ease of learning for
	lesser experienced maintainers.*"""

	@overload
	def __new__(cls, iterable): ...
	@overload
	def __new__(cls, *paths): ...
	def __new__(cls, first, *rest):
		if cls is FileList:
			pathCls = FilePath
		elif cls is DirectoryList:
			pathCls = DirectoryPath
		else:
			pathCls = Path
		
		if not rest and not isinstance(first, str):
			paths = tuple(map(pathCls, first))
		else:
			paths = tuple(map(pathCls, (first,) + rest))

		if cls is PathList:
			if all(isinstance(p, FilePath) for p in paths):
				return super().__new__(FileList, paths)
			elif all(isinstance(p, DirectoryPath) for p in paths):
				return super().__new__(DirectoryList, paths)
		
		return super().__new__(cls, paths)
	
	def __str__(self):
		return " ".join(self)
	
	def __format__(self, format_spec : str):
		if format_spec.endswith("n"):
			return format(self.name, format_spec.rstrip("n"))
		else:
			return format(" ".join(map(lambda p:"'"+p.strip("'")+"'", self)), format_spec)
	
	def __iter__(self) -> Generator["PathList",None,None]:
		return super().__iter__()
	
	@cached_property
	def name(self) -> str:
		from PseudoPathy.Alignments import alignName
		return alignName(tuple(pName(p) for p in self))
	
	@cached_property
	def signature(self) -> str:
		from PseudoPathy.Alignments import alignSignature
		return alignSignature(self)

class DirectoryList(PathList): pass

class FileList(PathList):
	
	
	@cached_property
	def name(self) -> str:
		from PseudoPathy.Alignments import alignName
		return alignName(tuple(p.name for p in self))
	
	@cached_property
	def ext(self) -> str|tuple[str]:
		if len(set(map(*this.ext, self))) == 1:
			self[0].ext
		else:
			return tuple(fp.ext for fp in self)

	@cached_property
	def signature(self) -> str:
		from PseudoPathy.Alignments import alignSignature
		return alignSignature(tuple(p.directory / p.name for p in self))