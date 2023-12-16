
# stock_population_evaluation.py

from cutting_stock.fitness_functions import *

# 1b TODO: Evaluate the population and assign the fitness and visualize
# member variables as described in the Assignment 1b notebook
def base_population_evaluation(population, **kwargs):
    # Use base_fitness_function, i.e.,
    # base_fitness_function(individual.genes, **kwargs)
    for individual in population:
        temp = base_fitness_function(individual.genes, **kwargs)
        individual.fitness = temp['fitness']
        individual.visualize = temp['visualize']
        
    pass


# 1c TODO: Evaluate the population and assign the base_fitness, violations, fitness, and visualize
# member variables as described in the constraint satisfaction portion of Assignment 1c
def unconstrained_population_evaluation(population, penalty_coefficient, red=None, **kwargs):
    # Use unconstrained_fitness_function, i.e.,
    # unconstrained_fitness_function(individual.genes, **kwargs)
    if not red:
        # GREEN deliverable logic goes here
        for individual in population:
            temp = unconstrained_fitness_function(individual.genes, **kwargs)
            individual.base_fitness = temp['base fitness']
            individual.unconstrained_fitness = temp['unconstrained fitness']
            individual.violations = temp['violations']
            individual.fitness = individual.unconstrained_fitness - individual.violations * penalty_coefficient
            individual.visualize = temp['visualize']
        pass

    else:
        # RED deliverable logic goes here
        pass


# 1d TODO: Evaluate the population and assign the objectives and visualize
# member variables as described in the multi-objective portion of Assignment 1d
def multiobjective_population_evaluation(population, yellow=None, **kwargs):
    # Use multiobjective_fitness_function, i.e.,
    # multiobjective_fitness_function(individual.genes, **kwargs)
    if not yellow:
        # GREEN deliverable logic goes here
        for individual in population:
            temp = multiobjective_fitness_function(individual.genes, **kwargs)
            individual.objectives = [temp['length'], temp['width']]
            individual.visualize = temp['visualize']
            
        pass

    else:
        # YELLOW deliverable logic goes here
        pass

