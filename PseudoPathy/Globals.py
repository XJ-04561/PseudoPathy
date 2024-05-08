

import os, shutil, random, sys, logging, re, copy, stat
from functools import cached_property
from typing import overload, Literal, Container, Any, Callable
from appdirs import AppDirs
from itertools import chain
random.seed()

class Alias:

	realName : str
	aliasName : str

	fget : Callable
	fset : Callable
	fdel : Callable

	def fget(self, instance):
		print(repr(self), repr(instance))
		if self.realName != self.aliasName:
			return getattr(instance, self.realName)
		else:
			for cls in type(instance).mro()[1:]:
				if self.realName in dir(cls):
					attr = getattr(cls, self.realName)
					if hasattr(attr, "__get__"):
						return attr.__get__(instance, cls)
					else:
						return attr
			return getattr(instance, self.realName) # Throws appropriate exception
	def fset(self, instance, value):
		instance.__dict__[self.realName] = value
	def fdel(self, instance):
		del instance.__dict__[self.realName]
	
	def __init__(self, realName):
		self.realName = realName
	
	def __set_name__(self, owner, name):
		self.aliasName = name
	
	def __get__(self, instance, owner=None):
		return self.fget(instance)

	def __set__(self, instance, value):
		self.fset(instance, value)
	
	def __delete__(self, instance, owner=None):
		self.fdel(instance)

class LinkNames(type):
	def __new__(cls, name, bases, namespace):
		for name, oldName in namespace["__annotations__"].items():
			if type(oldName) is str:
				for base in reversed(bases):
					if hasattr(base, oldName):
						namespace[name] = property(lambda self: getattr(self, oldName), lambda self, value: setattr(self, oldName, value), lambda self: delattr(self, oldName), getattr(getattr(base, oldName), "__doc__", None))
						break
		return type.__new__(type, name, bases, namespace)

def unCapitalize(string):
	return f"{string[0].lower()}{string[1:]}"

class PathPermsMeta(type):
	def __instancecheck__(self, instance: Any) -> bool:
		return getattr(instance, unCapitalize(self.__name__), None) is not None or os.access(str(instance), mode=self.code)

class Readable(metaclass=PathPermsMeta):
	code : int = 4
class Writable(metaclass=PathPermsMeta):
	code : int = 2
class Executable(metaclass=PathPermsMeta):
	code : int = 1
class FullPerms(metaclass=PathPermsMeta):
	code : int = 7

LOGGER = logging.Logger("PseudoPathy")
"""`logging.Logger` object to use."""

DISPOSE : bool = True

USER_DIRECTORY = os.path.expanduser("~")

# OS Alibis
from PseudoPathy.PathShortHands import pSep, pJoin, pExists, pIsAbs, pIsFile, pIsDir, pExpUser, pAbs, pNorm, pReal, pDirName, pName, pExt, pAccess, pBackAccess, pMakeDirs, PERMS_LOOKUP_OS, PERMS_LOOKUP
