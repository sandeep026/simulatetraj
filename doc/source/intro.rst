Dependencies
============

+-----------------+------------------+
|Dependency       |Version           |
+=================+==================+
|python           | 3.11             |
+-----------------+------------------+
|casadi           | 3.6.4            |
+-----------------+------------------+
|matplotlib       | 3.8.2            |
+-----------------+------------------+
|numpy            | 1.26.4           |
+-----------------+------------------+


Installation
============

At the moment, the package is tested and run on Windows 10. Although not tested, the following dependencies
are readily available in linux/macos and the package must be runnable.

-  Clone the repository or download zip
-  Open the folder with VScode

venv
----

-  Create virtual environment using venv
-  All dependencies and package will be installed automatically

conda
-----

-  create conda environment with python >=3.1
-  type ``pip install poetry``
-  from the directory containing the toml file, type ``poetry install``
-  all dependencies and package will be installed

Run the python notebooks from examples folder to verify the
installation.

Limitations
===========

-  casadi based limitations apply
