import random
from copy import copy
from genetics import Genetics
import sys
import os
import json

current_module = sys.modules[__name__]

testAmount = 10
avglog = []
maxlog = []
savingJson = True
isPlotting = True
run = True

# AGS params
maxiterations = 10000
mutprob = 0.8
popcap = 100
initializationfnid = 'randominit'
fitnessfnid = 'collisionFitness'
selectionfnid = 'tournament'
recombinationfnid = 'pmx'
mutationfnid = 'swapMutation'
survivingfnid = 'replaceWorst'
stopfnid = 'stop'
# tournament parameters
nSelected = 5
nParents = 2

###############################
# AUX
###############################

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

def getBestSolution(pop):
    b = None
    for i in pop:
        if b is None or i['fitness'] > b['fitness']:
            b = i
    return b

def logger (iters, pop):
    avglog.append(avgfitness(pop))
    maxlog.append(maxfitness(pop))

def jsonMaxAvgLog (avglog, maxlog):
    data = {}
    data['iterations'] = len(avglog)
    data['avglog'] = avglog
    data['maxlog'] = maxlog

    # Creates a dir to contain the ploting graphs for the current configuration
    plotDir = 'plot-' + str(initializationfnid) + '-' + str(fitnessfnid) + '-' + str(selectionfnid) + '-' + str(recombinationfnid) + '-' + str(mutationfnid) + '-' + str(survivingfnid) + '-' + 'mit' + str(maxiterations) + '-' + 'mtp' + str(mutprob) + '-' + 'cap' + str(popcap)
    if not os.path.exists(plotDir):
        os.makedirs(plotDir)

    # Checks the plotting order
    order = 1
    plotDirFiles = [int(f.split(".")[0]) for f in os.listdir(plotDir) if (os.path.isfile(os.path.join(plotDir, f)) and f.split(".")[1] == "json")]
    order = 1 + (max(plotDirFiles) if len(plotDirFiles) > 0 else 0)

    with open(os.path.join(plotDir, str(order) + '.json'), 'w') as outfile:
        json.dump(data, outfile)

def plotMaxAvgLog (avglog, maxlog):

    # Creates a dir to contain the ploting graphs for the current configuration
    plotDir = 'plot-' + str(initializationfnid) + '-' + str(fitnessfnid) + '-' + str(selectionfnid) + '-' + str(recombinationfnid) + '-' + str(mutationfnid) + '-' + str(survivingfnid) + '-' + 'mit' + str(maxiterations) + '-' + 'mtp' + str(mutprob) + '-' + 'cap' + str(popcap)
    if not os.path.exists(plotDir):
        os.makedirs(plotDir)

    # Checks the plotting order
    order = 1
    plotDirFiles = [int(f.split(".")[0]) for f in os.listdir(plotDir) if (os.path.isfile(os.path.join(plotDir, f)) and f.split(".")[1] == "png")]
    order = 1 + (max(plotDirFiles) if len(plotDirFiles) > 0 else 0)

    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt

        # Plotting
        plt.title('8 Queen\'s problem with Evolutionary Computation.')
        plt.plot(avglog, '-', label='Avg')
        plt.plot(maxlog, '-.', label='Max')
        plt.ylabel('Fitness')
        plt.xlabel('Iterations')
        plt.legend(loc='best', shadow=True)
        plt.savefig( os.path.join(plotDir, str(order) + '.png' ))
        plt.clf()

    except Exception, e:
        print 'attection: impossible to plot the grafic, verify if you have matplotlib installed.'
        print 'What went wrong: '+ str(e)

# Find the elements selected by a roulette. SortedPop is the decreasingly sorted population,
# pointers is a list of roulette results, between 0 and the fitness sum of the population.
def findRouletterPointers (sortedPop, pointers):
    ret = list()

    for pointer in pointers:
        cumFitness = 0
        position = 0
        while cumFitness + sortedPop[position]['fitness'] < pointer:
            cumFitness += sortedPop[position]['fitness']
            position += 1
        ret.append(sortedPop[position])

    return ret

