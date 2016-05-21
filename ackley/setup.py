import numpy as np

# Total amount of individuals
popcap = 60

# Specifies the solution's dimension
dims = 30

# Max mutation pace range for initialization
mutpacerange = 5

# Minimum mutation pace
mutpacemin = 0.1

# Children per iteration to population size ratio
cpc = 7

# Evolution Strategy params
mutationFn = "singleSd"
parentSelectionFn = "globalUniformSelection"
recombinationFn = "hibridRecomb"

# Parameter for recombinations that interpolate the parents. True means the
# child is the average
childAverage = True