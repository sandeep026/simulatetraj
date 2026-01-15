import casadi as cs
import matplotlib.pyplot as plt

class Simulate:
    '''
    A class to numerically solve initial value problems using CVODES.

    Attributes
    ----------
    tau : cs.MX
        scaled time domain variable
    
    t0 : cs.MX
        initial time
    
    tf : cs.MX
        final time
    
    t : cs.MX
        time domain variable
    
    N : cs.MX
        number of intervals
    
    t_grid_s : cs.MX
        discrete scaled grid
    
    t_grid : cs.MX
        discrete grid
    
    f_s : cs.MX
        scaled dynamics
    
    x_n : cs.Function
        function object for the integrator
    
    x0 : cs.MX
        initial state
    
    r : dict
        dictionary of results from integration
    
    pt_val :
        numerical value of the parameter vector         

    Parameters
    ----------
    n_x : cs.MX
        number of states
    n_u : cs.MX, optional
        number of controls, by default cs.MX(0)
    
    n_p : cs.MX, optional
        number of parameters, by default cs.MX(0)   

    Raises
    ------
    ValueError
        input should not be less than or equal to zero
    TypeError
        input must be an integer

    Examples
    --------
    >>> from simulate import Simulate
    >>> import casadi as cs
    >>> a=Simulate(n_x=cs.MX(2),n_u=cs.MX(1),n_p=cs.MX(1))            

    '''
    def __init__(self,n_x: cs.MX,n_u: cs.MX =cs.MX(0),n_p: cs.MX=cs.MX(0)):
        #scaled domain
        self.tau=cs.MX.sym('tau',1)
        # initial and final time
        self.t0=cs.MX.sym('t0',1)
        self.tf=cs.MX.sym('tf',1)
        # actual time domain
        self.t=cs.MX.sym('t',1)
        # check consistency of inputs entered
        def check_n(a,b,att):
            '''
            check_n _summary_

            _extended_summary_

            Parameters
            ----------
            a : _type_
                _description_
            b : _type_
                _description_
            att : _type_
                _description_

            Raises
            ------
            ValueError
                _description_
            TypeError
                _description_
            '''
            if a.is_constant():
                if cs.ge(a,b):
                    if a.is_zero():
                        setattr(self,att[-1],cs.MX())
                    else:
                        setattr(self,att[-1],cs.MX.sym(att[-1],int(cs.evalf(a)),1))
                    setattr(self,att,a)
                else:
                    raise ValueError(att+' must not be less than or equal to zero')
            else:
                raise TypeError(att+' must be a integer')
        check_n(n_x,cs.MX(1),'n_x')
        check_n(n_u,cs.MX(0),'n_u')
        check_n(n_p,cs.MX(0),'n_p')
        # set default values
        self.N=cs.MX()
        self.t_grid_s=cs.DM()
        self.t_grid=cs.DM()
        self.f_s=cs.MX()
        self.x_n=cs.Function()
        self.x0=cs.MX()
        self.r={}
        self.pt_val=cs.MX()

    def set_grid(self,tini: cs.MX,tfin: cs.MX,N:cs.MX):
        '''
        Define the time grid for numerical integration.

        Parameters
        ----------
        tini : cs.MX
            initial time

        tfin : cs.MX
            final time

        N : cs.MX
            number of intervals

        Raises
        ------
        ValueError
            N must not be less than or equal to 1
        TypeError
            N must be a integer
        ValueError
            Time must be positive
        ValueError
            Final time must be greater than initial time

        Examples
        --------
        >>> a.set_grid(cs.MX(0),cs.MX(10),cs.MX(25))    
        '''
        if N.is_constant():
            if cs.ge(N,cs.MX(1)):
                self.N=N
            else:
                raise ValueError('N must not be less than or equal to 1')
        else:
            raise TypeError('N must be a integer')
        # scaled domain
        self.t_grid_s=cs.np.linspace(0,1,int(cs.evalf(N))+1)
        # check the sign of final and initial time 
        temp=[tini,tfin]
        temp2=['tini','tfin']
        temp3=0
        for i,j in enumerate(temp):
            if j.is_constant():
                if bool(cs.ge(j,cs.DM(0))):
                    setattr(Simulate,temp2[i],j)
                else:
                    raise ValueError(temp2[i]+" is not positive")
            else:
                setattr(Simulate,temp2[i],j)
                temp3=1
        if temp3==0:
            if bool(cs.gt(temp[1],temp[0])):
                pass
            else:
                raise ValueError('Final time must be greater than initial time')
        else:
            pass
        # due to scaling final and initial time are parameter of the ode
        self.pt_val=cs.vertcat(self.tini,self.tfin)

    def set_ode(self,f):
        '''
        Define the state derivative vector

        Parameters
        ----------
        f : cs.MX
            expression for the state derivative 

        Examples
        --------

        >>> f=cs.vertcat((1-a.x[1]**2)*a.x[0]-a.x[1]+a.u,a.x[0])+a.p
        >>> a.set_ode(f)    
        '''
        # scale ode
        self.f_s=(self.tf-self.t0)*cs.substitute(f,self.t,(self.tf-self.t0)*self.tau)
        self.ode = {'x':self.x, 't':self.tau,'u':self.u, 'p': cs.vertcat(self.t0,self.tf,self.p),'ode':self.f_s}

    def start(self,X0:cs.DM|cs.MX,U:cs.DM|cs.MX=cs.MX(),P:cs.DM|cs.MX=cs.MX(),tol:float=1e-3):
        '''
        Simulate the dynamics with initial condition with x0, control input u and parameter p
        using CVODES.

        (abstol,reltol)=(tol,100*tol)

        Parameters
        ----------
        X0 : cs.DM | cs.MX
            initial condition for the state

        U : cs.DM | cs.MX, optional
            control input, by default None

        P : cs.DM | cs.MX, optional
            parameter vector, by default None

        tol : float
            tolerance for CVODES, by default 1e-3            
            
        Raises
        ------
        TypeError
            x0 must be of type MX/DM

        Examples
        --------
        >>> x0=cs.DM([0,0])
        >>> a.start(X0=cs.horzcat(x0),U=cs.linspace(-1,1,25).T,P=cs.DM(0))
        >>> r=a.r
        >>> t=a.t_grid
        '''
        if isinstance(X0,(cs.MX,cs.DM)):
            pass
        else:
            raise TypeError('x0 must be of type MX/DM')
        
        if U.is_empty():
            if self.n_u.is_zero():
                pass
            else:
                raise ValueError('control input required')
        else:
            if self.n_u.is_zero():
                raise ValueError('control inputs not required')
            else:
                if cs.eq(cs.evalf(self.n_u),cs.evalf(U.shape[0])) and cs.eq(cs.evalf(self.N),cs.evalf(U.shape[1])) :
                    pass
                else:
                    raise ValueError('wrong dimension for control matrix')

        if P.is_empty():
            if self.n_p.is_zero():
                pass
            else:
                raise ValueError('parameter required')
        else:
            if self.n_p.is_zero():
                raise ValueError('parameter not required')
            else:
                if cs.eq(cs.evalf(self.n_p),cs.evalf(P.shape[0])) and cs.eq(cs.DM(1),cs.evalf(P.shape[1])) :
                    pass
                else:
                    raise ValueError('wrong dimension for control matrix')                
        self.x0=X0
        self.u_val=U
        self.x_n = cs.integrator('x_n','cvodes',self.ode,self.t_grid_s[0],self.t_grid_s[1:],{'abstol':tol,'reltol':100*tol})
        self.r=self.x_n(x0=self.x0,u=U,p=cs.vertcat(self.pt_val,P))
        self.t_grid=cs.linspace(self.tini,self.tfin,int(cs.evalf(self.N))+1)

    def plot_sol(self):
        '''
        Plots the solution obtained.

        Raises
        ------
        ValueError
            No plots for symbolic maps
        '''
        if self.tini.is_constant() and self.tfin.is_constant():
            pass
        else:
            raise ValueError('No plots for symbolic maps')
        if cs.ge(self.N,50):
            sty='-'
        else:
            sty='o-'    
        X=cs.evalf(cs.horzcat(self.x0,self.r['xf'])).full()
        for i in range(int(cs.evalf(self.n_x))):
            plt.figure()
            plt.plot(cs.np.reshape(cs.evalf(self.t_grid).full(),-1),cs.np.reshape(X[i,:],-1),sty,label='x'+str(i+1))
            plt.xlabel('time')
            plt.ylabel('state')
            plt.grid(True)
            plt.legend()
        plt.show()
        if self.n_u.is_zero():
            pass
        else:
            U=cs.evalf(cs.horzcat(cs.DM.nan(int(cs.evalf(self.n_u)),1),self.u_val)).full()
            for i in range(int(cs.evalf(self.n_u))):
                plt.figure()
                plt.step(cs.np.reshape(cs.evalf(self.t_grid).full(),-1),cs.np.reshape(U[i,:],-1),'-',label='u'+str(i+1))
                plt.xlabel('time')
                plt.ylabel('control')
                plt.grid(True)
                plt.legend()
                plt.show()

# t0 tf N
# xdot
# x0


if __name__=='__main__':

    # multipoint_simulation-casadi
    a=Simulate(cs.MX(2),cs.MX(1),cs.MX(1))
    a.set_grid(cs.MX(0),cs.MX(10),cs.MX(25))
    f=cs.vertcat((1-a.x[0]**2)*a.x[1]-a.x[0]+a.u,a.x[1])+a.p
    a.set_ode(f)
    x0=cs.DM([0,0])
    a.start(X0=x0,U=cs.linspace(-1,1,25).T,P=cs.DM(0))
    r=a.r
    t=a.t_grid
    a.plot_sol()
    print(a.r['xf'].shape)

    #t**2
    b=Simulate(cs.MX(1))
    b.set_grid(cs.MX(0),cs.MX(10),cs.MX(100000))
    f=2*b.t
    b.set_ode(f)
    x0=cs.DM([0])
    b.start(x0)
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
    plt.plot(cs.evalf(d.r['xf'][0,:]),cs.evalf(d.r['xf'][1,:]),'o')
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