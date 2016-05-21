import setup as st
import numpy as np
from solution import Solution
from random import random, randint
from math import pi

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


def _angleCorrection(angle):
    if abs(angle) > pi:
        return angle - 2*pi*np.sign(angle)
    return angle
# =============================================================================
# ========================== RECOMBINATION FUNCTIONS ==========================
# =============================================================================

def discreteRecomb(p1, p2):
    childObjvar = _discListRecomb(p1.objvar, p2.objvar)
    childMutpace = _discListRecomb(p1.mutpace, p2.mutpace)
    childRot = _discListRecomb(p1.rot, p2.rot)

    return Solution(objvar=childObjvar, mutpace=childMutpace, rot=childRot)


def interpolationRecomb(p1, p2):
    alpha = 0.5 if st.childAverage else random()

    childObjvar = _interpListRecomb(p1.objvar, p2.objvar, alpha)
    childMutpace = _interpListRecomb(p1.mutpace, p2.mutpace, alpha)
    childRot = _interpListRecomb(p1.rot, p2.rot, alpha)

    # Corrects any possibly out of range values of rot
    childRot = map(_angleCorrection, childRot)

    return Solution(objvar=childObjvar, mutpace=childMutpace, rot=childRot)


def hibridRecomb(p1, p2):
    # Discrete recombination of the object values
    childObjvar = _discListRecomb(p1.objvar, p2.objvar)

    # Interpolating recombination of the strategy parameters
    alpha = 0.5 if st.childAverage else random()
    childMutpace = _interpListRecomb(p1.mutpace, p2.mutpace, alpha)
    childRot = _interpListRecomb(p1.rot, p2.rot, alpha)

    # Corrects any possibly out of range values of rot
    childRot = map(_angleCorrection, childRot)

    return Solution(objvar=childObjvar, mutpace=childMutpace, rot=childRot)
