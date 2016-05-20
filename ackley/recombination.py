import setup as st
import numpy as np



def recombIntermitante(p1, p2):
	return (p1 + p2)/2.0

def recombDiscret(p1, p2):
	mask = np.random.rand(p1.shape[0]) > 0.5
	return np.vectorize(lambda p1, p2, c: p1 if c else p2)(p1,p2,mask)

