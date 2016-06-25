from heapq import heapify, heappop
from setup import GENERATIONAL, POPULATION_SIZE

def sort_survivor_selection(population, children):
    candidates = list()
    if GENERATIONAL:
        candidates = children
    else:
        candidates = population+children

    sorted_ = sorted(candidates, reverse=True)
    return sorted_[:POPULATION_SIZE]

def heap_survivor_selection(population, children):
    candidates = list()
    if GENERATIONAL:
        candidates = children
    else:
        candidates = population+children
    
    def inverse_fitness(x):
        x.fitness['score'] *= -1
        x.fitness['clock'] *= -1
        return x

    population = list()
    candidates = map(inverse_fitness, candidates)

    heapify(candidates)
    for i in range(POPULATION_SIZE):
        individual = heappop(candidates)
        population.append(individual)

    return map(inverse_fitness, population)
    

