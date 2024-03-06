
try:
    from PseudoPathy.Paths import Path, FilePath, DirectoryPath, DisposablePath
    from PseudoPathy.Group import PathGroup
    from PseudoPathy.Library import MinimalPathLibrary, PathLibrary
    import PseudoPathy.Functions as Functions
    import PseudoPathy.Globals as Globals
except:
    from Paths import Path, FilePath, DirectoryPath, DisposablePath
    from Group import PathGroup
    from Library import MinimalPathLibrary, PathLibrary
    import Functions as Functions
    import Globals