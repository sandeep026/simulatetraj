Module simulate
===============

Classes
-------

`Simulate(n_x: casadi.casadi.MX, n_u: casadi.casadi.MX = MX(0), n_p: casadi.casadi.MX = MX(0))`
:   A class to numerically solve intial value problem using CVODES.
    
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
        intial state
    
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

    ### Methods

    `plot_sol(self)`
    :   Plots the solution obtained.
        
        Raises
        ------
        ValueError
            No plots for symbolic maps

    `set_grid(self, tini: casadi.casadi.MX, tfin: casadi.casadi.MX, N: casadi.casadi.MX)`
    :   Define the time grid for numerical integration.
        
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

    `set_ode(self, f)`
    :   Define the state derivative vector
        
        Parameters
        ----------
        f : cs.MX
            expression for the state derivative 
        
        Examples
        --------
        
        >>> f=cs.vertcat((1-a.x[1]**2)*a.x[0]-a.x[1]+a.u,a.x[0])+a.p
        >>> a.set_ode(f)

    `start(self, X0: casadi.casadi.DM | casadi.casadi.MX, U: casadi.casadi.DM | casadi.casadi.MX = MX(0x0), P: casadi.casadi.DM | casadi.casadi.MX = MX(0x0), tol: float = 0.001)`
    :   Simulate the dynamics with initial condition with x0, control input u and parameter p
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