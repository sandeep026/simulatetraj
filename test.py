from simulate import Simulate
import casadi as cs
import matplotlib.pyplot as plt
a=Simulate(n_x=cs.MX(2),n_p=cs.MX(1))
a.set_grid(cs.MX(0),cs.MX(10),cs.MX(25))
f=cs.vertcat((1-a.x[1]**2)*a.x[0]-a.x[1]+0.2*a.t-1,a.x[0])+a.p
a.set_ode(f)
x0=cs.DM([0,0])
a.start(X0=cs.horzcat(x0),P=cs.DM(0))
r=a.r
t=a.t_grid
a.plot_sol()

a=Simulate(n_x=cs.MX(2),n_u=cs.MX(1),n_p=cs.MX(1))
a.set_grid(cs.MX(0),cs.MX(10),cs.MX(25))
f=cs.vertcat((1-a.x[1]**2)*a.x[0]-a.x[1]+a.u,a.x[0])+a.p
a.set_ode(f)
x0=cs.DM([0,0])
a.start(X0=cs.horzcat(x0),U=cs.linspace(-1,1,25).T,P=cs.DM(0))
r=a.r
t=a.t_grid
a.plot_sol()
#t**2
b=Simulate(cs.MX(1))
b.set_grid(cs.MX(0),cs.MX(10),cs.MX(100000))
f=2*b.t
b.set_ode(f)
x0=cs.DM([0])
b.start(x0)
b.plot_sol()
print('Global error x(N+1) for xdot=2t:',cs.evalf(b.r['xf'][-1]-100))
b=Simulate(cs.MX(1))
b.set_grid(cs.MX(0),cs.MX(10),cs.MX(100000))
f=2*b.t
b.set_ode(f)
x0=cs.DM([0])
b.start(x0,tol=1e-12)
b.plot_sol()
print('Global error x(N+1) for xdot=2t:',cs.evalf(b.r['xf'][-1]-100))
#lotka voltera/prey predator
d=Simulate(n_x=cs.MX(2),n_p=cs.MX(2))
d.set_grid(cs.MX(0),cs.MX(15),cs.MX(1000))
f=cs.vertcat(d.x[0]-d.p[0]*d.x[0]*d.x[1],-d.x[1]+d.p[1]*d.x[0]*d.x[1])
d.set_ode(f)
x0=cs.DM([20,20])
p=cs.DM([0.01,0.02])
d.start(X0=x0,P=p,tol=1e-8)
#d.plot_sol()
plt.plot(cs.evalf(d.r['xf'][0,:]),cs.evalf(d.r['xf'][1,:]).full(),'o')
plt.show()
#
e=Simulate(n_x=cs.MX(1),n_u=cs.MX(1),n_p=cs.MX(1))
e.set_grid(cs.MX(0),cs.MX(15),cs.MX(1000))
f=e.p*e.x+cs.exp(-0.01*e.t)*e.u
e.set_ode(f)
x0=cs.DM([20])
p=-cs.DM([0.1])
u=5*cs.sin(1*cs.linspace(0,15,1000).T)
e.start(X0=x0,U=u,P=p)
e.plot_sol()
#symbolic integrator function
c=Simulate(cs.MX(1),cs.MX(1))
c.set_grid(cs.MX.sym('tf',1,1),cs.MX.sym('tf',1,1),cs.MX(10))
f=2*c.t+c.u
c.set_ode(f)
x0=cs.DM([0])
c.start(x0,cs.MX.sym('u',1,10))
try:
    c.plot_sol()
except:
    print('Error catched for plotting symbolic')    