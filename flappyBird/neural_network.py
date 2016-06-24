from math import tanh as activation
from setup import (NUM_INPUTS as ninputs, 
                   HIDDEN_LAYERS as hl, 
                   NODES_PER_LAYER as npl)

NUM_WEIGHTS = ( (hl-1)*npl*npl      # Connections between hidden layers
                + hl*npl            # Biases
                + ninputs*npl       # Connections between inputs and fst hidden layer
                + npl               # Connections between last hidden layer and output layer
                + 1 )               # Output layer node's bias

class Neural_Network:
    def __init__(self, weights):
        if npl <= 0 or hl < 1:
            raise Exception("Neural Network settings not supported")

        self.weights = weights

    def feedforward(self, inputs):
        if len(inputs) != ninputs:
            raise Exception("Incorrect number of neural network inputs")

        return self.rec_feedforward(inputs, 1, 0)

    def rec_feedforward(self, past, layer, weight_idx):
        if layer == 2+hl:
            assert weight_idx == len(self.weights)
            return past[0]

        total_nodes = npl if layer < 1+hl else 1
        present = list()
        
        node = 0
        while node < total_nodes:
            sum_ = 0
            
            # Multiply weights and past
            for val in past:
                sum_ += self.weights[weight_idx] * val
                weight_idx += 1
            
            # Add bias
            sum_ += self.weights[weight_idx]
            weight_idx += 1

            # Add output to present
            present.append(activation(sum_))
            # Increase counter
            node += 1

        return self.rec_feedforward(present, layer+1, weight_idx)
