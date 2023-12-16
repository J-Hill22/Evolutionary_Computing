
# tree_genotype.py

import random
from copy import deepcopy
from fitness import manhattan

class TreeNode:
    def __init__(self, left=None, right=None):
        self.left = left
        self.right = right
        
        
class TerminalNode(TreeNode):
    def __init__(self, left=None, right=None):
        super().__init__(left, right)
    def print(self, depth):
        return f"\n{'|' * depth}{self.value}"
    
class GNode(TerminalNode):
    value = "G"
    
    def __init__(self, is_ghost=False):
        super().__init__()
        self.is_ghost = is_ghost
        
    def score(self, state: dict, ghost_id=None):
        if self.is_ghost:
            # As a ghost, find nearest other ghost
            player_pos = state['players'][ghost_id]
            other_ghosts = list(key for key in state['players'] if 'm' not in key and key != ghost_id)
            temp =  min(manhattan(player_pos, state['players'][ghost_pos]) for ghost_pos in other_ghosts)
            return temp
        else:
            # As Pac-Man, find distance to nearest ghost
            ghosts = list(key for key in state['players'] if 'm' not in key)
            return min(manhattan(state['players']['m'], state['players'][ghost]) for ghost in ghosts)
    
class MNode(TerminalNode):
    value = "M"
    
    def __init__(self, is_ghost=False):
        super().__init__()
        self.is_ghost = is_ghost
    
    def score(self, state: dict, ghost_id=None):
        ghost_key = ghost_id
        #print(ghost_id)
        ghost_pos = state['players'][ghost_key]
        pac_pos = state['players']['m']
        return manhattan(ghost_pos, pac_pos)

    
    
class PNode(TerminalNode):
    value = "P"
    
    def __init__(self, is_ghost=False):
        super().__init__()
    
    def score(self, state: dict, ghost_id=None):
        if ghost_id: player_key = ghost_id
        else: player_key = 'm'
        return min(manhattan(state['players'][player_key], pill) for pill in state['pills'])
    
class WNode(TerminalNode):
    value = "W"
    
    def __init__(self, is_ghost=False):
        super().__init__()
        self.is_ghost = is_ghost
    
    def score(self, state: dict, ghost_id=None):
        count = 0
        walls = state['walls']
        
        player_key = 'm' if not self.is_ghost else ghost_id
        player = state['players'][player_key]
        surrounding_tiles = ((0,1), (0,-1), (1,0), (-1,0))
        for i, j in surrounding_tiles:
            try:
                if walls[player[0] - i][player[1] - j]:
                    count += 1
            except IndexError: count += 1
        return count
    
class FNode(TerminalNode):
    value = "F"
    
    def __init__(self, is_ghost=False):
        super().__init__()
    
    def score(self, state: dict, ghost_id=None):
        if state['fruit'] is not None:
            return manhattan(state['players']['m'], state['fruit'])
        return 1000
    
class CNode(TerminalNode):
    def __init__(self, is_ghost=False):
        super().__init__()
        self.random_number = random.uniform(-32.0, 32.0)
        self.value = str(float(self.random_number))
                
    
    def score(self, state: dict, ghost_id=None):
        return self.random_number
    
class NonterminalNode(TreeNode):
    def __init__(self):
        self.right = None
        self.left = None
    
    def print(self, depth):
        return f"\n{'|' * depth}{self.value}" + self.left.print(depth + 1) + self.right.print(depth + 1)
    
class AddNode(NonterminalNode):
    value = "+"
    
    def score(self, state, ghost_id=None):
        return self.left.score(state, ghost_id=ghost_id) + self.right.score(state, ghost_id=ghost_id)
    
class SubNode(NonterminalNode):
    value = "-"
    
    def score(self, state, ghost_id=None):
        return self.left.score(state, ghost_id=ghost_id) - self.right.score(state, ghost_id=ghost_id)
    
class MulNode(NonterminalNode):
    value = "*"
    
    def score(self, state, ghost_id=None):
        return self.left.score(state, ghost_id=ghost_id) * self.right.score(state, ghost_id=ghost_id)
    
class DivNode(NonterminalNode):
    value = "/"
    
    def score(self, state, ghost_id=None):
        left_score = self.left.score(state, ghost_id=ghost_id)
        right_score = self.right.score(state, ghost_id=ghost_id)
        epsilon = 1e-9 
        
        if abs(right_score) < epsilon:
            if left_score >= 0.0: return left_score / 0.1
            return left_score / -0.1
        return left_score / right_score

