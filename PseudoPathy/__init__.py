
try:
    from PseudoPathy.Paths import Path, FilePath, DirectoryPath, DisposablePath
    from PseudoPathy.Group import PathGroup
    from PseudoPathy.Library import PathLibrary
    import PseudoPathy.Functions as Functions
    import PseudoPathy._globals as Globals
except:
    from Paths import Path, FilePath, DirectoryPath, DisposablePath
    from Group import PathGroup
    from Library import PathLibrary
    import Functions as Functions
    import _globals as Globals