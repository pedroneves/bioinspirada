from math import pi
from random import uniform
from setup import (NUM_INPUTS as ninputs, 
                   HIDDEN_LAYERS as hl, 
                   NODES_PER_LAYER as npl)

class Individual:
    def __init__(self, objvars=None, sigmas=None, alphas=None):
        # ===============================================
        # === Number of weights in the neural network ===
        # ===============================================
        if npl <= 0 or hp < 1:
            raise Exception("Neural Network settings not supported")

        self.dims = 0
        self.dims += (hl-1)*npl*npl     # Connections between hidden layers
        self.dims += hl*npl             # Biases
        self.dims += ninputs*npl        # Connections between inputs and fst hidden layer
        self.dims += npl                # Connections between last hidden layer and output layer
        self.dims += 1                  # Output layer node's bias
        # -----------------------------------------------
        
        # =================================
        # === Individual Initialization ===
        # =================================
        # Object variables initialization
        if objvars == None:
            self.objvars = random_list(self.dims)
        else:
            self.objvars = objvars

        # Mutation paces initialization
        if sigmas == None:
            self.sigmas = random_list(self.dims, SIGMA_MIN, SIGMA_MAX)
        else:
            self.sigmas = sigmas

        # Rotation angles initialization
        if alphas == None:
            self.alphas = random_list(dims*(dims-1)/2, -pi, pi)
        else:
            self.alphas = alphas
        # ---------------------------------
        
        # Plays the game to compute fitness
        self.fitness = play_game()


    def random_list(size, minval=-1, maxval=1):
        list = list()
        
        while len(list) < length:
            list.append(uniform(minval, maxval))

        return list

    # TODO
    def play_game():
        return