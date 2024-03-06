from setuptools import setup, find_packages
import os
from PseudoPathy.__init__ import __version__

setup(
    name="PseudoPathy",
    version=__version__,
    url=None,
    description="\"Smart\" file- and directory path managing package.",

    # Author details
    author="Fredrik Sörensen",
    author_email="fredrik.sorensen@foi.se",

    license='GNU GENERAL PUBLIC LICENSE version 3',

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent"
    ],
    python_requires=">=3.8",

    keywords="Paths Path Filemanagement Directories Directorymanagement",

    install_requires=[""],
    packages=find_packages(exclude=[os.path.join('PseudoPathy', 'test.py')])
)