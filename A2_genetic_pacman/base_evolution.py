

# base_evolution.py

import statistics
import random

class BaseEvolutionPopulation():
    def __init__(self, individual_class, mu, num_children,
                 mutation_rate, parent_selection, survival_selection,
                 problem=dict(), parent_selection_kwargs=dict(),
                 recombination_kwargs=dict(), mutation_kwargs=dict(),
                 survival_selection_kwargs=dict(), **kwargs):
        self.mu = mu
        self.num_children = num_children
        self.mutation_rate = mutation_rate
        self.parent_selection = parent_selection
        self.survival_selection = survival_selection
        self.parent_selection_kwargs = parent_selection_kwargs
        self.recombination_kwargs = recombination_kwargs
        self.mutation_kwargs = mutation_kwargs
        self.survival_selection_kwargs = survival_selection_kwargs

        self.log = []
        self.log.append(f'mu: {self.mu}')
        self.log.append(f'num_children: {self.num_children}')
        self.log.append(f'mutation rate: {self.mutation_rate}')
        self.log.append(f'parent selection: {self.parent_selection.__name__ }')
        self.log.append(f'parent selection kwargs: {self.parent_selection_kwargs}')
        self.log.append(f'survival selection: {self.survival_selection.__name__ }')
        self.log.append(f'survival selection kwargs: {self.survival_selection_kwargs}')
        self.log.append(f'recombination kwargs: {self.recombination_kwargs}')
        self.log.append(f'mutation kwargs: {self.mutation_kwargs}')

        self.population = individual_class.initialization(self.mu, **problem, **kwargs)
        self.evaluations = 0

        self.log.append(f'Initial population size: {len(self.population)}')


    def generate_children(self):
        # Randomly select self.num_children * 2 parents using your selection algorithm
        parents = self.parent_selection(self.population, self.num_children * 2, **self.parent_selection_kwargs)
        random.shuffle(parents)
        child_count = self.num_children
        
        children = list()
        mates = list()
        # TODO: Get pairs of parents
        # HINT: range(0, len(parents), 2) to iterate two at a time            
        for p1, p2 in zip(parents, parents[1:]):
            mates.append([p1, p2])
        # the above method ends up 1 short for # parents ((num_children * 2) - 1)
        # to make up for that I manually appened the last parent at the end
        # as last parent = p1 and the first parent = p2, "wrapping" the list
        mates.append([parents[-1], parents[0]])
        


        # TODO: Recombine each pair to generate a child
        # HINT: With parents p1 and p2, get a child with
        #       p1.recombine(p2, **self.recombination_kwargs)
        for i in range(self.num_children):
            parent_1 = mates[i][0]
            parent_2 = mates[i][1]
            #print(parent_1, parent_2)
            child = parent_1.recombine(parent_2, **self.recombination_kwargs)
            children.append(child)


        # TODO: Mutate each child independently with probability self.mutation_rate.
        #       The probability is independent for each child, meaning you should
        #       randomly decide if each individual child gets mutated. That is,
        #       you shouldn't calculate a precise number of mutations to occur ahead of time.
        #       Record the number of mutated children in mutated_child_count variable.
        # HINT: With a recombined child, get a mutated copy with
        #       child.mutate(**self.mutation_kwargs)
        #       Keep in mind this does not modify child, it returns a new object
        mutated_child_count = 0
        mutation_prob = self.mutation_rate
        for i in range(child_count):
            rand_prob = random.random()
            if rand_prob < mutation_prob:
                mutated_child = children[i].mutate(**self.mutation_kwargs)
                children[i] = mutated_child
                mutated_child_count += 1


        self.log.append(f'Number of children: {len(children)}')
        self.log.append(f'Number of mutations: {mutated_child_count}')

        return children


    def survival(self):
        self.log.append(f'Pre-survival population size: {len(self.population)}')
        self.population = self.survival_selection(self.population, self.mu, **self.survival_selection_kwargs)
        self.log.append(f'Post-survival population size: {len(self.population)}')
