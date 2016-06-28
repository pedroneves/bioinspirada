import setup as sp
import os

LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), sp.LOG_DIR_NAME)

def checkLogDir ():
    if not os.path.exists(LOG_DIR):
        os.mkdir(LOG_DIR)

def mean (pop):
    ssum = 0
    csum = 0
    i = 0
    while i < len(pop):
        ssum += pop[i].fitness['score']
        csum += pop[i].fitness['clock']
        i += 1
    return {
        'score': (ssum / len(pop)),
        'clock': (csum / len(pop))
    }

class Log:
    def __init__(self, name):
        self.data = list()
        self.name = name
        self.path = os.path.join(LOG_DIR, name)

    def push (self, itnum, pop):
        entry = {
            'iteration': itnum,
            'max': {
                'score': pop[0].fitness['score'],
                'clock': pop[0].fitness['clock']
            },
            'mean': mean(pop)
        }
        self.data.append(entry)

    def save(self):
        checkLogDir()
        
        f = open(self.path, 'a')
        s = ''
        i = 0

        while i < len(self.data):
            s += '{0},{1},{2},{3},{4},\n'.format(
                self.data[i]['iteration'],
                self.data[i]['max']['score'],
                self.data[i]['max']['clock'],
                self.data[i]['mean']['score'],
                self.data[i]['mean']['clock'])
            i += 1

        f.write(s)
        f.close()
