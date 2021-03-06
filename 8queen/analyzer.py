#
#
# This script is responsable for analyzing all the test logs and giving a comparative
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

def mean (logs):
    return (sum(logs) + 0.0)/len(logs)

def sd (logs):
    try:
        import numpy as np
        return np.std(logs)
    except Exception, e:
        print 'sd is kaput: '+ str(e)

def getLogData (logDirectory):
    # Get the files on the given logDirectory
    files = getLogFiles(logDirectory)

    # iterate over all files, open and extract the data
    i = 0
    log = {
        'strategy': logDirectory, # labeling
        'iterations': [], # all the iterations for each test
        'avgs': [], # all the average fitness of all tests
        'maxs': [], # all the maximun fitness of all tests
        'tests': 0, # total of tests for the strategy specified for by the logDirectory
        'converged': 0, # number of converged tests
        'statistics': {
            'convergence': 0,
            'iterations': {
                'avg': 0,
                'sd': 0
            },
            'avgfitness': {
                'avg': 0,
                'sd': 0
            },
            'maxfitness': {
                'avg': 0,
                'sd': 0
            }
        }
    }
    while i < len(files):
        log['tests'] += 1

        with open(os.path.join(logDirectory, files[i])) as json_file:
            j = json.load(json_file)

            if(j['converged']):
                log['converged'] += 1
                log['iterations'].append(j['iterations'])
                log['avgs'].extend(j['avglog'])
                log['maxs'].extend(j['maxlog'])
        i+=1

    # calculate the statistics
    log['statistics']['convergence'] = (log['converged']*100.0)/log['tests']

    log['statistics']['iterations']['avg'] = mean(log['iterations'])
    log['statistics']['iterations']['sd'] = sd(log['iterations'])

    log['statistics']['avgfitness']['avg'] = mean(log['avgs'])
    log['statistics']['avgfitness']['sd'] = sd(log['avgs'])

    log['statistics']['maxfitness']['avg'] = mean(log['maxs'])
    log['statistics']['maxfitness']['sd'] = sd(log['maxs'])

    return log



testDirs = getLogDirs()
testLogs = map(getLogData, testDirs)

print 'Analysis'
with open('analysis.csv', 'w') as csvfile:
    csvfile.write('{0};{1};{2};{3};{4};{5};{6};{7};{8}\n'.format(
        'strategy',
        'order',
        'convergence',
        'iterations-avg',
        'iterations-sd',
        'avgfitness-avg',
        'avgfitness-sd',
        'maxfitness-avg',
        'maxfitness-sd'
    ))

    i = 0
    while(i < len(testLogs)):
        csvfile.write('{0};{1};{2};{3};{4};{5};{6};{7};{8};\n'.format(
            testLogs[i]['strategy'],
            str((i+1)),
            testLogs[i]['statistics']['convergence'],
            testLogs[i]['statistics']['iterations']['avg'],
            testLogs[i]['statistics']['iterations']['sd'],
            testLogs[i]['statistics']['avgfitness']['avg'],
            testLogs[i]['statistics']['avgfitness']['sd'],
            testLogs[i]['statistics']['maxfitness']['avg'],
            testLogs[i]['statistics']['maxfitness']['sd']
        ))
        print 'Test {0}\n\tConvergence: {1}\n\tIterations\n\t  avg: {2}\n\t  sd: {3}\n\tAvgFitness\n\t  avg: {4}\n\t  sd: {5}\n\tMaxFitness\n\t  avg: {6}\n\t  sd: {7}'.format(
            testLogs[i]['strategy'],
            testLogs[i]['statistics']['convergence'],
            testLogs[i]['statistics']['iterations']['avg'],
            testLogs[i]['statistics']['iterations']['sd'],
            testLogs[i]['statistics']['avgfitness']['avg'],
            testLogs[i]['statistics']['avgfitness']['sd'],
            testLogs[i]['statistics']['maxfitness']['avg'],
            testLogs[i]['statistics']['maxfitness']['sd']
        )
        i += 1
