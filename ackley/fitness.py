import numpy as np
from deap import benchmarks

# Third party implementation. Ackley params cannot be changed
def ackley (lst):
	return benchmarks.ackley(lst)[0]
	

# Team's ackley implementation. 
def ackley2 (solution):
    
    # ACKLEY PARAMS
    c1 = 20
    c2 = 0.2
    c3 = 2*np.pi
    rt1 = 1.0/30
    
    def sqr (x):
        return x*x
        
    def fn1 (x):
        return np.cos(c3*x)
    
    # On the project description, the last term is
    # is defined as '1' instead of 'exp(1)'. However, with some research, the last
    # one is the correct one. The 'exp(1)' is the correct on
    return (-c1*np.exp( -c2*np.sqrt(rt1*( sum(map(sqr,solution.objvar)) )) )) - np.exp(rt1 * sum(map(fn1, solution.objvar))) + c1 + np.exp(1)