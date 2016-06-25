import neural_network
import flappybird as game
from math import pi
from random import uniform
from setup import SIGMA_MIN, SIGMA_MAX, MUTATION_TYPE, NUM_GAMEPLAYS

class Individual:
    def __cmp__(self, other):
        if self.fitness['score'] != other.fitness['score']:
            return self.fitness['score'] - other.fitness['score']
        else:
            return self.fitness['clock'] - other.fitness['clock']

    def __init__(self, objvars=None, sigmas=None, alphas=None, 
                 compute_fitness=True):
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
        
        if compute_fitness:
           # Plays the game to compute fitness
            self.fitness = {}
            self.compute_fitness();

    def random_list(self, size, minval=-1, maxval=1):
        list_ = list()
        
        while len(list_) < size:
            list_.append(uniform(minval, maxval))

        return list_

    def compute_fitness(self):
        nn = self.get_neural_network()
        
        scores = list()
        for i in range(NUM_GAMEPLAYS):
            score = game.play(nn)
            scores.append(score)

        mean_score = sum(map(lambda x: x['score'], scores)) / len(scores)
        mean_clock = sum(map(lambda x: x['clock'], scores)) / len(scores)

        self.fitness = {'score': mean_score, 'clock': mean_clock}

    def get_neural_network(self):
        return neural_network.Neural_Network(self.objvars)