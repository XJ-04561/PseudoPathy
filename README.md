# PseudoPathy
 "Smart" file- and directory path managing package.

```python
p1 = Path(os.path.expanduser("~"))
p2 = Path("Documents", "GitHub", "PseudoPathy")

# Performs os.path.join
p3 = p2 > "README.md"

# Creates a PathGroup with these two paths
pg = p1 | p2

# Performs os.path.join on each path in the PathGroup
pg > "setup.py"

# Creates a library which contains 3 properties: workDir, userDir, and installDir
lib = PathLibrary()

# The library can be used like a dictionary, but values can be accessed by using keys as attributes as well
lib.pathToREADME = p3

```
