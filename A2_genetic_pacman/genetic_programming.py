
# genetic_programming.py

from base_evolution import BaseEvolutionPopulation
import random

class GeneticProgrammingPopulation(BaseEvolutionPopulation):
    def generate_children(self):
        children = list()
        recombined_child_count = 0
        mutated_child_count = 0

        # 2b TODO: Generate self.num_children children by either:
        #          recombining two parents OR
        #          generating a mutated copy of a single parent.
        #          Use self.mutation_rate to decide how each child should be made.
        #          Use your Assignment Series 1 generate_children function as a reference.
        #          Count the number of recombined/mutated children in the provided variables.
        for _ in range(self.num_children):
            if random.random() < self.mutation_rate:
                parent = self.parent_selection(self.population, 1, **self.parent_selection_kwargs)[0]
                children.append(parent.mutate(**self.mutation_kwargs))
                mutated_child_count += 1
            else:                                           
                parent, mate = self.parent_selection(self.population, 2, **self.parent_selection_kwargs)
                children.append(parent.recombine(mate, **self.recombination_kwargs))
                recombined_child_count += 1


        self.log.append(f'Number of children: {len(children)}')
        self.log.append(f'Number of recombinations: {recombined_child_count}')
        self.log.append(f'Number of mutations: {mutated_child_count}')

        return children
