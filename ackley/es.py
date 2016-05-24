import setup as st
import parent_selection as ps
import recombination as rcb
import mutation as mut
import survivor_selection as ss
from solution import Solution
from copy import deepcopy

nMutationTrials = 1

def iteration (population):
    
    children = list()
    
    # Generate st.childrenRation*len(population) children
    while len(children) < st.childrenRatio:
        # Select parents
        parents = ps.globalUniformSelection(population)
        # Generate a child
        child = rcb.hibridRecomb(parents[0], parents[1])
        # Generate nMutationTrials mutated versions of the child
        trials = list()
        for i in range(0, nMutationTrials):
            trials.append(mut.multipleSd(child))
        # Add the most fit mutation to the children list
        bestMutation = max(trials, key=(lambda x: x.fitness))
        children.append(bestMutation)

    population = ss.survivorSelection(population, children)

    return population


def init ():
    pop = []
    i = 0
    while i < st.popcap:
        pop.append(Solution())
        i += 1
        
    return pop