
# linear_genotype.py

import random
from copy import deepcopy

class LinearGenotype():
    def __init__(self):
        self.fitness = None
        self.genes = None

    def random_initialization(self, shapes, bounds, **kwargs):
        # TODO: Initialize self.genes, using the input parameters.
        #       It should be an indexable data structure of length len(shapes),
        #       where each element is an indexable data structure of length 3.
        #       The first value of each element should be an integer within the
        #       half-open interval [bounds[0][0], bounds[0][1]). The second should be
        #       similar, within [bounds[1][0], bounds[1][1]). The third should be
        #       either 0, 1, 2, or 3. All values should be chosen uniform randomly.
        shapes_length = len(shapes)
        self.genes = [
            [
                random.randint(bounds[0][0], (bounds[0][1] - 1)),
                random.randint(bounds[1][0], (bounds[1][1] - 1)),
                random.randint(0,3)
            ]
            for i in range (shapes_length)
        ]
        pass


    def recombine(self, mate, method, **kwargs):
        child = LinearGenotype()
        child = deepcopy(self)
        gene_count = len(self.genes)
        # TODO: Recombine genes of self with mate and assign to child's genes member variable
        assert method.casefold() in {'uniform', 'one-point', 'bonus'}
        if method.casefold() == 'uniform':
            # Perform uniform recombination
            for i in range(len(self.genes)):
                if random.choice([0,1]) == 1:
                    child.genes[i] = deepcopy(self.genes[i])
                else: 
                    child.genes[i] = deepcopy(mate.genes[i])
                    pass
            #child.genes = deepcopy(self.genes)
            return child

        elif method.casefold() == 'one-point':
            # Perform one-point crossover
            co_point = random.randint(1, gene_count - 1)
            for i in range(co_point, (len(self.genes))):
                child.genes[i] = deepcopy(mate.genes[i])
            return child
            pass

        elif method.casefold() == 'bonus':
            '''
            This is a red deliverable (i.e., bonus for anyone).

            Implement the bonus crossover operator as described in deliverable
            Red 1 of Assignment 1b.
            '''
            pass

        return child


    def mutate(self, bounds, bonus=None, **kwargs):
        mutant = LinearGenotype()
        mutant.genes = deepcopy(self.genes)

        if not bonus:
            # TODO: Mutate genes of mutant
            for i in range(len(mutant.genes)):
                choose_allele = random.randrange(1,4)
                match str(choose_allele):
                    case '1':
                        mutate_by = random.randrange(0, 50)
                        mutated_allele = (mutant.genes[i][0] + mutate_by) % 50
                        mutant.genes[i][0] = mutated_allele
                    case '2':
                        mutate_by = random.randrange(0, 15)
                        mutated_allele = (mutant.genes[i][1] + mutate_by) % 15
                        mutant.genes[i][0] = mutated_allele
                    case '3':
                        mutate_by = random.randrange(0, 4)
                        mutated_allele = (mutant.genes[i][2] + mutate_by) % 4
                        mutant.genes[i][0] = mutated_allele

        else:
            '''
            This is a red deliverable (i.e., bonus for anyone).

            Implement the bonus crossover operator as described in deliverable
            Red 1 of Assignment 1b.
            '''
            pass

        return mutant


    @classmethod
    def initialization(cls, mu, *args, **kwargs):
        population = [cls() for _ in range(mu)]
        for i in range(len(population)):
            population[i].random_initialization(*args, **kwargs)
        return population