def pmxGenerateChild (p1, p2, idx1, idx2):
    child = dict()

    def findPosition(phenotype, elem):
        pos = 0
        for e in phenotype:
            if e == elem:
                return pos
            pos += 1
        return -1

    for i in range(idx1, idx2+1):
        child[i] = p1[i]

    for i_ in range(idx1, idx2+1):
        i = i_
        elem = p2[i_]
        if not (elem in child.values()):
            while i in child.keys():
                j = child[i]
                i = findPosition(p2, j)
            child[i] = elem

    # Fill the remaining slots of the child and return it as a list
    ret = copy(p2)
    for i in child:
        ret[i] = child[i]
    return ret


###############################
# FITNESS
###############################

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



###############################
# INITIALIZATION
###############################

def randominit ():
    i = 0
    pop = []
    while i < popcap:
        pop.append(individual())
        i += 1
    return pop



###############################
# RECOMBINATIONS
###############################

def pmx (parents):
    p1 = gtp(parents[0]['genotype'])
    p2 = gtp(parents[1]['genotype'])

    # Generate two distinct indices
    positions = set()
    while len(positions) < 2:
        positions.add(random.randint(0, len(p1)-1))
    idx1 = min(positions)
    idx2 = max(positions)

    child1Phenotype = pmxGenerateChild(p1, p2, idx1, idx2)
    child2Phenotype = pmxGenerateChild(p2, p1, idx1, idx2)

    child1 = dict()
    child1['genotype'] = ptg(child1Phenotype)
    child1['fitness'] = fitnessfn(child1['genotype'])

    child2 = dict()
    child2['genotype'] = ptg(child2Phenotype)
    child2['fitness'] = fitnessfn(child2['genotype'])

    return [child1, child2]

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

def simpleCrossover (parents):
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

    i = i*3
    while(i < 24):
        childGeno1.append(parents[1]['genotype'][i])
        childGeno2.append(parents[0]['genotype'][i])
        i += 1

    r.append(individual())
    r.append(individual())
    r[0]['genotype'] = "".join(childGeno1)
    r[1]['genotype'] = "".join(childGeno2)
    r[0]['fitness'] = fitnessfn(r[0]['genotype'])
    r[1]['fitness'] = fitnessfn(r[1]['genotype'])

    return r

###############################
# MUTATIONS
###############################

def reversionMutation (solution):
    phenotype = gtp(solution['genotype'])

    # No mutation occurs
    if random.random() > mutprob:
        return solution

    # Generate two distinct indices
    positions = set()
    while len(positions) < 2:
        positions.add(random.randint(0, len(phenotype)-1))
    idx1 = min(positions)
    idx2 = max(positions)

    newPhenotype = list()
    newPhenotype.extend(phenotype[:idx1])
    middle = phenotype[idx1:idx2+1]
    middle.reverse()
    newPhenotype.extend(middle)
    newPhenotype.extend(phenotype[idx2+1:])

    # Compute the new genotype and fitness
    genotype = ptg(newPhenotype)
    fitness = fitnessfn(genotype)
    # Update values and return
    solution['genotype'] = genotype
    solution['fitness'] = fitness
    return solution

def insertionMutation (solution):
    phenotype = gtp(solution['genotype'])

    # No mutation occurs
    if random.random() > mutprob:
        return solution

    # Generate two distinct indices
    positions = set()
    while len(positions) < 2:
        newPosition = random.randint(0, len(phenotype)-1)
        if not (newPosition-1 in positions):
            positions.add(newPosition)
    idx1 = min(positions)
    idx2 = max(positions)

    temp = phenotype[idx2]
    phenotype.pop(idx2)
    phenotype.insert(idx1+1, temp)

    # Compute the new genotype and fitness
    genotype = ptg(phenotype)
    fitness = fitnessfn(genotype)
    # Update values and return
    solution['genotype'] = genotype
    solution['fitness'] = fitness
    return solution

