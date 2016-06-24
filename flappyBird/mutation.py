import numpy as np
from copy import deepcopy
from individual import Individual
from math import pi, tan
from neural_network import NUM_WEIGHTS as dimensions
from setup import SIGMA_MIN

# Default learning rates. Fixed at first, based on the problem dimension but may be
# functions
lr_single_sd = 1/np.sqrt(dimensions)

lr_multiple_sd1 = 1/np.sqrt(2*np.sqrt(dimensions))
lr_multiple_sd2 = 1/np.sqrt(2*dimensions)
beta = pi/36

def single_sd (individual):
    individual = deepcopy(individual)

    # Updates the first mutation pace
    individual.sigmas[0] *= np.exp(lr_single_sd * np.random.normal(0, 1))
        
    # Checking if the mutation pace is lower then the threshold
    if individual.sigmas[0] < SIGMA_MIN:
        individual.mutpace[0] = SIGMA_MIN
            
    # Mapping fn to update all objective variables
    def obj_var_mutation (x):
        return x + (individual.sigmas[0] * np.random.normal(0,1))
        
    # Updating remaining vars
    individual.objvars = map(obj_var_mutation, individual.objvars)
    individual.compute_fitness()
    
    return individual

def multiple_sd (individual):
    individual = deepcopy(individual)

    # --- Mutate standard deviations ---
    common = lr_multiple_sd2 * np.random.normal(0, 1)
    # Mutate one standard deviation
    def mutate_one_sd (sd):
        new_sd = sd * np.exp(common + lr_multiple_sd1*np.random.normal(0, 1))
        return max(SIGMA_MIN, new_sd)
    
    individual.sigmas = map(mutate_one_sd, individual.sigmas)

    # --- Mutate object variables ---
    for i in range(0, dimensions):
        individual.objvars[i] += individual.sigmas[i] * np.random.normal(0, 1)

    individual.compute_fitness()

    return individual