class RANDNode(NonterminalNode):
    value = "RAND"
    
    def score(self, state, ghost_id=None):
        return random.uniform(min(self.left.score(state, ghost_id=ghost_id), self.right.score(state, ghost_id=ghost_id)), max(self.left.score(state, ghost_id=ghost_id), self.right.score(state, ghost_id=ghost_id)))
    
class ParseTreeConstructor:
    def __init__(self, max_depth, is_ghost=False):
        self.max_depth = max_depth
        self.root = None
        self.is_ghost = is_ghost
        if is_ghost:
            self.nonterminals = [AddNode, SubNode, MulNode, DivNode, RANDNode]
            self.terminals = [MNode, GNode, PNode, WNode, FNode, CNode]
        else:
            self.nonterminals = [AddNode, SubNode, MulNode, DivNode, RANDNode]
            self.terminals = [GNode, PNode, WNode, FNode, CNode]

    def full_method(self):
        def full(depth):
            if depth == self.max_depth:
                terminal_node = random.choice(self.terminals)
                return terminal_node(self.is_ghost)
            else:
                curr = random.choice(self.nonterminals)()
                curr.left = full(depth + 1)
                curr.right = full(depth + 1)
                return curr
        
        self.root = full(0)
        return self
    
    def grow_method(self):
        def grow(depth):
            if depth == self.max_depth:
                terminal_node = random.choice(self.terminals)
                return terminal_node(self.is_ghost)
            else:
                curr = random.choice(self.terminals + self.nonterminals)()
                if isinstance(curr, NonterminalNode):
                    curr.left = grow(depth + 1)
                    curr.right = grow(depth + 1)
                return curr
        
        self.root = grow(0)
        return self
        
    def print(self):
        return self.root.print(0).strip()
    
    def score(self, state: dict):
        return self.root.score(state)

    def node_count(self):
        return self.node_counter(self.root)
    
    def node_counter(self, node):
        if node is None:
            return 0
        if isinstance(node, TerminalNode):
            return 1
        return 1 + self.node_counter(node.left) + self.node_counter(node.right)
    
    def height(self):
        return self.max_depth_counter(self.root)
    
    def max_depth_counter(self, node):
        if node is None:
            return -1
        left_depth = self.max_depth_counter(node.left)
        right_depth = self.max_depth_counter(node.right)
        return 1 + max(left_depth, right_depth)
    
    def get_node_depth(self, node, target_node, current_depth=0):
        if node is None:
            return -1  
        if node == target_node:
            return current_depth

        left_depth = self.get_node_depth(node.left, target_node, current_depth + 1)
        if left_depth != -1:
            return left_depth

        right_depth = self.get_node_depth(node.right, target_node, current_depth + 1)
        if right_depth != -1:
            return right_depth

        return -1
    
    def score(self, state: dict, ghost_id=None):
        # Pass ghost_id to the root node's score method
        return self.root.score(state, ghost_id=ghost_id)
    
    
def select_random_node(tree, depth_limit):
        current_node = tree.root
        parent_node = None
        child_key = None
        depth = 0
        
        while current_node is not None and depth < depth_limit:
            action = random.choice(['left', 'right', 'stop'])
            
            if hasattr(current_node, 'left') and action == 'left' and current_node.left is not None:
                parent_node = current_node
                child_key = 'left'
                current_node = current_node.left
            elif hasattr(current_node, 'right') and action == 'right' and current_node.right is not None:
                parent_node = current_node
                child_key = 'right'
                current_node = current_node.right
            else:
                break
            
            depth += 1
        return (parent_node, child_key), current_node

    
