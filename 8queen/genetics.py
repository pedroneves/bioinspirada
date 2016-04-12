class Genetics:

    def __init__(self):
        self.population = None
        self.iterations = 0
        self.initialization = None
        self.preIteration = None
        self.postIteration = None
        self.stopping = None
        self.selection = None
        self.recombination = None
        self.mutation = None
        self.surviving = None

    def run(self):
        if self.initialization is None:
            return 'initialization function is empty'
        if self.stopping is None:
            return 'stopping function is empty'
        if self.selection is None:
            return 'selection function is empty'
        if self.recombination is None:
            return 'recombination function is empty'
        if self.mutation is None:
            return 'mutation function is empty'
        if self.surviving is None:
            return 'surviving function is empty'

        self.population = self.initialization();

        while not self.stopping(self.iterations, self.population):

            if self.preIteration is not None:
                self.preIteration(self.iterations, self.population)

            self.population = self.surviving(self.mutation(self.recombination(self.selection(self.population))))

            if self.postIteration is not None:
                self.postIteration(self.iterations, self.population)

            self.iterations += 1

        print('Evolution terminated after {0} iterations'.format(self.iterations))

        return self.population

    def setInitialization (self, initfn):
        if hasattr(initfn, '__call__'):
            self.initialization = initfn


    def setPreIteration (self, preiterfn):
        if hasattr(preiterfn, '__call__'):
            self.preIteration = preiterfn

    def setPostIteration (self, postiterfn):
        if hasattr(postiterfn, '__call__'):
            self.postIteration = postiterfn

    def setStopping (self, stoppingfn):
        if hasattr(stoppingfn, '__call__'):
            self.stopping = stoppingfn

    def setSelection (self, selectionfn):
        if hasattr(selectionfn, '__call__'):
            self.selection = selectionfn

    def setRecombination (self, recombinationfn):
        if hasattr(recombinationfn, '__call__'):
            self.recombination = recombinationfn

    def setMutation (self, mutationfn):
        if hasattr(mutationfn, '__call__'):
            self.mutation = mutationfn

    def setSurviving (self, survivingfn):
        if hasattr(survivingfn, '__call__'):
            self.surviving = survivingfn
