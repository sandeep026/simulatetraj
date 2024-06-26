.. simulatetraj documentation master file, created by
   sphinx-quickstart on Fri Feb  9 10:49:11 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to simulatetraj's documentation!
========================================

Using simulatetraj, initial value problems can be solved numerically. In
the backend, adaptive numerical integration using backward difference formula/Adam Moulton Bashfort method 
is performed using CVODES from the SUNDIALS suite. The implementation solely relies on CasADi's integrator
class in the backend.

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

.. toctree::
   :maxdepth: 2
   :caption: Introduction:

   intro.rst

.. toctree::
   :maxdepth: 2
   :caption: Examples:

   eg.rst

.. toctree::
   :maxdepth: 2
   :caption: Trajectory optimization:

   opti.rst
   examples/block_optimal.ipynb
   examples/larson.ipynb


.. toctree::
   :maxdepth: 2
   :caption: API:

   api.rst


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
