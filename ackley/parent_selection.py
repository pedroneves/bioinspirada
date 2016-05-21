import setup as st
import recombination as rec
from random import randint
from copy import deepcopy
from solution import Solution

# =============================================================================
# ============================= UTILITY FUNCTIONS =============================
# =============================================================================

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
        attr1 = getAttrFn(population[rand1])[i]
        attr2 = getAttrFn(population[rand2])[i]
        list1.append(attr1)
        list2.append(attr2)

    return list1, list2

# =============================================================================
# ======================== PARENT SELECTION FUNCTIONS =========================
# =============================================================================

def localUniformSelection(population):
    rand1 = randint(0, len(population)-1)
    rand2 = rand1
    while rand2 == rand1:
        rand2 = randint(0, len(population)-1)

    # Return a copy of parents' data
    p1 = deepcopy(population[rand1])
    p2 = deepcopy(population[rand2])

    return p1, p2

def globalUniformSelection(population):
    objvarLists = _chooseListsFromPop(population, (lambda x: x.objvar))
    mutpaceLists = _chooseListsFromPop(population, (lambda x: x.mutpace))
    rotLists = _chooseListsFromPop(population, (lambda x: x.rot))

    p1 = Solution(objvarLists[0], mutpaceLists[0], rotLists[0])
    p2 = Solution(objvarLists[1], mutpaceLists[1], rotLists[1])

    return p1, p2
