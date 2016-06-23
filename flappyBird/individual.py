from neural_network import N_LAYERS, NODES_PER_LAYER
from random import uniform
from math import pi

SIGMA_MIN = 0.0001
SIGMA_MAX = 5

class Individual:
    def __init__(self, objvars=None, sigmas=None, alphas=None):
        self.dims = N_LAYERS*NODES_PER_LAYER
        
        # Object variables initialization
        if objvars == None:
            self.objvars = random_list(size)
        else:
            self.objvars = objvars

        # Mutation paces initialization
        if sigmas == None:
            self.sigmas = random_list(size, SIGMA_MIN, SIGMA_MAX)
        else:
            self.sigmas = sigmas

        # Rotation angles initialization
        if alphas == None:
            self.alphas = random_list(dims*(dims-1)/2, -pi, pi)
        else:
            self.alphas = alphas

        self.fitness = play_game()


    def random_list(size, minval=-1, maxval=1):
        list = list()
        
        while len(list) < length:
            list.append(uniform(minval, maxval))

        return list

    # TODO
    def play_game():
        return