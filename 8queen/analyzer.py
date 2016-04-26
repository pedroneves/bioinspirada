#
#
# This script is responsable to analyze all the test logs and give a comparative
# view of the average iteration and the standard deviation for each test.
#
#

import os
import json

plotNamePrefix = "analysis-"
logDirPrefix = "log-"
logFileSufix = ".json"

def getLogDirs ():
    def isLogDir (d):
        return d.startswith(logDirPrefix)

    return filter(isLogDir, next(os.walk("."))[1])

def getLogFiles (logDirectory):
    def isLogFile (f):
        return f.endswith(logFileSufix)

    # get all the files in the give dir and checks if it a log JSON file
    return filter(isLogFile, next(os.walk(os.path.join(".", logDirectory)))[2])

def getLogIterations (logDirectory):

    files = getLogFiles(logDirectory)

    # iterate over all files, open and extract the total of iterations
    i = 0
    iterations = []
    while i < len(files):
        with open(os.path.join(logDirectory, files[i])) as json_file:
            iterations.append(json.load(json_file)['iterations'])
        i+=1

    return iterations

def avgLogIterations (l):
    return sum(l)/len(l)

def sdLogIterations (l):
    try:
        import numpy as np
        return np.std(l)
    except Exception, e:
        print 'sdLogIterations is kaput: '+ str(e)


testDirs = getLogDirs()
testLogs = map(getLogIterations, testDirs)
testAvgs = map(avgLogIterations, testLogs)
testStds = map(sdLogIterations, testLogs)

print 'Iteration analysis'
i = 0
while i < len(testDirs):
    print '\n{0}\n\tavg: {1}\n\tsd: {2}'.format(" ".join(testDirs[i].split("-")[1:]), testAvgs[i], testStds[i])
    i+=1
