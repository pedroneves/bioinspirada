import random as rd
import setup as st
import fitness as ft

# Represents a individual in Evolutive Strategy for Ackley's function
class Solution:
    # Object Variables
    objvar = None
    
    # Mutation paces
    mutpace = None
    
    # Angle rotations
    rot = None
    
    # Amount of dimensions
    dim = 0
    
    # Fitness
    fitness = 0
    
    def __init__(self):
        self.dim = st.dims
        self.objvar = range(st.dims)
        self.mutpace = range(st.dims)
        self.rot = range((st.dims*(st.dims - 1)/2))
        
        i = 0
        while(i < st.dims):
            self.objvar[i] = rd.uniform(-15,15)
            self.mutpace[i] = rd.uniform(0, st.mutpacerange)
            i+=1
            
        i = 0
        while(i < len(self.rot)):
            self.rot[i] = rd.uniform(-15,15)
            i+=1
            
        self.fitness = ft.ackley(self)
        
    def __str__ (self):
        return ("Solution {0} - \n" + str(self.objvar) + "\n" + str(self.mutpace) + "\n" + str(self.rot)).format(self.fitness)
        
            