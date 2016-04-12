import random
from genetics import Genetics
import sys

current_module = sys.modules[__name__]

maxiterations = 10000
mutprob = 0.8
popcap = 100
fitnessfnid = 'collisionFitness'

def fitnessfn (genotype):
    return getattr(current_module, fitnessfnid)(genotype)

# ftg = FenotypeToGenotype
def ftg (fenotype):
    def toBin (x):
        return ('{0:b}'.format(x)).zfill(3)

    return ''.join(map(toBin, fenotype))

def gene(genotype, index):
    return genotype[index*3:(index+1)*3]

# gtf = GenotypeToFenotype
def gtf (genotype):
    def toInt (g):
        return int(g, 2);

    def splitGenotype(i):
        return gene(genotype, i)

    return map(toInt, map(splitGenotype, range(8)))

def individual ():

    fenotype = range(8)
    random.shuffle(fenotype)

    i = {
        'genotype': ftg(fenotype),
        'fitness': 0
    }

    i['fitness'] = fitnessfn(i['genotype'])

    return i

def collisionFitness (genotype):
    fenotype = gtf(genotype);
    totalColisions = 0;

    def isInDiagonal(xp, yp, xc, yc) :
        return (abs(xp - xc) == abs(yp - yc))

    for col, row in enumerate(fenotype):
        for chkCol, chkRow in enumerate(fenotype):
            # to avoid check with himself
            if chkCol != col:
                if chkRow == row or isInDiagonal(col, row, chkCol, chkRow):
                    totalColisions += 1;

    return 1 / (1.0 + totalColisions)

def initialization ():
    i = 0
    pop = []
    while i < popcap:
        pop.append(individual())
        i += 1
    return pop

def maxfitness (population):
    m = 0
    for i in population:
        m = max(m, i['fitness'])
    return m

def stop(iterations, population):
    return iterations >= maxiterations or maxfitness == 1.0
