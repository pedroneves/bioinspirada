import setup as st

def survivorSelection(population, children):
    candidates = children if st.generational else population+children
    return sorted(candidates, reverse=True, key=lambda x: x.fitness)[:st.popcap]