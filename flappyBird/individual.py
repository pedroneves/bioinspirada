import neural_network
from math import pi
from random import uniform
from setup import SIGMA_MIN, SIGMA_MAX, MUTATION_TYPE

class Individual:
    def __init__(self, objvars=None, sigmas=None, alphas=None):
        self.dims = neural_network.NUM_WEIGHTS
        
        # Object variables initialization
        if objvars == None:
            self.objvars = self.random_list(self.dims)
        else:
            self.objvars = objvars

        # Mutation paces initialization
        if MUTATION_TYPE == 1:
            self.sigmas = list()
            self.sigmas.append(uniform(SIGMA_MIN, SIGMA_MAX))
        if sigmas == None:
            self.sigmas = self.random_list(self.dims, SIGMA_MIN, SIGMA_MAX)
        else:
            self.sigmas = sigmas

        # Rotation angles initialization
        if MUTATION_TYPE != 2:
            self.alphas = list()
        elif alphas == None:
            self.alphas = self.random_list(self.dims*(self.dims-1)/2, -pi, pi)
        else:
            self.alphas = alphas
        
        # Plays the game to compute fitness
        self.compute_fitness();

    def random_list(self, size, minval=-1, maxval=1):
        list_ = list()
        
        while len(list_) < size:
            list_.append(uniform(minval, maxval))

        return list_

    # TODO
    def compute_fitness(self):
        return