def swapMutation (solution):
    mutatedGenotype = genotypeToList(solution['genotype'])

    if random.random() <= mutprob:
        tgt1 = random.randint(0,7)
        tgt2 = random.randint(0,7)

        while(tgt1 == tgt2):
            tgt2 = random.randint(0,7)

        aux = mutatedGenotype[tgt2]
        mutatedGenotype[tgt2] = mutatedGenotype[tgt1]
        mutatedGenotype[tgt1] = aux

    r = individual()
    r['genotype'] = "".join(mutatedGenotype)
    r['fitness'] = fitnessfn(r['genotype'])

    return r

# Classic Genetic Algorithm mutation, with independent mutations occuring at each bit
def simpleMutation (solution):
    i = 0
    mutatedGenotype = range(len(solution['genotype']))
    while (i < len(solution['genotype'])):
        if(random.random() < mutprob):
            mutatedGenotype[i] = str((int(solution['genotype'][i]) + 1) % 2)
        else:
            mutatedGenotype[i] = solution['genotype'][i]
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



###############################
# SELECTIONS
###############################

# Classic roulette wheel method for selecting parents
def roulette (pop):
    sortedPop = sorted(pop, reverse = True, key = lambda x: x['fitness'])
    fitnessSum = sum([x['fitness'] for x in sortedPop])

    roulettePointers = list();
    roulettePointers.append(random.uniform(0, fitnessSum))
    roulettePointers.append(random.uniform(0, fitnessSum))

    return findRouletterPointers(sortedPop, roulettePointers)

# Baker's Stochastic Universal Sampling roulette algorithm
def rouletteSUS (pop):
    sortedPop = sorted(pop, reverse = True, key = lambda x: x['fitness'])
    fitnessSum = sum([x['fitness'] for x in sortedPop])

    pointerDistance = fitnessSum/float(nParents)
    pointer = random.uniform(0, pointerDistance)
    roulettePointers = list()
    while len(roulettePointers) < nParents:
        roulettePointers.append(pointer)
        pointer += pointerDistance

    return findRouletterPointers(sortedPop, roulettePointers)

# Classic tournament method for selecting parents
def tournament (pop):
    # Select nSelected random indices corresponding to members of the population pop
    randIndices = list()
    while(len(randIndices) < nSelected):
        newRandIndex = random.randint(0, len(pop)-1)
        if not (newRandIndex in randIndices):
            randIndices.append(newRandIndex)

    # Get the appropriate members
    selectedMembers = map(lambda idx: pop[idx], randIndices)
    # Sort the selected members by fitness
    selectedMembers.sort(reverse = True, key = lambda x: x['fitness']);
    # Return nParents elements with the highest fitness
    return selectedMembers[:nParents]

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



###############################
# SURVIVORS
###############################

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


###############################
# RUN
###############################
if run:
    print "Running..."
    ags = Genetics()

    test = 0
    while(test < testAmount):
        avglog = []
        maxlog = []

        ags.setInitialization(getattr(current_module, initializationfnid))
        ags.setStopping(getattr(current_module, stopfnid))
        ags.setSelection(getattr(current_module, selectionfnid))
        ags.setRecombination(getattr(current_module, recombinationfnid))
        ags.setMutation(mutate)
        ags.setSurviving(getattr(current_module, survivingfnid))
        ags.setPostIteration(logger)
        superiorRace = ags.run()

        if isPlotting:
            print "Plotting..."
            plotMaxAvgLog(avglog, maxlog)

        if savingJson:
            jsonMaxAvgLog(avglog, maxlog)

        best = getBestSolution(superiorRace)
        print "Test #{2}: Max fitness {0} and phenotype {1}".format(best['fitness'], gtp(best['genotype']), (test+1))
        test += 1
