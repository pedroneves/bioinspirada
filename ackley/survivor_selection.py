import setup as st

def survivorSelection(population, children):
    def bestFromPop():
        return sorted(population, reverse=True, key=lambda x: x.fitness)[:int(round(0.1*len(population)))]

    candidates = list()
    if st.generational:
        candidates = children+bestFromPop() if st.generationalElitist else children
    else:
        candidates = population+children

    return sorted(candidates, reverse=True, key=lambda x: x.fitness)[:st.popcap]