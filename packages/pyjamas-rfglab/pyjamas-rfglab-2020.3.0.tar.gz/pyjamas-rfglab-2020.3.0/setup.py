"""
    PyJAMAS is Just A More Awesome Siesta
    Copyright (C) 2018  Rodrigo Fernandez-Gonzalez (rodrigo.fernandez.gonzalez@utoronto.ca)

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

""" See this to build an executable:
https://setuptools.readthedocs.io/en/latest/setuptools.html#eggsecutable-scripts"""

"""Building the package:
pythonw setup.py sdist bdist_wheel build_sphinx
#tar tzf dist/*.gz
pythonw -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
pip install -i https://test.pypi.org/simple/ pyjamas

or

pythonw -m twine upload dist/*

# To install, open a new terminal (not within pycharm) and do:
pip3.6 uninstall pyjamas-rfglab
pip3.6 install pyjamas-rfglab

To fill in the install_requires field below, try pipreqs pyjamas from the src/pyjamas folder.
NOTE: When installing a package from testPyPI, the dependencies are also installed from there.
So you will get package not found errors.

NOTE 2: Windows installation should be after installing CONDA, and "conda install shapely=1.6.4". This also installs
geos (C library used by shapely) 3.7.1. Unfortunately geos is only available up to version 0.2.1 in pypi.
Alternatively, there are shapely wheels at http://www.lfd.uci.edu/~gohlke/pythonlibs/#shapely. 
"""

import os
import setuptools
import sys

from sphinx.setup_command import BuildDoc

from pyjamas.pjscore import PyJAMAS


with open("README.md", "r") as fh:
    long_description: str = fh.read()

bin_path: str = os.path.dirname(sys.executable)
# The interpreter needs to be modified to use pythonw, not python (this is a windowed app!!!).
interpreter_name: str = 'pythonw'
shebang: str = '#!/usr/bin/env '
sys.executable = os.path.join(bin_path, interpreter_name)
name = "pyjamas-rfglab"
description = "PyJAMAS is Just A More Awesome SIESTA"

version = PyJAMAS.__version__

# Build pyjamas.
setuptools.setup(
    name=name,
    version=version,
    author="Rodrigo Fernandez-Gonzalez",
    author_email="rodrigo.fernandez.gonzalez@utoronto.ca",
    description=description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://bitbucket.org/rfg_lab/pyjamas",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    install_requires=["joblib==0.11", "lxml>=4.2.5", "matplotlib==3.1.1", "networkx==2.1", "numpy==1.16.1",
                      "opencv-python-headless>=3.4.5.20",
                      "pandas==0.25.1", "PyQt5==5.13.1", "scikit-image==0.15.0", "scikit-learn>=0.21.3",
                      "scipy==1.4.1", "seaborn==0.9.0", "setuptools==41.4.0", "shapely>=1.6.0"],
    python_requires='>=3.6,<3.8',
    entry_points={
        'console_scripts': [
            'pyjamas=pyjamas.pjscore:main'
        ]
    }
)

# Build sphinx docs.
setuptools.setup(
    name=name,
    version=version,
    author="Negar Balaghi and Rodrigo Fernandez-Gonzalez",
    author_email="rodrigo.fernandez.gonzalez@utoronto.ca",
    description=description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://bitbucket.org/rfg_lab/pyjamas",
    cmdclass={'build_sphinx': BuildDoc},
    command_options={
        'build_sphinx': {
            'project': ('setup.py', 'PyJAMAS'),
            'version': ('setup.py', version),
            'build_dir': ('setup.py', './build/docs'),
        }
    },
)