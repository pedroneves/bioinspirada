import setup as st
import numpy as np
from solution import Solution
from random import random

def _discListRecomb(list1, list2):
    result = list()
    
    for i in range(0, len(list1)):
        result.append(list1[i] if random() < 0.5 else list2[i])
    
    return result

def _interpListRecomb(list1, list2, alpha=random()):
    result = list()

    for i in range(0, len(list1)):
        result.append(alpha*list1[i] + (1-alpha)*list2[i])

    return result

def localDiscRecomb(p1, p2):
    childObjvar = _discListRecomb(p1.objvar, p2.objvar)
    childMutpace = _discListRecomb(p1.mutpace, p2.mutpace)
    childRot = _discListRecomb(p1.rot, p2.rot)

    return Solution(objvar=childObjvar, mutpace=childMutpace, rot=childRot)

#def globalDiscRecomb(population):
#    list1 = list()
#    list2 = list()

#    for i in range(0, st.dims):
#        rand1 = randint(0, len(population)-1)
#        rand2 = randint(0, len(population)-1)
        # Guarantee of different individuals
#        while rand2 == rand1:
#            rand2 = randint(0, len(population)-1)



#def localInterpRecomb(p1, p2, childAvegare=False):

#def globalInterpRecomb(population, childAverage=False):

#localHibridRecomb(p1, p2, childAverage=False):

# Recommended recombination strategy, according to the book
#globalHibridRecomb(population, childAverage=False):

def recombIntermitante(p1, p2):
	return (p1 + p2)/2.0

def recombDiscret(p1, p2):
	mask = np.random.rand(p1.shape[0]) > 0.5
	return np.vectorize(lambda p1, p2, c: p1 if c else p2)(p1,p2,mask)

