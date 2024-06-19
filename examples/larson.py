# %% [markdown]
# ### Optimal control problem 2
# 
# B. A. Conway and K. M. Larson : Collocation Versus Differential Inclusion in Direct Optimization

# %% [markdown]
# * import the packages
# * single shooting

# %%
from simulatetraj import Simulate
import casadi as cs
import matplotlib.pyplot as plt

# %% [markdown]
# * create a simulate object and define the dynamics
# * set the number of control intervals
# * specify BCs for the OCP

# %%
a=Simulate(cs.MX(2),cs.MX(1),cs.MX(0))
f=cs.vertcat(a.x[1],-a.x[1]+a.u)
a.set_ode(f)
N=cs.MX(50)
a.set_grid(cs.MX(0),cs.MX(2),N)
x0=cs.DM([0,0])

# %% [markdown]
# * create opti object
# * write code for single shooting transcription
# * initial guess for NLP
# * solve using IPOPT and plot

# %%
nlp=cs.Opti()
X0=nlp.variable(int(cs.evalf(a.n_x)),1)
U=nlp.variable(int(cs.evalf(a.n_u)),int(cs.evalf(N)))
obj=cs.sumsqr(U)*2/N
a.start(X0=x0,U=U,tol=1e-6)
X=cs.horzcat(X0,a.r['xf'])
nlp.minimize(obj)
nlp.subject_to(X0-x0==0)
nlp.subject_to(cs.horzcat(1,-2.694528)@X[:,-1]+1.155356==0)
nlp.solver('ipopt')
nlp.set_initial(U,cs.np.linspace(0,1,int(cs.evalf(N))))
sol=nlp.solve()
obj_val=sol.value(nlp.f)
print(f'Objective value: Paper - 0.577678 | code - {obj_val}')

# %% [markdown]
# * plot results

# %%
plt.figure()
plt.plot(cs.evalf(a.t_grid).full(),sol.value(X[0,:]),label='x_1')
plt.plot(cs.evalf(a.t_grid).full(),sol.value(X[1,:]),label='x_2')
plt.legend()
plt.grid(True)
plt.show()
plt.figure()
plt.step(cs.evalf(a.t_grid).full(),cs.np.hstack((cs.np.nan,sol.value(U))),label='u')
plt.legend()
plt.grid(True)
plt.show()

# %% [markdown]
# Note that the single shooting method is not robust and may be prone to failure. Multiple shooting methods are recommended.


