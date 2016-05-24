import random as rd
import setup as st
import fitness as ft
import math

# Represents a individual in Evolution Strategy for Ackley's function
class Solution:
    # Object Variables
    objvar = None
    
    # Mutation paces
    mutpace = None
    
    # Angle rotations (alpha values)
    rot = None
    
    # Number of dimensions
    dim = 0
    
    # Fitness
    fitness = 0
    
    def __init__(self, objvar=None, mutpace=None, rot=None):
        self.dim = st.dims
        self.objvar = range(st.dims) if objvar == None else objvar
        self.mutpace = range(st.dims) if mutpace == None else mutpace
        self.rot = range((st.dims*(st.dims - 1)/2)) if rot == None else rot
        
        i = 0
        while(i < st.dims):
            if objvar == None:
                self.objvar[i] = rd.uniform(-15,15)
            if mutpace == None:
                self.mutpace[i] = rd.uniform(0, st.mutpacerange)
            i+=1
        
        if rot == None:
            i = 0
            while(i < len(self.rot)):
                number = rd.uniform(-math.pi, math.pi)
                while number < -math.pi or number > math.pi:
                    number = rd.uniform(-math.pi, math.pi)
                
                self.rot[i] = number
                i+=1
        
        # Negative since we want to maximize the fitness
        self.fitness = -ft.ackley(self.objvar)



    def __str__ (self):
        return ("Solution {0} - \n" + str(self.objvar) + "\n" + str(self.mutpace) + "\n" + str(self.rot)).format(self.fitness)
        
            