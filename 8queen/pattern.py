from util import *

class Pattern:
    
    def __init__(self, n, b, code = ""):
        if(code == ""):
            code = generatePattern(n, b)
        self.code = code
        self.fit = calculateFit(self.code, n, b)
    def __str__(self):
        return str(self.code) + ' - ' + str(self.fit)
        
    def __gt__(self, o):
        return self.fit > o.fit
    