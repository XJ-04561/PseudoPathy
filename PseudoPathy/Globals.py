

import os, shutil, random, sys, logging, re
from functools import cached_property
from typing import overload, Literal, Container, Any
from platformdirs import AppDirs

pat = re.compile(r"[_](\w)")

def camelize(string : str):
	pat.sub(string, lambda m : m.group(0).upper())

class Pathize:
	prop : property
	def __init__(self, prop):
		self.prop = prop
	
	def __get__(self, instance, owner=None):
		from Paths import DirectoryPath
		return DirectoryPath(self.prop.__get__(instance, owner))

class Camelized(type):
	def __new__(cls, className, bases, namespace):
		namespace = {camelize(name):Pathize(value) for name, value in filter(lambda x : not x[0].startswith("_"), namespace.items())}
		for base in bases:
			namespace = namespace | {camelize(name):Pathize(value) for name, value in filter(lambda x : not x[0].startswith("_"), vars(base).items())}
		return super().__new__(cls, className, (), namespace)

class SoftwareDirs(AppDirs, metaclass=Camelized):
	@property
	def SOFTWARE_NAME(self):
		return self.appname
	
	@SOFTWARE_NAME.setter
	def SOFTWARE_NAME(self, value):
		self.appname = value
	
	@SOFTWARE_NAME.deleter
	def SOFTWARE_NAME(self):
		self.appname = ""
	
	siteCacheDir : str
	userCacheDir : str

	siteConfigDir : str
	userConfigDir : str
	iterConfigDir : str
	siteDataDir : str
	userDataDir : str
	iterDataDir : str
	siteRuntimeDir : str
	userRuntimeDir : str
	userDocumentsDir : str
	userLogDir : str
	userStateDir : str


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
