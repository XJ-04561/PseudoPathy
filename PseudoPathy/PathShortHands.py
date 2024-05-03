"""
# OS Alibis
```python
pSep = os.path.sep

pJoin = os.path.join

pExists = os.path.exists

pIsAbs = lambda path: os.path.isabs(os.path.normpath(os.path.expanduser(path)))

pIsFile = os.path.isfile

pIsDir = os.path.isdir

pExpUser = os.path.expanduser

pAbs = lambda path: os.path.abspath(os.path.expanduser(path))

pNorm = lambda path: os.path.normpath(os.path.expanduser(path))

pReal = lambda path: os.path.realpath(os.path.expanduser(path))

pDirName = os.path.dirname

pName = lambda path: os.path.basename(os.path.splitext(path)[0])

pExt = lambda path: os.path.splitext(path)[1]

def pBackAccess(path : str, perms : str):
    root ,*parts = path.split(os.path.sep)
    return any(pAccess(pJoin(root, os.path.sep, *(parts[:-i])), perms) for i in range(len(parts)+1))

def pMakeDirs(path, mode=7):
    os.makedirs(path, mode=mode<<6, exist_ok=True)
    if os.access(path, mode=mode):
        return True
    os.chmod(path, mode=mode<<6 + mode<<3)
    if os.access(path, mode=mode):
        return True
    os.chmod(path, mode=mode<<6 + mode<<3 + mode)
    if os.access(path, mode=mode):
        return True
    return False
```
"""

import os

PERMS_LOOKUP = {"r":"read", "w":"write", "x":"execute"}
"""Dictionary for lookup of full names for permission type initials using lower case initials as keys. ie. `"r"` -> `"read"`, `"w"` -> `"write"`, or `"x"` -> `"execute"`."""
PERMS_LOOKUP_OS = {"r":os.R_OK, "w":os.W_OK, "x":os.X_OK, "d":8}
PERMS_LOOKUP_OS_INV = {os.R_OK:"r", os.W_OK:"w", os.X_OK:"x", 0:"d"}

##
## HANDLE BITMASK BETTER
##

"""Dictionary for lookup of `os` permission types using lower case initials as keys. ie. `"r"`, `"w"`, or `"x"`."""

## Make these methods of Path and PathGroup instead?

# OS Alibis
pPerms = lambda mode : sum(map(PERMS_LOOKUP_OS.__getitem__, mode))
"""`lambda mode : sum(map(PERMS_LOOKUP_OS.__getitem__, mode))`"""

pCharPerms = lambda chMode : "".join(map(PERMS_LOOKUP_OS_INV.__getitem__, chMode))
"""`lambda mode : sum(map(PERMS_LOOKUP_OS.__getitem__, mode))`"""

pSep = os.path.sep
"""`os.path.sep`"""

pJoin = os.path.join
"""`os.path.join`"""

pExists = os.path.exists
"""`os.path.exists`"""

pIsAbs = lambda path: os.path.isabs(os.path.normpath(os.path.expanduser(path)))
"""`lambda path: os.path.isabs(os.path.normpath(os.path.expanduser(path)))`"""

pIsFile = os.path.isfile
"""`os.path.isfile`"""

pIsDir = os.path.isdir
"""`os.path.isdir`"""

pExpUser = os.path.expanduser
"""`os.path.expanduser`"""

pAbs = lambda path: os.path.abspath(os.path.expanduser(path))
"""`lambda path: os.path.abspath(os.path.expanduser(path))`"""

pNorm = lambda path: os.path.normpath(os.path.expanduser(path))
"""`lambda path: os.path.normpath(os.path.expanduser(path))`"""

pReal = lambda path: os.path.realpath(os.path.expanduser(path))
"""`lambda path: os.path.realpath(os.path.expanduser(path))`"""

pDirName = os.path.dirname
"""`os.path.dirname`"""

pName = lambda path: os.path.basename(os.path.splitext(path)[0])
"""`lambda path: os.path.basename(os.path.splitext(path)[0])`"""

pExt = lambda path: os.path.splitext(path)[1]
"""`lambda path: os.path.splitext(path)[1]`"""

pAccess = lambda path, mode : os.access(path, mode=pPerms(mode))
"""`lambda path, mode : os.access(path, mode=sum(PERMS_LOOKUP_OS[c] for c in mode))`"""

def pBackAccess(path : str, perms : str):
    """```python
    def pBackAccess(path : str, perms : str):
        root ,*parts = path.split(os.path.sep)
        return any(pAccess(pJoin(root, *(parts[:i])), perms) for i in range(len(parts), 0, -1))
    ```
    Checks if os.access is true for all perms, but if it isn't, then it checks the parent directory, this repeats until a parent directory passes."""
    root ,*parts = path.split(os.path.sep)
    # separator required between root and the rest. Otherwise you get: os.path.join("C:", "Users") -> 'C:Users' or os.path.join("", "srv") -> "srv"
    return any(pAccess(pJoin(root, os.path.sep, *(parts[:-i])), perms) for i in range(len(parts)+1))

def pMakeDirs(path, mode : int=7, others : int=4):
    """```python
    os.makedirs(path, mode=mode<<6, exist_ok=True)
    if os.access(path, mode=mode):
        return True
    os.chmod(path, mode=mode<<6 + mode<<3)
    if os.access(path, mode=mode):
        return True
    os.chmod(path, mode=mode<<6 + mode<<3 + mode)
    if os.access(path, mode=mode):
        return True
    return False
    ```
    """

    os.makedirs(path, mode=mode<<6 + others<<3 + others, exist_ok=True)
    if os.access(path, mode=mode):
        return True
    os.chmod(path, mode=mode<<6 + mode<<3 + others)
    if os.access(path, mode=mode):
        return True
    os.chmod(path, mode=mode<<6 + mode<<3 + mode)
    if os.access(path, mode=mode):
        return True
    return False