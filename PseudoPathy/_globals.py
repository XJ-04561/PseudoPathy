

import os, shutil, random
from functools import cached_property, cache
random.seed()

class DummyLogger:
    """A dummy logger for all Path derived objects to log to, except it does not
    perform logging. To enable logging you simply assign a working logger to the
    'logger' attribute of the Path class."""
    def debug(self, *args, **kwargs): pass
    def info(self, *args, **kwargs): pass
    def warning(self, *args, **kwargs): pass
    def error(self, *args, **kwargs): pass
    def critical(self, *args, **kwargs): pass

PERMS_LOOKUP = {"r":"read", "w":"write", "x":"execute"}
PERMS_LOOKUP_OS = {"r":os.R_OK, "w":os.W_OK, "x":os.X_OK}
MAX_RESULTS = 10**9
LOGGER = DummyLogger()
DISPOSE = True

# OS alibis
pSep = os.path.sep
pJoin = os.path.join
pIsAbs = lambda path: os.path.isabs(os.path.expanduser(path))
pExpUser = os.path.expanduser
pAbs = os.path.abspath
pNorm = os.path.normpath
pDirName = os.path.dirname
pMakeDirs = os.makedirs
pIsFile = os.path.isfile