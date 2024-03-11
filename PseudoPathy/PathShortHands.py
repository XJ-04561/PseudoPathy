"""
# OS Alibis
```python
pSep = os.path.sep
pJoin = os.path.join
pExists = os.path.exists
pIsAbs = lambda path: os.path.isabs(os.path.normpath(os.path.expanduser(path)))
pIsFile = os.path.isfile
pExpUser = os.path.expanduser
pAbs = lambda path: os.path.abspath(os.path.expanduser(path))
pNorm = lambda path: os.path.normpath(os.path.expanduser(path))
pDirName = os.path.dirname
pName = lambda path: os.path.basename(os.path.splitext(path)[0])
pExt = lambda path: os.path.splitext(path)[1]
pBackAccess = lambda path, perms : any(all(os.access(path.rsplit(os.path.sep,i+1)[0], perm) for perm in perms) if type(perms) in [list,tuple] else os.access(path.rsplit(os.path.sep,i+1)[0], perms) for i in range(len(path.split(os.path.sep))))
pMakeDirs = lambda path: os.makedirs(path, mode=711, exist_ok=True)
```
"""

import os

## Make these methods of Path and PathGroup instead?

# OS Alibis
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

pExpUser = os.path.expanduser
"""`os.path.expanduser`"""

pAbs = lambda path: os.path.abspath(os.path.expanduser(path))
"""`lambda path: os.path.abspath(os.path.expanduser(path))`"""

pNorm = lambda path: os.path.normpath(os.path.expanduser(path))
"""`lambda path: os.path.normpath(os.path.expanduser(path))`"""

pDirName = os.path.dirname
"""`os.path.dirname`"""

pName = lambda path: os.path.basename(os.path.splitext(path)[0])
"""`lambda path: os.path.basename(os.path.splitext(path)[0])`"""

pExt = lambda path: os.path.splitext(path)[1]
"""`lambda path: os.path.splitext(path)[1]`"""

pBackAccess = lambda path, perms : any(all(os.access(path.rsplit(os.path.sep,i+1)[0], perm) for perm in perms) if type(perms) in [list,tuple] else os.access(path.rsplit(os.path.sep,i+1)[0], perms) for i in range(len(path.split(os.path.sep))))
"""`lambda path, perms : any(all(os.access(path.rsplit(os.path.sep,i+1)[0], perm) for perm in perms) for i in range(len(path)))`
Checks if os.access is true for all perms, but if it isn't, then it checks the parent directory, this repeats until a parent directory passes."""

pMakeDirs = lambda path: os.makedirs(path, mode=711, exist_ok=True)
"""`lambda path: os.makedirs(path, mode=711, exist_ok=True)`"""