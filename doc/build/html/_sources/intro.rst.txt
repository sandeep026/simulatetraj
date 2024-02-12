Problem
=======

Using simulatetraj, initial value problems can be solved numerically. In
the backend, an adaptive numerical integration is performed using CVODES
from the SUNDIALS suite.

Given initial state :math:`x(t_0)=x_0` and control inputs :math:`u(t)` on :math:`t \in [t_0,t_f]`, 
the state trajectory :math:`x(t)` is computed for the explicit
differential equation :math:`\dot{x}=f(x,u,t,p)`.

+------------+------------------+------------------------+
|Symbol      | Description      |Dimensions              |
+============+==================+========================+
|:math:`x(t)`| State vector     |:math:`\mathbb{R}^{n_x}`|
+------------+------------------+------------------------+
|:math:`u(t)`| Control vector   |:math:`\mathbb{R}^{n_u}`|
+------------+------------------+------------------------+
|:math:`p`   | Parameter vector |:math:`\mathbb{R}^{n_p}`|
+------------+------------------+------------------------+
|:math:`t`   | time             |:math:`\mathbb{R}^{1}`  |
+------------+------------------+------------------------+

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
|ipykernel        |6.29.1            |
+-----------------+------------------+
|numpy            | 1.26.4           |
+-----------------+------------------+
|matplotlib-inline| 0.1.6            |
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
