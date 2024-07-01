

import os, shutil, sys, logging, re, stat, appdirs, itertools, glob
from functools import cached_property
from itertools import chain
from typing import overload, Literal, Container, Any, Callable, Generator, Union, Iterator, Iterable, final, TypeVar
from This import this
from abc import ABC, abstractmethod

if os.name == "nt": # Is windows-like path separation
	SPLITTER = re.compile(f"[.]|[-]|[_]|[{os.path.sep}{os.path.sep}]")
	ALLOWED = re.compile(r"^[^;:/*?\\]+$")
else:
	SPLITTER = re.compile(f"[.]|[-]|[_]|[{os.path.sep}]")
	ALLOWED = re.compile(r"^[^;:/|<>=,]+$")

def unCapitalize(string):
	return f"{string[0].lower()}{string[1:]}"

# _P = TypeVar("_P")
# _PI = TypeVar("_PI")
class Pathy(ABC): ...
	
	# readable : "Pathy"
	# writable : "Pathy"
	# executable : "Pathy"
	# fullperms : "Pathy"

	# @abstractmethod
	# @property
	# def readable(self : _P) -> _P: ...
	
	# @abstractmethod
	# @property
	# def writable(self : _P) -> _P: ...
	
	# @abstractmethod
	# @property
	# def executable(self : _P) -> _P: ...
	
	# @abstractmethod
	# @property
	# def fullperms(self : _P) -> _P: ...

	# @overload
	# def find(self : _P, /) -> _P: ...
	# @overload
	# def find(self : _P, /, path : str) -> _P: ...
	# @overload
	# def find(self : _P, /, path : str, *, perm : str="r") -> _P: ...
	# @abstractmethod
	# def find(self : _P, /, path : str=None, *, perm : str="r") -> _P: ...
	
	# @overload
	# def create(self : _P|_PI[_P], /) -> _P: ...
	# @overload
	# def create(self : _P|_PI[_P], /, path : str) -> _P: ...
	# @overload
	# def create(self : _P|_PI[_P], /, path : str, *, perm : str="r") -> _P: ...
	# @abstractmethod
	# def create(self, /, path : str=None, *, perm : str="r"): ...

class Directory: ...
class File: ...
class Unique: ...

class Stat:
	
	mode : int = 0
	ino : int = 0
	dev : int = 0
	nlink : int = 0
	uid : int = 0
	gid : int = 0
	size : int = 0
	atime : int = 0
	mtime : int = 0
	ctime : int = 0
	atime_ns : int = 0
	mtime_ns : int = 0
	ctime_ns : int = 0
	blksize : int = 0
	blocks : int = 0
	rdev : int = 0

	def __init__(self, path):
		try:
			stat = os.stat(path)
			for name in ["st_mode", "st_ino", "st_dev", "st_nlink", "st_uid", "st_gid", "st_size", "st_atime", "st_mtime", "st_ctime", "st_atime_ns", "st_mtime_ns", "st_ctime_ns", "st_blksize", "st_blocks", "st_rdev"]:
				setattr(self, name[3:], getattr(stat, name))
		except:
			pass

class LStat(Stat):
	def __init__(self, path):
		try:
			stat = os.lstat(path)
			for name in ["st_mode", "st_ino", "st_dev", "st_nlink", "st_uid", "st_gid", "st_size", "st_atime", "st_mtime", "st_ctime", "st_atime_ns", "st_mtime_ns", "st_ctime_ns", "st_blksize", "st_blocks", "st_rdev"]:
				setattr(self, name[3:], getattr(stat, name))
		except:
			pass

		

OPEN_PATHS = []

LOGGER = logging.Logger("PseudoPathy", level=logging.FATAL)
"""`logging.Logger` object to use."""

DISPOSE : bool = True

# OS Alibis
from PseudoPathy.ShortHands import pSep, pJoin, pExists, pIsAbs, pIsFile, pIsDir, pExpUser, pAbs, pNorm, pReal, pDirName, pName, pExt, pAccess, pBackAccess, pMakeDirs, PERMS_LOOKUP_OS, PERMS_LOOKUP


