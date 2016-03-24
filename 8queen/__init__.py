from util import *
from pattern import *



def __init__():
    max_fit = 10000
    
    n_queen = 8
    n_species = 100
    n_elements_tourment = 5
    mean = []
    
    b = calculateBits(n_queen)
    species = []
    for i in range(n_species):
        pattern = Pattern(n_queen, b)
        species.append(pattern)
        
    species.sort(reverse = True)
    p1 = species[0]
    p2 = species[1]
    
    
    print '\n'.join(map(str,species))
    
    while(species[0].fit != 1 and FitCounter.counter < max_fit):
        parents = tournament(n_elements_tourment)[:2]
        children = crossOver(species[parents[0]], species[parents[1]], n_queen, b)
        species += children
        species.sort(reverse = True)
        species.pop()
        species.pop()
        mean.append(sum([x.fit for x in species])/max(n_species, 1))
        
    print "Parou com contador " + str(FitCounter.counter)
    print '\n'.join(map(str,species))
    
    print mean
    
    

if __name__ == '__main__':
    __init__()    