class TreeGenotype():
    def __init__(self):
        self.fitness = None
        self.genes = None


    @classmethod
    def initialization(cls, mu, depth_limit, **kwargs):
        population = [cls() for _ in range(mu)]

        # Uncomment these lines to see the primitives available:
        #print(kwargs['terminals'])
        #print(kwargs['nonterminals'])

        # 2a TODO: Initialize genes member variables of individuals
        #          in population using ramped half-and-half.
        #          Pass **kwargs to your functions to give them
        #          the sets of terminal and nonterminal primitives.
        max_depth = depth_limit
        methods = ('full_method', 'grow_method')
        i = 0
        while i < mu:
            for depth in range(2, max_depth + 1):
                for method in methods:
                    is_ghost = ('M' in kwargs['terminals'])
                    population[i].genes = getattr(ParseTreeConstructor(depth, is_ghost=is_ghost), method)()
                    i += 1
                    if i == mu: 
                        return population

        return population


    def to_string(self):
        # 2a TODO: Return a string representing self.genes in the required format.
        return self.genes.print()

    

    def recombine(self, mate, depth_limit, **kwargs):
        child = self.__class__()

        # 2b TODO: Recombine genes of mate and genes of self to
        #          populate child's genes member variable.
        #          We recommend using deepcopy, but also recommend
        #          that you deepcopy the minimal amount possible.
        child = deepcopy(self)
        path_child, subtree_child = select_random_node(child.genes, child.genes.height())
        path_mate, subtree_mate = select_random_node(mate.genes, mate.genes.height())
        
        if subtree_child is None or subtree_mate is None:
            return child
        
        if path_child and path_child[0] is not None and path_child[1] is not None:
            parent_child, child_key_child = path_child
            setattr(parent_child, child_key_child, subtree_mate)
        else:
            child.genes.root = subtree_mate
            
        # print(f"Self:\n{self.to_string()}\nMate:\n{mate.to_string()}\nChild:\n{child.to_string()}")
        
        return child


    def mutate_subtree(self, depth_limit):
        i = 0
        while True:
            mutant = deepcopy(self)
        
            path, subtree = select_random_node(mutant.genes, depth_limit)
            if path and path[0] is not None and path[1] is not None:
                parent, child_key = path
                
                depth_at_insertion = mutant.genes.get_node_depth(mutant.genes.root, parent)
                subtree_depth_limit = depth_limit - depth_at_insertion

                new_subtree = ParseTreeConstructor(subtree_depth_limit).grow_method().root
                setattr(parent, child_key, new_subtree)
                
                if mutant.genes.height() <= depth_limit: return mutant

            i += 1
            if i > 20: return deepcopy(self)
            # I was having way too much trouble with enforcing depth_limit :(


        return mutant

    def mutate_point(self, depth_limit, point_mutation_rate = 0.1):
        mutant = deepcopy(self)

        def mutate_node(node):
            if random.random() < point_mutation_rate:
                if isinstance(node, TerminalNode):
                    return random.choice(self.genes.terminals)()
                elif isinstance(node, NonterminalNode):
                    new_node = random.choice(self.genes.nonterminals)()
                    new_node.left = mutate_node(node.left) if node.left else None
                    new_node.right = mutate_node(node.right) if node.right else None
                    return new_node
            if isinstance(node, NonterminalNode):
                if node.left: node.left = mutate_node(node.left)
                if node.right: node.right = mutate_node(node.right)
            return node

        mutant.genes.root = mutate_node(mutant.genes.root)

        return mutant
    
    def mutate(self, depth_limit, **kwargs):
        mutant = self.__class__()
        # 2b TODO: Mutate mutant.genes to produce a modified tree.
        
        if random.choice(['subtree', 'point']) == 'subtree':
            mutant = self.mutate_subtree(depth_limit)
            # print(f"Self:\n{self.to_string()}\nSubtree Mutant:\n{mutant.to_string()}")
        else:
            mutant = self.mutate_point(depth_limit)
            # print(f"Self:\n{self.to_string()}\nPoint Mutant:\n{mutant.to_string()}")
        return mutant
    
# I was not able to successfully store my treeGenotypes in memory so I found it easier (faster)
# to rebuild them from their parse trees than to re-run the whole experiment
def reconstruct_tree_genotype(parse_tree_str, is_ghost=False):
    lines = parse_tree_str.split('\n')
    node_stack = [None] * (len(lines) + 1)
    root = None

    terminal_node_classes = {
        'G': GNode, 'M': MNode, 'P': PNode, 'W': WNode, 'F': FNode
    }
    nonterminal_node_classes = {
        '+': AddNode, '-': SubNode, '*': MulNode, '/': DivNode, 'RAND': RANDNode
    }

    for line in lines:
        if not line.strip():
            continue

        depth = line.count('|')
        value = line.split('|')[-1].strip()

        try:
            float_value = float(value)
            node = CNode()
            node.random_number = float_value
            node.value = value
        except ValueError:
            if value in terminal_node_classes:
                node = terminal_node_classes[value](is_ghost=is_ghost)
            elif value in nonterminal_node_classes:
                node = nonterminal_node_classes[value]()
            else:
                raise ValueError(f"Unknown node type: {value}")

        node_stack[depth] = node

        if depth == 0:
            root = node
        else:
            parent = node_stack[depth - 1]
            if not parent.left:
                parent.left = node
            else:
                parent.right = node

    tree_genotype = TreeGenotype()
    tree_genotype.genes = ParseTreeConstructor(max_depth=len(lines), is_ghost=is_ghost)
    tree_genotype.genes.root = root

    return tree_genotype