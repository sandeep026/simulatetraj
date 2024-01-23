import casadi as cs
import matplotlib.pyplot as plt

class Simulate:
    '''
    Simulate dynamics

    given the ode, initial condition, time grid and control input as a piecewise constant function,
    the evolution of dynamics can be computed
    '''
    def __init__(self,n_x: cs.MX,n_u: cs.MX =cs.MX(0),n_p: cs.MX=cs.MX(0)):
        #scaled domain
        self.tau=cs.MX.sym('tau',1)
        # intial and final time
        self.t0=cs.MX.sym('t0',1)
        self.tf=cs.MX.sym('tf',1)
        # actual domain
        self.t=cs.MX.sym('t',1)  
        def check_n(a,b,att):
            if a.is_constant():
                if cs.ge(a,b):
                    setattr(self,att[-1],cs.MX.sym(att,int(cs.evalf(a)),1))
                    setattr(self,att,a)
                else:
                    raise ValueError(att+' must not be less than or equal to zero')
            else:
                raise TypeError(att+' must be a integer')
        check_n(n_x,cs.MX(1),'n_x')
        check_n(n_u,cs.MX(0),'n_u')
        check_n(n_p,cs.MX(0),'n_p')

    def set_grid(self,tini: cs.MX,tfin: cs.MX,N:cs.MX):
        '''
        set_grid

        Scaled domain  tau: [0,1] 

        Parameters
        ----------
        tini : cs.SX|cs.MX
            initial time
        tfin : cs.SX|cs.MX
            final time
        N : cs.SX
            number of intervals
        '''
        if N.is_constant():
            if cs.ge(N,cs.MX(1)):
                self.N=N
            else:
                raise ValueError('N must not be less than or equal to 1')
        else:
            raise TypeError('N must be a integer')
        self.time=cs.np.linspace(0,1,int(cs.evalf(N))+1)
        # constant sx mx make changes
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

    def set_ode(self,f):
        '''
        set_ode 

        set the state derivative

        Parameters
        ----------
        f : _type_
            expression for the state derivative 
        '''
        # scale ode
        self.f_s=(self.tf-self.t0)*cs.substitute(f,self.t,(self.tf-self.t0)*self.tau)
        temp=cs.vertcat(self.t0,self.tf)
        if not self.n_u.is_zero():
            temp=cs.vertcat(temp,self.u)
        else:
            pass
        if not self.n_p.is_zero():
            temp=cs.vertcat(temp,self.p)
        else:
            pass        
        dae = {'x':self.x, 't':self.tau,'u':temp, 'ode':self.f_s}
        self.x_n = cs.integrator('x_n','cvodes',dae,self.time[0],self.time[1:],{'abstol':1e-12,'reltol':1e-8})

    def set_input(self,u:cs.DM|cs.MX=None,p:cs.DM|cs.MX=None):
        '''
        set_input 

        provide control inputs for simulation

        Parameters
        ----------
        u : _type_
            _description_
        p : _type_, optional
            _description_, by default None
        '''
        temp=[self.tini,self.tfin]     
        temp2=[]
        for i,j in enumerate(temp):
            if j.is_constant():
                temp2.append(cs.evalf(j))
            else:
                temp2.append(j)    

        u_aug=cs.vertcat(cs.repmat(temp2[0],1,int(cs.evalf(self.N))), cs.repmat(temp[1],1,int(cs.evalf(self.N))))
        if self.n_u.is_zero():
            pass
        else:
            if u is not None:
                u_aug=cs.vertcat(u_aug,u)
            else:
                raise ValueError("set numerical value for the control vector")
        if self.n_p.is_zero():
            pass
        else:
            if p is not None:
                u_aug=cs.vertcat(u_aug,cs.repmat(p,1,int(cs.evalf(self.N))))
            else:
                raise ValueError("set numerical value for the parameter vector")
        self.u_aug=u_aug

    def start(self,x0:cs.DM|cs.MX):
        if isinstance(x0,(cs.MX,cs.DM)):
            pass
        else:
            raise TypeError('x0 must be of type MX/DM')
        self.x0=x0
        self.r=self.x_n(x0=x0,u=self.u_aug)
        self.tgrid=cs.linspace(self.tini,self.tfin,int(cs.evalf(self.N))+1)

    def plot_sol(self):
        if self.tini.is_constant() and self.tfin.is_constant():
            pass
        else:
            raise ValueError('No plots for symbolic maps')
        plt.figure()
        for i in range(int(cs.evalf(self.n_x))):
            plt.plot(cs.np.reshape(cs.evalf(self.tgrid).full(),-1),cs.np.reshape(cs.evalf(cs.horzcat(self.x0,self.r['xf'])).full()[i,:],-1),'-o',label='x'+str(i+1))
            plt.xlabel('time')
            plt.ylabel('state')    
            plt.grid(True)
            plt.legend()    
        plt.show()
        plt.figure()
        for i in range(int(cs.evalf(self.n_u))):
            plt.step(cs.np.reshape(cs.evalf(self.tgrid).full(),-1),cs.np.reshape(cs.evalf(cs.horzcat(cs.DM.nan(1,1),self.u_aug[i+2,:])).full()[i,:],-1),'-',label='u'+str(i+1))
            plt.xlabel('time')
            plt.ylabel('control')    
            plt.grid(True)
            plt.legend()    
            plt.show() 
