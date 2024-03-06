
try:
    from PseudoPathy.Paths import Path, FilePath, DirectoryPath, DisposablePath
    from PseudoPathy.Group import PathGroup
    from PseudoPathy.Functions import getUniqueName
    from PseudoPathy.Library import PathLibrary
    import PseudoPathy._globals as PseudoPathyGlobals
except:
    from Paths import Path, FilePath, DirectoryPath, DisposablePath
    from Group import PathGroup
    from Functions import getUniqueName
    from Library import PathLibrary
    import _globals as PseudoPathyGlobals