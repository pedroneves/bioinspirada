import setup as st
import recombination as rec
from random import randint
from copy import deepcopy
from individual import Individual

# =============================================================================
# ============================= UTILITY FUNCTIONS =============================
# =============================================================================

def _choose_lists_from_pop(population, get_attr_fn):
    list1 = list()
    list2 = list()

    if len(population) == 0:
        return list()

    for i in range(0, population[0].dims):
        # Select individuals
        rand1 = randint(0, len(population)-1)
        rand2 = randint(0, len(population)-1)
        # Guarantee of different individuals
        while rand2 == rand1:
            rand2 = randint(0, len(population)-1)

        # Add attributes
        attr1 = get_attr_fn(population[rand1])[i]
        attr2 = get_attr_fn(population[rand2])[i]
        list1.append(attr1)
        list2.append(attr2)

    return list1, list2

# =============================================================================
# ======================== PARENT SELECTION FUNCTIONS =========================
# =============================================================================

def local_uniform_selection(population):
    rand1 = randint(0, len(population)-1)
    rand2 = rand1
    while rand2 == rand1:
        rand2 = randint(0, len(population)-1)

    return p1, p2

def global_uniform_selection(population):
    objvar_lists = _choose_lists_from_pop(population, (lambda x: x.objvars))
    sigma_lists = _choose_lists_from_pop(population, (lambda x: x.sigmas))
    alpha_lists = _choose_lists_from_pop(population, (lambda x: x.alphas))

    p1 = Individual(objvar_lists[0], sigma_lists[0], alpha_lists[0], 
                    compute_fitness=False)
    p2 = Individual(objvar_lists[1], sigma_lists[1], alpha_lists[1], 
                    compute_fitness=False)

    return p1, p2
