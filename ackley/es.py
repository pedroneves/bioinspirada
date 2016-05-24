import setup as st
import parent_selection as ps
import recombination as rcb
import mutation as mut
import survivor_selection as ss
from solution import Solution
from copy import deepcopy
import sys
import matplotlib.pyplot as plt
import numpy as np

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
    done = False
    maxFit = []
    meanFit = []
    while itNum < st.maxIterations:
        population = iteration(population)
        if population[0].fitness == 0:
            print "Solution found!"
            break
        #else:
            #print population[0].fitness
        currentFit = [x.fitness for x in population]
        maxFit.append(max(currentFit))
        meanFit.append(np.mean(currentFit))

        if itNum % 10 == 0:
            print str(itNum) + '   ' + str(currentFit[0])
        itNum += 1

        if(population[0].fitness > -st.mutpacemin*10):
            break

    if itNum == st.maxIterations:
        print ("Maximum number of iterations reached. Best fitness found was " +
            str(population[0].fitness))		

    print 'maxFit'
    print '\n'.join(map(str,maxFit[::20]))

    print 'meanFit'
    print '\n'.join(map(str,meanFit[::20]))

    plt.title('Ackley function')
    plt.plot(maxFit, label = 'Max Fit')
    plt.plot(meanFit, label = 'Mean Fit')
    plt.ylabel('Fitness')
    plt.xlabel('Interations')
    plt.legend(loc='best',shadow=True)
    plt.show()    

def init ():
    pop = []
    i = 0
    while i < st.popcap:
        pop.append(Solution())
        i += 1
    mainLoop(pop)

init()
