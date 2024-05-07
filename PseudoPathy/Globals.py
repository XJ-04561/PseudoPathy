

import os, shutil, random, sys, logging, re, copy
from functools import cached_property
from typing import overload, Literal, Container, Any
from appdirs import AppDirs

# pat = re.compile(r"[_](\w)")

# def camelize(string : str):
# 	pat.sub(string, lambda m : m.group(0).upper())

# class Pathize:
# 	prop : property
# 	def __init__(self, prop):
# 		self.prop = prop
	
# 	def __get__(self, instance, owner=None):
# 		from Paths import DirectoryPath
# 		return DirectoryPath(self.prop.__get__(instance, owner))

# class Camelized(type):
# 	def __new__(cls, className, bases, namespace):
# 		namespace = {camelize(name):Pathize(value) for name, value in filter(lambda x : not x[0].startswith("_"), namespace.items())}
# 		for base in bases:
# 			namespace = namespace | {camelize(name):Pathize(value) for name, value in filter(lambda x : not x[0].startswith("_"), vars(base).items())}
# 		return super().__new__(cls, className, (), namespace)

class Rename(type):
	def __new__(cls, name, bases, namespace):
		for name, oldName in namespace["__annotations__"].items():
			if type(oldName) is str:
				for base in reversed(bases):
					if hasattr(base, oldName):
						namespace[name] = getattr(base, oldName)
						break
		return type.__new__(type, name, bases, namespace)
class LinkNames(type):
	def __new__(cls, name, bases, namespace):
		for name, oldName in namespace["__annotations__"].items():
			if type(oldName) is str:
				for base in reversed(bases):
					if hasattr(base, oldName):
						namespace[name] = property(lambda self: getattr(self, oldName), lambda self, value: setattr(self, oldName, value), lambda self: delattr(self, oldName), getattr(getattr(base, oldName), "__doc__", None))
						break
		return type.__new__(type, name, bases, namespace)
AppDirs
class SoftwareDirs(AppDirs, metaclass=Rename):

	SOFTWARE_NAME : str
	AUTHOR_NAME : str
	VERSION_NUMBER : str
	userDataDir		: "user_data_dir"
	userConfigDir	: "user_config_dir"
	userCacheDir	: "user_cache_dir"
	siteDataDir		: "site_data_dir"
	siteConfigDir	: "site_config_dir"
	userLogDir		: "user_log_dir"
	def __init__(self, *args, **kwargs) -> None:
		self.appname
		self.appauthor
		self.appauthor
	def __getattribute__(self, name: str) -> Any:
		if isinstance(getattr(self, name), str):
			from PseudoPathy.Paths import DirectoryPath
			return DirectoryPath(name)
		else:
			return super().__getattribute__(name)


random.seed()

def unCapitalize(string):
	return f"{string[0].lower()}{string[1:]}"

class PathPermMeta(type):
	def __instancecheck__(self, instance: Any) -> bool:
		return getattr(instance, unCapitalize(self.__name__), None) is not None or os.access(str(instance), mode=self.code)

class Readable(metaclass=PathPermMeta):
	code : int = 4
class Writable(metaclass=PathPermMeta):
	code : int = 2
class Executable(metaclass=PathPermMeta):
	code : int = 1
class FullPerms(metaclass=PathPermMeta):
	code : int = 7

LOGGER = logging.Logger("PseudoPathy")
"""`logging.Logger` object to use."""

DISPOSE : bool = True

USER_DIRECTORY = os.path.expanduser("~")

# OS Alibis
from PseudoPathy.PathShortHands import pSep, pJoin, pExists, pIsAbs, pIsFile, pIsDir, pExpUser, pAbs, pNorm, pReal, pDirName, pName, pExt, pAccess, pBackAccess, pMakeDirs, PERMS_LOOKUP_OS, PERMS_LOOKUP
