import random
from genetics import Genetics
import sys

current_module = sys.modules[__name__]

maxiterations = 10000
mutprob = 0.8
popcap = 100
initializationfnid = 'randominit'
fitnessfnid = 'collisionFitness'
selectionfnid = 'rank2outof5random'
recombinationfnid = 'cutAndCrossfill'
mutationfnid = 'swapMutation'
survivingfnid = 'replaceWorst'
stopfnid = 'stop'

def fitnessfn (genotype):
    return getattr(current_module, fitnessfnid)(genotype)

def mutationfn (solution):
    return getattr(current_module, mutationfnid)(solution)

# ptg = PhenotypeToGenotype
def ptg (phenotype):
    def toBin (x):
        return ('{0:b}'.format(x)).zfill(3)

    return ''.join(map(toBin, phenotype))

def feature(genotype, index):
    return genotype[index*3:(index+1)*3]

# gtp = GenotypeToPhenotype
def gtp (genotype):
    def toInt (g):
        return int(g, 2);

    def splitGenotype(i):
        return feature(genotype, i)

    return map(toInt, map(splitGenotype, range(8)))

def genotypeToList (genotype):
    r = []
    i = 0
    while(i < 8):
        r.append(feature(genotype, i))
        i += 1

    return r

def individual ():

    phenotype = range(8)
    random.shuffle(phenotype)

    i = {
        'genotype': ptg(phenotype),
        'fitness': 0
    }

    i['fitness'] = fitnessfn(i['genotype'])

    return i

def collisionFitness (genotype):
    phenotype = gtp(genotype);
    totalColisions = 0;

    def isInDiagonal(xp, yp, xc, yc) :
        return (abs(xp - xc) == abs(yp - yc))

    for col, row in enumerate(phenotype):
        for chkCol, chkRow in enumerate(phenotype):
            # to avoid check with himself
            if chkCol != col:
                if chkRow == row or isInDiagonal(col, row, chkCol, chkRow):
                    totalColisions += 1;

    return 1 / (1.0 + totalColisions)

def randominit ():
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

def avgfitness (population):
    m = 0
    for i in population:
        m = m + i['fitness']
    m = m / len(population)
    return m

def stop(iterations, population):
    return iterations >= maxiterations or maxfitness(population) == 1.0

def cutAndCrossfill (parents):
    childGeno1 = []
    childGeno2 = []
    crossoverPoint = random.randint(1,7)
    i = 0
    r = []

    # Copy the first part
    while(i < crossoverPoint):
        childGeno1.append(feature(parents[0]['genotype'], i))
        childGeno2.append(feature(parents[1]['genotype'], i))
        i += 1

    # Search the parents for the rest of the genes
    i = crossoverPoint
    while(len(childGeno1) < 8):
        if feature(parents[1]['genotype'], i) not in childGeno1:
            childGeno1.append(feature(parents[1]['genotype'], i))

        i = (i+1) % 8

    i = crossoverPoint
    while(len(childGeno2) < 8):
        if feature(parents[0]['genotype'], i) not in childGeno2:
            childGeno2.append(feature(parents[0]['genotype'], i))

        i = (i+1) % 8

    r.append(individual())
    r.append(individual())
    r[0]['genotype'] = "".join(childGeno1)
    r[1]['genotype'] = "".join(childGeno2)
    r[0]['fitness'] = fitnessfn(r[0]['genotype'])
    r[1]['fitness'] = fitnessfn(r[1]['genotype'])

    return r

def swapMutation (solution):
    mutatedGenotype = genotypeToList(solution['genotype'])
    i = 0
    tgt = 0

    while(i < 8):
        if(random.random() <= mutprob):
            while(tgt == i):
                tgt = random.randint(0,7)

            tgtval = mutatedGenotype[tgt]
            mutatedGenotype[tgt] = mutatedGenotype[i]
            mutatedGenotype[i] = tgtval

        i += 1

    r = individual()
    r['genotype'] = "".join(mutatedGenotype)
    r['fitness'] = fitnessfn(r['genotype'])

    return r

# Exptects an array of children (solutions) from the recombination phase
def mutate (children):
    offspring = []
    while(len(offspring) < len(children)):
        offspring.append(mutationfn(children[len(offspring)]))

    return offspring

def rank2outof5random (pop):
    randoms = []
    while(len(randoms) < 5):
        randoms.append(pop[random.randint(0, len(pop)-1)])

    def ascending (a,b):
        if (a['fitness'] - b['fitness']) < 0:
            return -1
        elif (a['fitness'] - b['fitness']) == 0:
            return 0
        else:
            return 1

    randoms = sorted(randoms, ascending)

    probmap = range(len(randoms))

    i = 0
    while(i < len(probmap)):
        probmap[i] = (i+1.0)/sum(range(1,len(randoms) + 1))
        if i > 0:
            probmap[i] = probmap[i-1] + probmap[i]
        i += 1

    # Selection wheel
    parents = range(2)
    j = 0
    while(j < len(parents)):
        i = 0
        prob = random.random()
        while(i < len(probmap)):
            if i == 0:
                if prob >= 0 and prob < probmap[i]:
                    parents[j] = randoms[i]
            else:
                if prob >= probmap[i-1] and prob < probmap[i]:
                    parents[j] = randoms[i]

            i += 1

        j += 1


    return parents

def replaceWorst (pop, offspring):
    pop.extend(offspring)
    def descending (a,b):
        if (a['fitness'] - b['fitness']) < 0:
            return 1
        elif (a['fitness'] - b['fitness']) == 0:
            return 0
        else:
            return -1
    return sorted(pop, descending)[0:popcap]

def getBestSolution(pop):
    b = None
    for i in pop:
        if b is None or i['fitness'] > b['fitness']:
            b = i
    return b

avglog = []
maxlog = []
def logger (iters, pop):
    avglog.append(avgfitness(pop))
    maxlog.append(maxfitness(pop))

def plotMaxAvgLog ():
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        plt.title('8 Queen\'s problem with Evolutionary Computation.')
        plt.plot(avglog, '-', label='Mean')
        plt.plot(maxlog, '-.', label='Best')
        # plt.plot([(FitCounter.counter - n_species)/2], [mean[-1]], '-o')
        plt.ylabel('Fitnnes')
        plt.xlabel('Interation')
        plt.legend(loc='best', shadow=True)
        plt.savefig(
            'plot-' +
            str(initializationfnid) + '-' +
            str(fitnessfnid) + '-' +
            str(selectionfnid) + '-' +
            str(recombinationfnid) + '-' +
            str(mutationfnid) + '-' +
            str(survivingfnid) + '-' +
            'mit' + str(maxiterations) + '-'
            'mtp' + str(mutprob) + '-'
            'cap' + str(popcap)
        )

    except:
        print 'attection: impossible to plot the grafic, verify if you have matplotlib installed.'

ags = Genetics()
ags.setInitialization(getattr(current_module, initializationfnid))
ags.setStopping(getattr(current_module, stopfnid))
ags.setSelection(getattr(current_module, selectionfnid))
ags.setRecombination(getattr(current_module, recombinationfnid))
ags.setMutation(mutate)
ags.setSurviving(getattr(current_module, survivingfnid))
ags.setPostIteration(logger)
p = ags.run()
plotMaxAvgLog()
best = getBestSolution(p)
print "Max fitness {0} and phenotype {1}".format(best['fitness'], gtp(best['genotype']))
