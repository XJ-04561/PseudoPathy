

import os, shutil, random, sys, logging, re, copy, stat, appdirs
from functools import cached_property
from itertools import chain
from typing import overload, Literal, Container, Any, Callable, Generator, Self, Union, Iterator, Iterable
from This import this
random.seed()


if os.name == "nt": # Is windows-like path separation
	SPLITTER = re.compile(f"[.]|[-]|[_]|[{os.path.sep}{os.path.sep}]")
	ALLOWED = re.compile(r"^[^;:/*?\\]+$")
else:
	SPLITTER = re.compile(f"[.]|[-]|[_]|[{os.path.sep}]")
	ALLOWED = re.compile(r"^[^;:/|<>=,]+$")

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

class Pathy: pass
class Directory: pass
class File: pass
class Unique: pass

OPEN_PATHS = []

LOGGER = logging.Logger("PseudoPathy", level=logging.FATAL)
"""`logging.Logger` object to use."""

DISPOSE : bool = True

# OS Alibis
from PseudoPathy.PathShortHands import pSep, pJoin, pExists, pIsAbs, pIsFile, pIsDir, pExpUser, pAbs, pNorm, pReal, pDirName, pName, pExt, pAccess, pBackAccess, pMakeDirs, PERMS_LOOKUP_OS, PERMS_LOOKUP


