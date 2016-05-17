import setup as st
import numpy as np
from solution import Solution
from ackley import ackley

# Default learning pace. Fixed at first, based on the problem dimension but may be
# a function
learningRate = 1/np.sqrt(st.dims)

# Mutation non-correlated and with a single standard deviation parameter
# Although the solutions has the most complete format, in this case, only the first
# mutation pace is used
def singleSd (population):
    
    newpop = []
    i = 0
    
    while i < len(population):
        
        newSolution = Solution()
        
        # Updates the first mutation pace
        newSolution.mutpace[0] = population[i].mutpace[0] * np.exp(learningRate * np.random.normal(0, 1))
        
        # Checking if the mutation pace is lower then the threshold
        if newSolution.mutpace[0] < st.mutpacemin:
            newSolution.mutpace[0] = st.mutpacemin
            
        # Mapping fn to update all objective variables
        def objVarMutation (x):
            return x + (newSolution.mutpace[0]*np.random.normal(0,1))
        
        # Updating remaining vars
        newSolution.objvar = map(objVarMutation, population[i].objvar)
        newSolution.fitness = ackley(newSolution)
        
        if newSolution.fitness > population[i].fitness:
            newpop.append(newSolution)
        else:
            newpop.append(population[i])
        
        i += 1

    return newpop