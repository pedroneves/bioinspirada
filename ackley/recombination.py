import setup as st
import numpy as np
from solution import Solution
from random import random

# =============================================================================
# ============================= UTILITY FUNCTIONS =============================
# =============================================================================

def _discListRecomb(list1, list2):
    result = list()
    
    for i in range(0, len(list1)):
        result.append(list1[i] if random() < 0.5 else list2[i])
    
    return result


def _interpListRecomb(list1, list2, alpha):
    result = list()

    for i in range(0, len(list1)):
        result.append(alpha*list1[i] + (1-alpha)*list2[i])

    return result


def _chooseListsFromPop(population, getAttrFn):
    list1 = list()
    list2 = list()

    for i in range(0, st.dims):
        # Select individuals
        rand1 = randint(0, len(population)-1)
        rand2 = randint(0, len(population)-1)
        # Guarantee of different individuals
        while rand2 == rand1:
            rand2 = randint(0, len(population)-1)

        # Add attributes
        attr1 = getAttrFn(population[rand1])
        attr2 = getAttrFn(population[rand2])
        list1.append(attr1)
        list2.append(attr2)

    return list1, list2

# =============================================================================
# ========================== RECOMBINATION FUNCTIONS ==========================
# =============================================================================

def localDiscRecomb(p1, p2):
    childObjvar = _discListRecomb(p1.objvar, p2.objvar)
    childMutpace = _discListRecomb(p1.mutpace, p2.mutpace)
    childRot = _discListRecomb(p1.rot, p2.rot)

    return Solution(objvar=childObjvar, mutpace=childMutpace, rot=childRot)


def globalDiscRecomb(population):
    objvarLists = _chooseListsFromPop(population, (lambda x: x.objvar))
    mutpaceLists = _chooseListsFromPop(population, (lambda x: x.mutpace))
    rotLists = _chooseListsFromPop(population, (lambda x: x.rot))

    childObjvar = _discListRecomb(objvarLists[0], objvarLists[1])
    childMutpace = _discListRecomb(mutpaceLists[0], mutpaceLists[1])
    childRot = _discListRecomb(rotLists[0], rotLists[1])

    return Solution(objvar=childObjvar, mutpace=childMutpace, rot=childRot)


def globalInterpRecomb(population):
    objvarLists = _chooseListsFromPop(population, (lambda x: x.objvar))
    mutpaceLists = _chooseListsFromPop(population, (lambda x: x.mutpace))
    rotLists = _chooseListsFromPop(population, (lambda x: x.rot))

    alpha = 0.5 if st.childAverage else random()
    
    childObjvar = _interpListRecomb(objvarLists[0], objvarLists[1], alpha)
    childMutpace = _interpListRecomb(mutpaceLists[0], mutpaceLists[1], alpha)
    childRot = _interpListRecomb(rotLists[0], rotLists[1], alpha)

    return Solution(objvar=childObjvar, mutpace=childMutpace, rot=childRot)

        
def localInterpRecomb(p1, p2):
    alpha = 0.5 if st.childAverage else random()

    childObjvar = _interpListRecomb(p1.objvar, p2.objvar, alpha)
    childMutpace = _interpListRecomb(p1.mutpace, p2.mutpace, alpha)
    childRot = _interpListRecomb(p1.rot, p2.rot, alpha)

    return Solution(objvar=childObjvar, mutpace=childMutpace, rot=childRot)


def localHibridRecomb(p1, p2):
    # Discrete recombination of the object values
    childObjvar = _discListRecomb(p1.objvar, p2.objvar)

    # Interpolating recombination of the strategy parameters
    alpha = 0.5 if st.childAverage else random()
    childMutpace = _interpListRecomb(p1.mutpace, p2.mutpace, alpha)
    childRot = _interpListRecomb(p1.rot, p2.rot, alpha)

    return Solution(objvar=childObjvar, mutpace=childMutpace, rot=childRot)


# Recommended recombination strategy, according to the book
def globalHibridRecomb(population):
    objvarLists = _chooseListsFromPop(population, (lambda x: x.objvar))
    mutpaceLists = _chooseListsFromPop(population, (lambda x: x.mutpace))
    rotLists = _chooseListsFromPop(population, (lambda x: x.rot))

    # Discrete recombination of the object values
    childObjvar = _discListRecomb(objvarLists[0], objvarLists[1])

    # Interpolating recombination of the strategy parameters
    alpha = 0.5 if st.childAverage else random()
    childMutpace = _interpListRecomb(mutpaceLists[0], mutpaceLists[1], alpha)
    childRot = _interpListRecomb(rotLists[0], rotLists[1], alpha)

    return Solution(objvar=childObjvar, mutpace=childMutpace, rot=childRot)
