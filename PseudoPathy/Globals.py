

import os, shutil, random, sys, logging, re, copy
from functools import cached_property
from typing import overload, Literal, Container, Any
from appdirs import AppDirs
random.seed()

class Alias:

	realName : str
	aliasName : str
	def __init__(self, realName):
		self.realName = realName
	
	def __set_name__(self, owner, name):
		self.aliasName = name
	
	def __get__(self, instance, owner=None):
		return getattr(instance, self.realName)

	def __set__(self, instance, value):
		setattr(instance, self.realName, value)
	
	def __delete__(self, instance, owner=None):
		delattr(instance, self.realName)

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

class SoftwareDirs(AppDirs, metaclass=Rename):

	appname : str = Alias("SOFTWARE_NAME")
	appauthor : str = Alias("AUTHOR_NAME")
	version : str = Alias("VERSION_NUMBER")
	multipath : bool = True

	userDataDir		= Alias("user_data_dir")
	userConfigDir	= Alias("user_config_dir")
	siteDataDir		= Alias("site_data_dir")
	siteConfigDir	= Alias("site_config_dir")
	userCacheDir	= Alias("user_cache_dir")
	userLogDir		= Alias("user_log_dir")

	@cached_property
	def user_data_dir(self):
		from PseudoPathy.Group import PathGroup
		return PathGroup(AppDirs.user_data_dir.fget(self))

	@cached_property
	def user_config_dir(self):
		from PseudoPathy.Group import PathGroup
		return PathGroup(AppDirs.user_config_dir.fget(self))

	@cached_property
	def site_data_dir(self):
		from PseudoPathy.Group import PathGroup
		return PathGroup(*AppDirs.site_data_dir.fget(self).split(os.pathsep))

	@cached_property
	def site_config_dir(self):
		from PseudoPathy.Group import PathGroup
		return PathGroup(*AppDirs.site_config_dir.fget(self).split(os.pathsep))

	@cached_property
	def user_cache_dir(self):
		from PseudoPathy.Group import PathGroup
		return PathGroup(AppDirs.user_cache_dir.fget(self))

	@cached_property
	def user_log_dir(self):
		from PseudoPathy.Group import PathGroup
		return PathGroup(AppDirs.user_log_dir.fget(self))

	@cached_property
	def site_data_dir(self):
		from PseudoPathy.Group import PathGroup
		return PathGroup(*AppDirs.site_data_dir.fget(self).split(os.pathsep))

	@cached_property
	def dataDir(self):
		from PseudoPathy.Group import PathGroup
		return PathGroup(self.siteDataDir, self.userDataDir)

	@cached_property
	def configDir(self):
		from PseudoPathy.Group import PathGroup
		return PathGroup(self.siteConfigDir, self.userConfigDir)


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
