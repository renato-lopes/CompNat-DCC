import random

from function_tree import FUNCTION_NODE, CONSTANT_NODE, VAR_NODE, LEFT_CHILD, RIGHT_CHILD, Tree
from symbols import get_random_function, get_random_constant, get_random_variable
from clustering import Metric, cluster_data, compute_fmi

MAX_FITNESS=999999

###### Initialization ######

def init_tree_full(height, num_variables, p_constant=0.0):
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

def init_tree_grow(height, num_variables, p_function=0.5, p_constant=0.0):
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

###### Genetic Operators ######

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

def point_mutation(t, num_variables):
    t = t.copy()
    # Get tree nodes
    all_nodes = []
    t.get_function_nodes(all_nodes)
    t.get_terminal_nodes(all_nodes)
    # Choose a node randomly
    random_node = all_nodes[random.randrange(len(all_nodes))][0]
    # Change node value
    if random_node.node_type == FUNCTION_NODE:
        random_node.node_value = get_random_function()
    elif random_node.node_type == CONSTANT_NODE:
        random_node.node_value = get_random_constant()
    elif random_node.node_type == VAR_NODE:
        random_node.node_value = get_random_variable(num_variables)
    else:
        raise ValueError()
    return t

def expansion_mutation(t, num_variables, tree_height, p_full=0.5):
    t = t.copy()
    # Get terminal nodes
    terminal_nodes = []
    t.get_terminal_nodes(terminal_nodes)
    # Choose a node randomly
    random_node, node_level = terminal_nodes[random.randrange(len(terminal_nodes))]
    # Create a random subtree
    if random.random() < p_full:
        new_tree = init_tree_full(tree_height-node_level, num_variables)
    else:
        new_tree = init_tree_grow(tree_height-node_level, num_variables)
    # Add new subtree
    if random_node.parent is not None:
        if random_node.parent[1] == LEFT_CHILD:
           random_node.parent[0].set_left_child(new_tree)
        else:
           random_node.parent[0].set_right_child(new_tree)
    else:
        t = new_tree
    return t

def reduction_mutation(t, num_variables, p_constant=0.0):
    t = t.copy()
    # Get function nodes
    function_nodes = []
    t.get_function_nodes(function_nodes)
    if len(function_nodes) == 0: # Can not reduce
        return t
    # Choose a node randomly
    random_node = function_nodes[random.randrange(len(function_nodes))][0]
    # Create a new terminal node
    if random.random() < 0.5:
        new_node = Tree(CONSTANT_NODE, get_random_constant())
    else:
        new_node = Tree(VAR_NODE, get_random_variable(num_variables))
    # Change old node
    if random_node.parent is not None:
        if random_node.parent[1] == LEFT_CHILD:
           random_node.parent[0].set_left_child(new_node)
        else:
           random_node.parent[0].set_right_child(new_node)
    else:
        t = new_node
    return t

def mutate(t, num_variables, tree_height):
    # Mutate random tree using point, expansion and reduction mutations
    mutation_type = random.randrange(3)
    if mutation_type == 0:
        mutated_t = point_mutation(t, num_variables)
    elif mutation_type == 1:
        mutated_t = expansion_mutation(t, num_variables, tree_height)
    elif mutation_type == 2:
        mutated_t = reduction_mutation(t, num_variables)
    return mutated_t

###### Selection ######

def k_tounament(population, fitness, k):
    # Select a k-size random sample from the population
    indices = random.sample(list(range(len(population))), k)
    best_fitness = 0.0
    best_item = None
    for i in indices:
        if fitness[i] > best_fitness:
            best_fitness = fitness[i]
            best_item = population[i]
    return best_item, best_fitness

###### Fitness ######

def compute_fitness(tree, X, y, num_classes):
    metric = Metric(tree)
    clusters = cluster_data(X, num_classes, metric)
    tree_fitness = compute_fmi(num_classes, clusters, y) # Fitness is given by FMI score
    return tree_fitness
