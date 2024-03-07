"""
# OS Alibis
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
"""

import os

# OS Alibis
pSep = os.path.sep
"""os.path.sep"""
pJoin = os.path.join
"""os.path.join"""
pExists = os.path.exists
"""os.path.exists"""
pIsAbs = lambda path: os.path.isabs(os.path.normpath(os.path.expanduser(path)))
"""lambda path: os.path.isabs(os.path.normpath(os.path.expanduser(path)))"""
pIsFile = os.path.isfile
"""os.path.isfile"""
pExpUser = os.path.expanduser
"""os.path.expanduser"""
pAbs = lambda path: os.path.abspath(os.path.expanduser(path))
"""lambda path: os.path.abspath(os.path.expanduser(path))"""
pNorm = lambda path: os.path.normpath(os.path.expanduser(path))
"""lambda path: os.path.normpath(os.path.expanduser(path))"""
pDirName = os.path.dirname
"""os.path.dirname"""
pName = lambda path: os.path.basename(os.path.splitext(path)[0])
"""lambda path: os.path.basename(os.path.splitext(path)[0])"""
pExt = lambda path: os.path.splitext(path)[1]
"""lambda path: os.path.splitext(path)[1]"""