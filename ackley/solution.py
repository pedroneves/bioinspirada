import random as rd

# Represents a individual in Evoluive Strategy for Ackley's function
class Solution:
    # Object Variables
    objvar = None
    
    # Mutation paces
    mutpace = None
    
    # Angle rotations
    rot = None
    
    # Amount of dimensions
    dim = 0
    
    def __init__(self, dimensions):
        self.dim = dimensions
        self.objvar = range(dimensions)
        self.mutpace = range(dimensions)
        self.rot = range((dimensions*(dimensions - 1)/2))
        
        i = 0
        while(i < dimensions):
            self.objvar[i] = rd.uniform(-15,15)
            self.mutpace[i] = rd.uniform(-15,15)
            i+=1
            
        i = 0
        while(i < len(self.rot)):
            self.rot[i] = rd.uniform(-15,15)
            i+=1
        