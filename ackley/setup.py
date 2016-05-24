import numpy as np

# Total amount of individuals
popcap = 30

# Specifies the solution's dimension
dims = 30

# Max mutation pace range for initialization
mutpacerange = 5

# Minimum mutation pace
mutpacemin = 0.1

# Desired ammount of children generated per iteration is childrenRatio * popcap
childrenRatio = 7

# Evolution Strategy params
mutationFn = "singleSd"
parentSelectionFn = "globalUniformSelection"
recombinationFn = "hibridRecomb"

# Parameter for recombinations that interpolate the parents. True means the
# child is the average
childAverage = True

# Specification of which survival selection approach to follow: generational or
# non-generational
generational = True