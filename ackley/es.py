import setup as st
import parent_selection as ps
import recombination as rcb
import mutation as mut
import survivor_selection as ss
from solution import Solution
from copy import deepcopy
import sys

parentSelectionfn = getattr(sys.modules['parent_selection'], st.parentSelectionFn)
recombfn = getattr(sys.modules['recombination'], st.recombinationFn)
mutationfn = getattr(sys.modules['mutation'], st.mutationFn)

nMutationTrials = 5

def iteration (population):
    
    children = list()
    
    # Generate st.childrenRation*len(population) children
    while len(children) < st.childrenRatio*len(population):
        # Select parents
        parents = parentSelectionfn(population)
        # Generate a child
        child = recombfn(parents[0], parents[1])
        # Generate nMutationTrials mutated versions of the child
        trials = list()
        for i in range(0, nMutationTrials):
            trials.append(mutationfn(child))
        # Add the most fit mutation to the children list
        bestMutation = max(trials, key=(lambda x: x.fitness))
        children.append(bestMutation)

    population = ss.survivorSelection(population, children)

    return population

def mainLoop (population):
    itNum = 0
    while itNum < st.maxIterations:
        population = iteration(population)
        if population[0].fitness == 0:
            print "Solution found!"
            break
        #else:
            #print population[0].fitness
        
        if itNum % 10 == 0:
            print str(itNum) + '   ' + str(map(lambda x: x.fitness, population))
        itNum += 1

    if itNum == st.maxIterations:
        print ("Maximum number of iterations reached. Best fitness found was " +
            str(population[0].fitness))


def init ():
    pop = []
    i = 0
    while i < st.popcap:
        pop.append(Solution())
        i += 1
    mainLoop(pop)

init()
