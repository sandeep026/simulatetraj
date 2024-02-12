Advanced
========

The integrator class can be used in conjunction with *trajectory
optimization*, where the symbolic primitives can be passed for initial
state and control inputs. This can be embedded in an optimization
problem and solved for the optimal control input vector. See examples
folder where single and multiple shooting methods have been implemented
and solved.

.. code:: python

   c=Simulate(cs.MX(1),cs.MX(1))
   c.set_grid(cs.MX.sym('tf',1,1),cs.MX.sym('tf',1,1),cs.MX(10))
   f=2*c.t+c.u
   c.set_ode(f)
   x0=cs.DM([0])
   c.start(x0,cs.MX.sym('u',1,10))  
