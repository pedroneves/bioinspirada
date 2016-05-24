import setup as st
import numpy as np
from solution import Solution
from fitness import ackley
from math import pi, tan
from copy import deepcopy

# Default learning paces. Fixed at first, based on the problem dimension but may be
# functions
lrSingleSd = 1/np.sqrt(st.dims)

lrMultipleSd1 = 1/np.sqrt(2*np.sqrt(st.dims))
lrMultipleSd2 = 1/np.sqrt(2*st.dims)
beta = pi/36

# Mutation non-correlated and with a single standard deviation parameter
# Although the solutions has the most complete format, in this case, only the first
# mutation pace is used
#def singleSd (population):
#    
#    newpop = []
#    i = 0
#    
#    while i < len(population):
#        
#        newSolution = Solution()
#        
#        # Updates the first mutation pace
#        newSolution.mutpace[0] = population[i].mutpace[0] * np.exp(lrSingleSd * np.random.normal(0, 1))
#        
#        # Checking if the mutation pace is lower then the threshold
#        if newSolution.mutpace[0] < st.mutpacemin:
#            newSolution.mutpace[0] = st.mutpacemin
#            
#        # Mapping fn to update all objective variables
#        def objVarMutation (x):
#            return x + (newSolution.mutpace[0]*np.random.normal(0,1))
#        
#        # Updating remaining vars
#        newSolution.objvar = map(objVarMutation, population[i].objvar)
#        newSolution.fitness = ackley(newSolution)
#        
#        if newSolution.fitness > population[i].fitness:
#            newpop.append(newSolution)
#        else:
#            newpop.append(population[i])
#        
#        i += 1
#
#    return newpop


def singleSd (individual):
    individual = deepcopy(individual)

    # Updates the first mutation pace
    individual.mutpace[0] *= np.exp(lrSingleSd * np.random.normal(0, 1))
        
    # Checking if the mutation pace is lower then the threshold
    if newSolution.mutpace[0] < st.mutpacemin:
        newSolution.mutpace[0] = st.mutpacemin
            
    # Mapping fn to update all objective variables
    def objVarMutation (x):
        return x + (individual.mutpace[0] * np.random.normal(0,1))
        
    # Updating remaining vars
    individual.objvar = map(objVarMutation, individual.objvar)
    individual.fitness = ackley(individual)
    
    return individual

def multipleSd (individual):
    individual = deepcopy(individual)

    # --- Mutate standard deviations ---
    common = lrMultipleSd2 * np.random.normal(0, 1)
    # Mutate one standard deviation
    def mutateOneSd (sd):
        new_sd = sd * np.exp(common + lrSingleSd1*np.random.normal(0, 1))
        return max(st.mutpacemin, new_sd)
    
    individual.mutpace = map(mutateOneSd, individual.mutpace)

    # --- Mutate object variables ---
    for i in range(0, st.dims):
        individual.objvar[i] += individual.mutpace[i] * np.random.normal(0, 1)

    return individual

# Unfinished   
#def correlatedSd (individual):
#    individual = deepcopy(individual)
#
#    # --- Mutate standard deviations ---
#    common = lrMultipleSd2 * np.random.normal(0, 1)
#    # Mutate one standard deviation
#    def mutateOneSd (sd):
#        new_sd = sd * np.exp(common + lrSingleSd1*np.random.normal(0, 1))
#        return max(st.mutpacemin, new_sd)
#
#    individual.mutpace = map(mutateOneSd, individual.mutpace)
#
#    # --- Mutate rotation angles ---
#    # Mutate one rotation angle
#    def mutateOneAngle (angle):
#        angle += beta*np.random.normal(0, 1)
#        if abs(angle) > pi:
#            angle -= 2*pi*np.sign(angle)
#        return angle
#
#    individual.rot = map(mutateOneAngle, individual.rot)
#
#    # --- Build covariance matrix ---
#    c = list()
#
#    while len(c) != st.dims:
#        line = [0]*st.dims
#
#    for i in range(0, st.dims):
#        for j in range(0, st.dims):
#            if i == j:
#                c[i][j] = pow(individual.mutpace[i], 2)
#            else:
#
#    # --- Mutate object variables ---
#
#
#    return individual