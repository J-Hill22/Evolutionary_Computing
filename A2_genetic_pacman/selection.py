
# selection.py

import random

# For all the functions here, it's strongly recommended to
# review the documentation for Python's random module:
# https://docs.python.org/3/library/random.html

# Parent selection functions---------------------------------------------------
def uniform_random_selection(population, n, **kwargs):
    # TODO: select n individuals uniform randomly
    output = [-1]*n
    population_size = len(population)
    for i in range (n):
        output[i] = population[random.randint(0, population_size - 1)]
    return output
    pass



def k_tournament_with_replacement(population, n, k, **kwargs):
    # TODO: perform n k-tournaments with replacement to select n individuals
    population_size = len(population)
    tourn_size = k
    fitnesses = [individual.fitness for individual in population]
    partis_fits = [-51]*tourn_size
    parents = list()
    for i in range(n):
        participants = random.sample(range(population_size), k=tourn_size)
        for each, j in zip(range(len(participants)), participants):
            partis_fits[each] = fitnesses[j]
        winner_locus = partis_fits.index(max(partis_fits))
        winner = participants[winner_locus]
        parents.append(population[winner])
    return parents

    pass


def fitness_proportionate_selection(population, n, **kwargs):
    # TODO: select n individuals using fitness proportionate selection
    population_size = len(population)
    fitnesses = [individual.fitness for individual in population]
    min_fitness = min(fitnesses)
    max_fitness = max(fitnesses)
    parents = list()
    fit_dist = [0]*population_size
    total_fit = 0
    prob_of_selection = list(range(0, population_size))
    if max_fitness < 0:
        i = 0
        for individual in population:
            curr_dist = (((individual.fitness - min_fitness) + 1) / population_size)
            fit_dist[i] = curr_dist
            i += 1
    elif min_fitness < 0:
        i = 0
        for individual in population:
            curr_dist = (individual.fitness - min_fitness) / population_size
            fit_dist[i] = curr_dist
            i += 1   
    else:
        i = 0
        for individual in population:
            curr_dist = (individual.fitness / population_size)
            fit_dist[i] = curr_dist
            i += 1

    output = random.choices(prob_of_selection, fit_dist,k = n)
    for i in output:
        parents.append(population[i])
    return parents
    pass



# Survival selection functions-------------------------------------------------
def truncation(population, n, **kwargs):
    # TODO: perform truncation selection to select n individuals
    fitnesses = [individual.fitness for individual in population]
    survivors = list()
    
    for i in range(n):
        fittest = max(fitnesses)
        fittest_locus = fitnesses.index(fittest)
        survivors.append(population[fittest_locus])
        fitnesses[fittest_locus] = -99999
    return survivors
    pass


def k_tournament_without_replacement(population, n, k, **kwargs):
    # TODO: perform n k-tournaments without replacement to select n individuals
    # Note: an individual should never be cloned from surviving twice!
    population_size = len(population)
    tourn_size = k
    fitnesses = [individual.fitness for individual in population]
    partis_fits = [-51]*tourn_size
    parents = list()
    pop_no_repl = list(range(population_size))
    
    for i in range(n):
        participants = random.sample(pop_no_repl, k=tourn_size)
        for each, j in zip(range(len(participants)), participants):
            partis_fits[each] = fitnesses[j]
        winner_locus = partis_fits.index(max(partis_fits))
        winner = participants[winner_locus]
        pop_no_repl.remove(winner)
        parents.append(population[winner])
    return parents
    pass



# Yellow deliverable parent selection function---------------------------------
def stochastic_universal_sampling(population, n, **kwargs):
    # Recall that yellow deliverables are required for students in the grad
    # section but bonus for those in the undergrad section.
    # TODO: select n individuals using stochastic universal sampling
    pass