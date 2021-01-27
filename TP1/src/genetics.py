import random

from function_tree import FUNCTION_NODE, CONSTANT_NODE, VAR_NODE, Tree
from symbols import get_random_function, get_random_constant, get_random_variable

def init_tree_full(height, num_variables, p_constant=0.5):
    if height > 0:
        root = Tree(FUNCTION_NODE, get_random_function()) # Internal nodes are only function nodes
        root.lchild = init_tree_full(height-1, num_variables, p_constant)
        root.rchild = init_tree_full(height-1, num_variables, p_constant)
    else:
        if random.random() < p_constant: # Choose between constant terminal or variable terminal
            root = Tree(CONSTANT_NODE, get_random_constant())
        else:
            root = Tree(VAR_NODE, get_random_variable(num_variables))
    return root

def init_tree_grow(height, num_variables, p_function=0.5, p_constant=0.5):
    if height > 0:
        if random.random() < p_function: # Choose between function or terminal
            root = Tree(FUNCTION_NODE, get_random_function())
            root.lchild = init_tree_grow(height-1, num_variables)
            root.rchild = init_tree_grow(height-1, num_variables)
        elif random.random() < p_constant: # Choose between constant terminal or variable terminal
            root = Tree(CONSTANT_NODE, get_random_constant())
        else:
            root = Tree(VAR_NODE, get_random_variable(num_variables))
    else: # Only terminals can be generated on the lowest height
        if random.random() < p_constant: # Choose between constant terminal or variable terminal
            root = Tree(CONSTANT_NODE, get_random_constant())
        else:
            root = Tree(VAR_NODE, get_random_variable(num_variables))
    return root

def initialize_population(population_size, tree_height, num_variables):
    # Initialize population using Ramped half-and-half
    population = []
    trees_per_height = population_size//tree_height
    
    for height in range(1, tree_height+1):
        for _ in range(0, trees_per_height//2):
            tree = init_tree_full(height, num_variables)
            population.append(tree)
        for _ in range(trees_per_height//2, trees_per_height):
            tree = init_tree_full(height, num_variables)
            population.append(tree)
    
    if len(population) < population_size: # Check if not evenly divided
        for _ in range(population_size - len(population)):
            tree = init_tree_full(tree_height, num_variables)
            population.append(tree)

    return population

