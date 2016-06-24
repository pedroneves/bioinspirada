from individual import Individual
from math import tanh as activation
from setup import (NUM_INPUTS as ninputs, 
                   HIDDEN_LAYERS as hl, 
                   NODES_PER_LAYER as npl)

class Neural_Network:
    # TODO
    def __init__(self, weights):
        self.weights = weights

    # TODO
    def feedforward(self, inputs):
        if len(values) != ninputs:
            raise Exception("Incorrect number of neural network inputs")

        return rec_feedforward(inputs, 1, 0, 0)

    def rec_feedforward(self, past, layer, weight_idx):
        if layer == 2+hl:
            assert weight_idx == len(self.weights)
            return past[0]

        total_nodes = npl if layer < 1+hl else 1
        present = list()
        
        node = 0
        while node < npl:
            sum_ = 0
            
            # Multiply weights and past
            for val in past:
                sum_ += weights[weight_idx] * val
                weight_idx += 1
            
            # Add bias
            sum_ += weights[weight_idx]
            weight_idx += 1

            # Add output to present
            present.append(activation(sum_))

        rec_feedforward(present, layer+1, weight_idx)