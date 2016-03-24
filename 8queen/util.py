from math import ceil
from random import *

class FitCounter:
    counter = 0

def generatePattern(n, b):
    num = range(n)
    shuffle(num)
    ret = map(toStr, num)
    fullret = add0(ret, b)
    return ''.join([''.join(x) for x in fullret])

def add0(ret, b):
    return [['0']*(b - len(x)) + x for x in ret]

def toStr(n):
    ret = []
    while(n > 0):
        ret.append(str(n % 2))
        n /=2
    return ret[::-1]

def calculateFit(p, n, b):
    FitCounter.counter += 1
    patter = toInt(p, b)
    return 1/(1.0+sum([coliDiaPrincipal(patter, i ,n) + coliDiaSecondaria(patter, i, n) for i in range(n)]))

def tournament(n):
    ret = []
    for i in range(n):
        ret.append(randint(0, n))
    ret.sort(reverse = True)
    return ret

def crossOver(p1, p2, n, b):
    from pattern import Pattern
    cut = randint(1,n-1)
    c1 = p1.code[:cut*b]
    c2 = p2.code[:cut*b]
    for i in range(cut*b, n*b, b):
        c1 += p2.code[i:i+b] if not containsPoss(c1, p2.code[i:i+b], b) else ""
        c2 += p1.code[i:i+b] if not containsPoss(c2, p1.code[i:i+b], b) else ""
    for i in range(0, cut*b, b):
        c1 += p2.code[i:i+b] if not containsPoss(c1, p2.code[i:i+b], b) else ""
        c2 += p1.code[i:i+b] if not containsPoss(c2, p1.code[i:i+b], b) else ""
    c1 = Pattern(n, b, mutate(c1, n, b))
    c2 = Pattern(n, b, mutate(c2, n, b))
    return [c1,c2]

def mutate(p, n, b):
    n1 = randint(0,n-1)*b
    n2 = randint(0,n-1)*b
    r1 = p[n2:n2+b]
    r2 = p[n1:n1+b]
    p = p[:n1] + r1 + p[n1+b:]
    p = p[:n2] + r2 + p[n2+b:]
    return p

def toInt(p, b):
    n = 0
    fac = 1
    ret = []
    q = p[::-1]
    for i in range(len(p)):
        n += fac * int(q[i])
        fac *= 2
        if((i+1) % b == 0):
            ret.append(n)
            n = 0
            fac = 1
    return ret[::-1]
        

def coliDiaPrincipal(p, i, n):
    m = min(i, p[i])
    x = i - m
    y = p[i] - m
    count = 0
    while(x != n and y != n):
        if(p[x] == y):
            count += 1
        x += 1
        y += 1
    return count - 1
    
def coliDiaSecondaria(p, i, n):
    m = min(i, n - p[i])
    x = i - m
    y = p[i] + m  
    count = 0
    while(x != n and y != -1):
        if(p[x] == y):
            count += 1
        x += 1
        y -= 1
    return count - 1

def calculateBits(n):
    b = 0
    while(n > 0):
        n = n/2
        b += 1
    return b
    
def containsPoss(s1, s2, b, stop = -1):
    ret = False
    if(stop == -1 or stop*b > len(s1)):
        stop = (len(s1)+1)/b
    for i in range(stop):
        if(comparePoss(s1, s2, i*b, b)):
            ret = True
            break
    return ret
    
    
def comparePoss(s1, s2, start, b):
    ret = True
    for i in range(b):
        if(s1[i + start] != s2[i]):
            ret = False
            break
    return ret