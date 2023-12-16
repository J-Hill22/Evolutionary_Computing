from math import inf
import math
import numpy as np


'''
1d TODO: Return True if A dominates B based on the objective member variables of both objects.
If attempting the YELLOW deliverable, your code must be able to gracefully handle
any number of objectives, i.e., don't hardcode an assumption that there are 2 objectives.
'''
def dominates(A, B):
    # HINT: We strongly recommend use of the built-in functions any() and all()
    not_worse = all(a >= b for a, b in zip(A.objectives, B.objectives))
    better = any(a > b for a, b in zip(A.objectives, B.objectives))
    return not_worse and better


'''
1d TODO: Use the dominates function (above) to sort the input population into levels
of non-domination, and assign to the level members based on an individual's level.
'''
def nondomination_sort(population):
    dominated_count = [0] * len(population)
    dominates_list = [[] for _ in range(len(population))]

    # Populate dominated count and dominates list
    for i in range(len(population)):
        for j in range(len(population)):
            if i == j:
                continue
            if dominates(population[i], population[j]):
                dominated_count[j] += 1
                dominates_list[i].append(j)

    # Identify the first front
    fronts = [[]]
    for i, count in enumerate(dominated_count):
        if count == 0:
            population[i].level = 1  # Assign level 1
            fronts[0].append(i)
            dominated_count[i] = -1  # Mark as processed

    # Build subsequent fronts
    current_level = 1
    while fronts[current_level - 1]:
        next_front = []
        for i in fronts[current_level - 1]:
            for j in dominates_list[i]:
                dominated_count[j] -= 1
                if dominated_count[j] == 0:
                    population[j].level = current_level + 1  # Assign the next level
                    next_front.append(j)
                    dominated_count[j] = -1  # Mark as processed
        current_level += 1
        fronts.append(next_front)
    pass


'''
1d TODO: Calculate the improved crowding distance from https://ieeexplore.ieee.org/document/996017
For each individual in the population, and assign this value to the crowding member variable.
Use the inf constant (imported at the top of this file) to represent infinity where appropriate.
'''
def assign_crowding_distances(population):
    # Don't forget to check for division by zero! Replace any divisions by zero with the inf constant.        
    l = len(population)
    m = len(population[0].objectives)
    distance = [0 for _ in range(l)]
    
    # Group individuals by their level
    level_indices = {}
    for i, ind in enumerate(population):
        if ind.level not in level_indices:
            level_indices[ind.level] = []
        level_indices[ind.level].append(i)
        
    # Assign infinite distance to individuals who are the only members of their front
    for indices in level_indices.values():
        if len(indices) == 1:
            distance[indices[0]] = inf
        else:
            for obj_ind in range(m):
                sorted_by_obj = sorted(indices, key=lambda x: population[x].objectives[obj_ind])
                obj_range = population[sorted_by_obj[-1]].objectives[obj_ind] - population[sorted_by_obj[0]].objectives[obj_ind]
                
                distance[sorted_by_obj[0]] = inf  # First in sorted list
                distance[sorted_by_obj[-1]] = inf  # Last in sorted list
                
                for i in range(1, len(sorted_by_obj) - 1):
                    if obj_range == 0:
                        distance[sorted_by_obj[i]] += inf
                    else:
                        distance[sorted_by_obj[i]] += (population[sorted_by_obj[i + 1]].objectives[obj_ind] - population[sorted_by_obj[i - 1]].objectives[obj_ind]) / obj_range
            
    for i, individual in enumerate(population):
        individual.crowding = distance[i]
    pass


# This function is implemented for you. You should not modify it.
# It uses the above functions to assign fitnesses to the population.
def assign_fitnesses(population, crowding=False, **kwargs):
    # Assign levels of nondomination.
    nondomination_sort(population)

    # Assign fitnesses.
    max_level = max(map(lambda x:x.level, population))
    for individual in population:
        individual.fitness = max_level + 1 - individual.level

    # Check if we should apply crowding penalties.
    if not crowding:
        for individual in population:
            individual.crowding = 0

    # Apply crowding penalties.
    else:
        assign_crowding_distances(population)
        for individual in population:
            if individual.crowding != inf:
                assert 0 <= individual.crowding <= len(individual.objectives),\
                    f'A crowding distance ({individual.crowding}) was not in the correct range. ' +\
                    'Make sure you are calculating them correctly in assign_crowding_distances.'
                individual.fitness -= 1 - 0.999 * (individual.crowding / len(individual.objectives))


'''
The remainder of this file is code used to calculate hypervolumes.
You do not need to read, modify or understand anything below this point.
Implementation based on https://ieeexplore.ieee.org/document/5766730
'''
def calculate_hypervolume(front, reference_point=None):
    point_set = [individual.objectives for individual in front]
    if reference_point is None:
        # Defaults to (-1)^n, which assumes the minimal possible scores are 0.
        reference_point = [-1] * len(point_set[0])
    return wfg_hypervolume(list(point_set), reference_point, True)


def wfg_hypervolume(pl, reference_point, preprocess=False):
    if preprocess:
        pl_set = {tuple(p) for p in pl}
        pl = list(pl_set)
        if len(pl[0]) >= 4:
            pl.sort(key=lambda x: x[0])

    if len(pl) == 0:
        return 0
    return sum([wfg_exclusive_hypervolume(pl, k, reference_point) for k in range(len(pl))])


def wfg_exclusive_hypervolume(pl, k, reference_point):
    return wfg_inclusive_hypervolume(pl[k], reference_point) - wfg_hypervolume(limit_set(pl, k), reference_point)


def wfg_inclusive_hypervolume(p, reference_point):
    return math.prod([abs(p[j] - reference_point[j]) for j in range(len(p))])


def limit_set(pl, k):
    ql = []
    for i in range(1, len(pl) - k):
        ql.append([min(pl[k][j], pl[k+i][j]) for j in range(len(pl[0]))])
    result = set()
    for i in range(len(ql)):
        interior = False
        for j in range(len(ql)):
            if i != j:
                if all(ql[j][d] >= ql[i][d] for d in range(len(ql[i]))) and any(ql[j][d] > ql[i][d] for d in range(len(ql[i]))):
                    interior = True
                    break
        if not interior:
            result.add(tuple(ql[i]))
    return list(result)

