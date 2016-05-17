import setup as st
from solution import Solution

def init ():
    pop = []
    i = 0
    while i < st.popcap:
        pop.append(Solution())
        i += 1
        
    return pop