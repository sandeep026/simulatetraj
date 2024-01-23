from simulate import Simulate, cs
a=Simulate(cs.MX(2),cs.MX(1),cs.MX(1))
a.set_grid(cs.MX(0),cs.MX(10),cs.MX(100))
f=cs.vertcat((1-a.x[1]**2)*a.x[0]-a.x[1]+a.u,a.x[0])
a.set_ode(f)
a.set_input(cs.linspace(-1,1,100).T,cs.DM(0))
x0=cs.DM([0,0])
a.start(x0)
r=a.r
t=a.tgrid
a.plot_sol()
print(a.r['xf'].shape)
