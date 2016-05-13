import numpy as np

# ACKLEY PARAMS
c1 = 20
c2 = 0.2
c3 = 2*np.pi
rt1 = 1.0/30


def ackley (solution):
    
    def sqr (x):
        return x*x
        
    def fn1 (x):
        return np.cos(c3*x)
    
    return (-c1*np.exp( -c2*np.sqrt(rt1*( sum(map(sqr,solution.objvar)) )) )) - np.exp(rt1 * sum(map(fn1, solution.objvar))) + c1 + 1
