import numpy as np
from individual import Individual
from math import pi
from random import random, randint
from setup import CHILD_AVERAGE

# =============================================================================
# ============================= UTILITY FUNCTIONS =============================
# =============================================================================

def _disc_list_recomb(list1, list2):
    result = list()
    
    for i in range(0, len(list1)):
        result.append(list1[i] if random() < 0.5 else list2[i])
    
    return result


def _interp_list_recomb(list1, list2, alpha):
    result = list()

    for i in range(0, len(list1)):
        result.append(alpha*list1[i] + (1-alpha)*list2[i])

    return result


def _angle_correction(angle):
    if abs(angle) > pi:
        return angle - 2*pi*np.sign(angle)
    return angle
# =============================================================================
# ========================== RECOMBINATION FUNCTIONS ==========================
# =============================================================================

def discrete_recomb(p1, p2):
    child_objvars = _disc_list_recomb(p1.objvars, p2.objvars)
    child_sigmas = _disc_list_recomb(p1.sigmas, p2.sigmas)
    child_alphas = _disc_list_recomb(p1.alphas, p2.alphas)

    return Individual(objvars=child_objvars, sigmas=child_sigmas, 
                      alphas=child_alphas)


def interpolation_recomb(p1, p2):
    interp_alpha = 0.5 if CHILD_AVERAGE else random()

    child_objvars = _interp_list_recomb(p1.objvars, p2.objvars, interp_alpha)
    child_sigmas = _interp_list_recomb(p1.sigmas, p2.sigmas, interp_alpha)
    child_alphas = _interp_list_recomb(p1.alphas, p2.alphas, interp_alpha)

    # Corrects any possibly out of range values of rot
    child_alphas = map(_angle_correction, child_alphas)

    return Individual(objvars=child_objvars, sigmas=child_sigmas, 
                      alphas=child_alphas)


def hibrid_recomb(p1, p2):
    # Discrete recombination of the object values
    child_objvars = _disc_list_recomb(p1.objvars, p2.objvars)

    # Interpolating recombination of the strategy parameters
    interp_alpha = 0.5 if CHILD_AVERAGE else random()
    child_sigmas = _interp_list_recomb(p1.sigmas, p2.sigmas, interp_alpha)
    child_alphas = _interp_list_recomb(p1.alphas, p2.alphas, interp_alpha)

    # Corrects any possibly out of range values of rot
    child_alphas = map(_angle_correction, child_alphas)

    return Individual(objvars=child_objvars, sigmas=child_sigmas, 
                      alphas=child_alphas)
