
from PseudoPathy.Globals import *
import PseudoPathy.Globals as Globals
from PseudoPathy.Paths import DirectoryPath, PathGroup
from PseudoPathy.Group import PathGroup

class SoftwareDirs:
	"""This is what you want to override for installation/software-related files to go into a folder named after your Software"""

	SOFTWARE_NAME : str = "PseudoPathy"
	AUTHOR_NAME : str = None
	VERSION_NAME : str = None
	ROAMING : bool = False

	workDir : str	= DirectoryPath(os.curdir)
	userDir			= DirectoryPath(os.path.expanduser("~"))

	baseDirs = ("userDataDir", "siteDataDir", "dataDir",
			 	"userConfigDir", "siteConfigDir", "configDir",
				"userCacheDir", "userLogDir")

	@cached_property
	def userDataDir(self):
		return DirectoryPath(appdirs.user_data_dir(self.SOFTWARE_NAME, self.AUTHOR_NAME, self.VERSION_NAME, self.ROAMING))
	@cached_property
	def siteDataDir(self):
		return PathGroup(*appdirs.site_data_dir(self.SOFTWARE_NAME, self.AUTHOR_NAME, self.VERSION_NAME, multipath=True).split(os.pathsep))
	@cached_property
	def dataDir(self):
		return self.siteDataDir | self.userDataDir

	@cached_property
	def userConfigDir(self):
		return DirectoryPath(appdirs.user_config_dir(self.SOFTWARE_NAME, self.AUTHOR_NAME, self.VERSION_NAME, self.ROAMING))
	@cached_property
	def siteConfigDir(self):
		return PathGroup(*appdirs.site_config_dir(self.SOFTWARE_NAME, self.AUTHOR_NAME, self.VERSION_NAME, multipath=True).split(os.pathsep))
	@cached_property
	def configDir(self):
		return self.siteConfigDir | self.userConfigDir

	@cached_property
	def userCacheDir(self):
		return DirectoryPath(appdirs.user_cache_dir(self.SOFTWARE_NAME, self.AUTHOR_NAME, self.VERSION_NAME))
	@cached_property
	def userLogDir(self):
		return DirectoryPath(appdirs.user_log_dir(self.SOFTWARE_NAME, self.AUTHOR_NAME, self.VERSION_NAME))


# class Alias:

# 	realName : str
# 	aliasName : str

# 	def __class_getitem__(cls, attrName : str):
# 		return cls(attrName)
	
# 	def fget(self, instance):
# 		if self.aliasName != self.realName:
# 			return getattr(instance, self.realName)
# 		elif (attr := type(instance).__getattribute__(type(instance), self.realName)) is not self:
# 			return attr.__get__(instance) if hasattr(attr, "__get__") else attr
# 		else:
# 			_iter = iter(type(instance).__mro__)
# 			next(_iter)
# 			for cls in _iter:
# 				if (attr := cls.__dict__.get(self.realName, _NOT_SET)) is not _NOT_SET:
# 					return attr.__get__(instance) if hasattr(attr, "__get__") else attr
# 		print(f"Nothing found for {self=}, {instance=}, {type(instance).__mro__=}")
# 	def fset(self, instance, value):
# 		instance.__dict__[self.realName] = value
# 	def fdel(self, instance):
# 		del instance.__dict__[self.realName]
	
# 	def __init__(self, realName):
# 		self.realName = realName
	
# 	def __set_name__(self, owner, name):
# 		self.aliasName = name
	
# 	def __get__(self, instance, owner=None):
# 		return self.fget(instance)

# 	def __set__(self, instance, value):
# 		self.fset(instance, value)
	
# 	def __delete__(self, instance, owner=None):
# 		self.fdel(instance)

# class LinkNames(type):
# 	def __new__(cls, name, bases, namespace):
# 		for name, oldName in namespace["__annotations__"].items():
# 			if type(oldName) is str:
# 				for base in reversed(bases):
# 					if hasattr(base, oldName):
# 						namespace[name] = property(lambda self: getattr(self, oldName), lambda self, value: setattr(self, oldName, value), lambda self: delattr(self, oldName), getattr(getattr(base, oldName), "__doc__", None))
# 						break
# 		return type.__new__(type, name, bases, namespace)


# class PathProperty(property):

# 	def __call__(self, instance, owner=None):
# 		raise AttributeError(f"{type(instance).__name__ or owner.__qualname__!r} {'object' if instance is not None else 'type'} has no attribute {self.__qualname__.split('.')[-1]!r}")
	
# 	def fget(_fget, instance):
# 		print(f"{_fget=}", f"{instance=}")
# 		from PseudoPathy import Path, PathGroup
# 		if os.pathsep not in (path := _fget(instance)):
# 			return Path(path)
# 		else:
# 			return PathGroup(*path.split(os.pathsep))
	
# 	def __new__(cls, fget, fset=None, fdel=None, doc=None):
# 		return super().__new__(cls, cls.fget.__get__(fget,type(fget)), fset, fdel, doc)


# 	def __add__(self, right):
# 		if isinstance(right, property):
# 			def add(instance):
# 				return self.fget(instance) + right.__get__(instance)
# 		else:
# 			def add(instance):
# 				return self.fget(instance) + right
# 		return PathProperty(add)
# 	def __truediv__(self, right):
# 		if isinstance(right, property):
# 			def truediv(instance):
# 				return self.fget(instance) / right.__get__(instance)
# 		else:
# 			def truediv(instance):
# 				return self.fget(instance) / right
# 		return PathProperty(truediv)
# 	def __rtruediv__(self, left):
# 		if isinstance(left, property):
# 			def rtruediv(instance):
# 				return left.__get__(instance) / self.fget(instance)
# 		else:
# 			def rtruediv(instance):
# 				return left / self.fget(instance)
# 		return PathProperty(rtruediv)
# 	def __or__(self, right):
# 		if isinstance(right, property):
# 			def _or(instance):
# 				return self.fget(instance) | right.__get__(instance)
# 		else:
# 			def _or(instance):
# 				return self.fget(instance) | right
# 		return PathProperty(_or)
# 	def __ror__(self, left):
# 		if isinstance(left, property):
# 			def ror(instance):
# 				return left.__get__(instance) | self.fget(instance)
# 		else:
# 			def ror(instance):
# 				return left | self.fget(instance)
# 		return PathProperty(ror)

# class PathAlias(Alias, PathProperty):

# 	def __get__(self, instance, owner=None):
# 		from PseudoPathy import Path, PathGroup
# 		if os.pathsep not in (path := Alias.__get__(self, instance)):
# 			return Path(path)
# 		else:
# 			return PathGroup(*path.split(os.pathsep))
