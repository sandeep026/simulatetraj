# %% [markdown]
# ### Optimal control problem 1
# 
# Matthew Kelly: An Introduction to Trajectory Optimization: How to Do Your Own Direct Collocation

# %% [markdown]
# * import the packages
# * serial multiple shooting (loop)
# * parallel multiple shooting (map)

# %%
from simulatetraj import Simulate
import casadi as cs
import matplotlib.pyplot as plt
loop=True
map=True

# %% [markdown]
# * create a simulate object and define the dynamics
# * set integration steps per interval to 1 for multiple shooting
# * specify BCs for the OCP

# %%
a=Simulate(cs.MX(2),cs.MX(1),cs.MX(0))
f=cs.vertcat(a.x[1],a.u)
a.set_ode(f)
m=cs.MX(1)
x0=cs.DM([0,0])
xf=cs.DM([1,0])

# %% [markdown]
# * create opti object
# * write code for multiple shooting transcription
# * initial guess for NLP
# * solve using IPOPT and plot

# %%
if loop:
    nlp=cs.Opti()
    #multiple shooting
    N=20
    grid=cs.linspace(0,1,N+1)
    X=nlp.variable(int(cs.evalf(a.n_x)),N+1)
    U=nlp.variable(int(cs.evalf(a.n_u)),N)
    obj=cs.sumsqr(U)*(grid[1]-grid[0])
    nlp.minimize(obj)
    nlp.subject_to(X[:,0]-x0==0)
    for i in range(N):
        a.set_grid(grid[i],grid[i+1],m)
        a.start(X0=X[:,i],U=U[:,i],tol=1e-12)
        nlp.subject_to(a.r['xf']-X[:,i+1]==0)
    nlp.subject_to(X[:,-1]-xf==0)
    nlp.solver('ipopt')
    nlp.set_initial(X[0,:],cs.np.linspace(0,1,N+1))
    nlp.set_initial(X[1,:],cs.np.linspace(0,1,N+1))
    nlp.set_initial(U,cs.np.linspace(0,1,N))
    sol=nlp.solve()
    obj_val=sol.value(nlp.f)
    print(f'Objective value: Paper - 12 | code - {obj_val}')
    plt.figure()
    plt.plot(grid.full(),sol.value(X[0,:]),label='x_1')
    plt.plot(grid.full(),sol.value(X[1,:]),label='x_2')
    plt.xlabel('time [s]')
    plt.legend()
    plt.grid(True)
    plt.savefig('box.svg')
    plt.show()
    plt.figure()
    plt.step(grid.full(),cs.np.hstack((cs.np.nan,sol.value(U))),label='u')
    plt.legend()
    plt.xlabel('time [s]')
    plt.grid(True)
    plt.savefig('boc.svg')
    plt.show()
else:
    pass    

# %%
if  map:
    nlp=cs.Opti()
    #multiple shooting
    N=20
    grid=cs.linspace(0,1,N+1)
    X=nlp.variable(int(cs.evalf(a.n_x)),N+1)
    U=nlp.variable(int(cs.evalf(a.n_u)),N)
    obj=cs.sumsqr(U)*(grid[1]-grid[0])
    st=cs.MX.sym('st',int(cs.evalf(a.n_x)),1)
    co=cs.MX.sym('co',int(cs.evalf(a.n_u)),1)
    Ti=cs.MX.sym('ti',1,1)
    Tf=cs.MX.sym('tf',1,1)
    a.set_grid(Ti,Tf,m)
    a.start(X0=st,U=co,tol=1e-12)
    int_fun=cs.Function('int_fun',[Ti,Tf,st,co],[a.r['xf']])
    int_map=int_fun.map(N,'thread',2)
    nlp.minimize(obj)
    nlp.subject_to(X[:,0]-x0==0)
    XN=int_map(grid[0:N],grid[1:N+1],X[:,0:N],U)
    nlp.subject_to(XN-X[:,1:N+1]==0)
    nlp.subject_to(X[:,-1]-xf==0)
    nlp.solver('ipopt')
    nlp.set_initial(X[0,:],cs.np.linspace(0,1,N+1))
    nlp.set_initial(X[1,:],cs.np.linspace(0,1,N+1))
    nlp.set_initial(U,cs.np.linspace(0,1,N))
    sol=nlp.solve()
    obj_val=sol.value(nlp.f)
    print(f'Objective value: Paper - 12 | code - {obj_val}')    
    plt.figure()
    plt.plot(grid.full(),sol.value(X[0,:]),label='x_1')
    plt.plot(grid.full(),sol.value(X[1,:]),label='x_2')
    plt.legend()
    plt.grid(True)
    plt.show()
    plt.figure()
    plt.step(grid.full(),cs.np.hstack((cs.np.nan,sol.value(U))),label='u')
    plt.legend()
    plt.grid(True)
    plt.show()
else:
    pass    


