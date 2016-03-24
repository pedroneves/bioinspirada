from util import *
from pattern import *

PLOT = True

def __init__():
    max_fit = 10000    
    n_queen = 8
    n_species = 20
    n_elements_tourment = 5




    mean = []
    top = []
    
    b = calculateBits(n_queen)
    species = []
    for i in range(n_species):
        pattern = Pattern(n_queen, b)
        species.append(pattern)
        
    species.sort(reverse = True)
    
    top.append(species[0].fit)
    mean.append(sum([x.fit for x in species])/max(n_species, 1))

    while(species[0].fit != 1 and FitCounter.counter < max_fit):
        parents = tournament(n_elements_tourment)[:2]
        children = crossOver(species[parents[0]], species[parents[1]], n_queen, b)
        species += children
        species.sort(reverse = True)
        species.pop()
        species.pop()
        top.append(species[0].fit)
        mean.append(sum([x.fit for x in species])/max(n_species, 1))    
    
    print '\n'.join(map(str,species))
    print 'Interation '+ str((FitCounter.counter - n_species)/2)
    print 'Winner ' + str(species[0])
    print 'Winner ' + str(toInt(species[0].code, b))
    try:
        import matplotlib.pyplot as plt
        plt.title(str(n_queen) + ' Queen\'s problem with Evolutionary Computation.')
        plt.plot(mean, '-', label='Mean')
        plt.plot(top, '-.', label='Best')
        plt.plot([(FitCounter.counter - n_species)/2], [mean[-1]], '-o')
        plt.ylabel('Fitnnes')
        plt.xlabel('Interation')
        plt.legend(loc='best', shadow=True)
        plt.show()
    except:
        print 'attection: impossible to plot the grafic, verify if you have matplotlib installed.'


if __name__ == '__main__':
    __init__()    
