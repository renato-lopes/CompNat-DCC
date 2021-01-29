import random

from function_tree import FUNCTION_NODE, CONSTANT_NODE, VAR_NODE, LEFT_CHILD, RIGHT_CHILD, Tree
from symbols import get_random_function, get_random_constant, get_random_variable

def init_tree_full(height, num_variables, p_constant=0.5):
    if height > 0:
        root = Tree(FUNCTION_NODE, get_random_function()) # Internal nodes are only function nodes
        root.set_left_child(init_tree_full(height-1, num_variables, p_constant))
        root.set_right_child(init_tree_full(height-1, num_variables, p_constant))
    else:
        if random.random() < p_constant: # Choose between constant terminal or variable terminal
            root = Tree(CONSTANT_NODE, get_random_constant())
        else:
            root = Tree(VAR_NODE, get_random_variable(num_variables))
    return root

def init_tree_grow(height, num_variables, p_function=0.7, p_constant=0.2):
    if height > 0:
        if random.random() < p_function: # Choose between function or terminal
            root = Tree(FUNCTION_NODE, get_random_function())
            root.set_left_child(init_tree_grow(height-1, num_variables))
            root.set_right_child(init_tree_grow(height-1, num_variables))
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
            tree = init_tree_grow(height, num_variables)
            population.append(tree)
        for _ in range(trees_per_height//2, trees_per_height):
            tree = init_tree_full(height, num_variables)
            population.append(tree)
    
    if len(population) < population_size: # Check if not evenly divided
        for _ in range(population_size - len(population)):
            tree = init_tree_full(tree_height, num_variables)
            population.append(tree)

    return population

def crossover(t1, t2):
    t1 = t1.copy()
    t2 = t2.copy()
    height = min(t1.height(), t2.height())
    crossover_level = random.randrange(height+1)
    # Get all nodes in the chosen level in both trees
    nodes_t1 = []
    t1.get_nodes_at_level(nodes_t1, crossover_level)
    nodes_t2 = []
    t2.get_nodes_at_level(nodes_t2, crossover_level)
    # Choose random node in each tree at the chosen level
    n_t1 = nodes_t1[random.randrange(len(nodes_t1))]
    n_t2 = nodes_t2[random.randrange(len(nodes_t2))]
    # Swap nodes between trees
    p_t1 = n_t1.parent
    p_t2 = n_t2.parent
    n_t1.parent = p_t2
    n_t2.parent = p_t1
    if p_t2 is not None:
        if p_t2[1] == LEFT_CHILD:
            p_t2[0].lchild = n_t1
        else:
            p_t2[0].rchild = n_t1
    if p_t1 is not None:
        if p_t1[1] == LEFT_CHILD:
            p_t1[0].lchild = n_t2
        else:
            p_t1[0].rchild = n_t2
    return t1, t2
