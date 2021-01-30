import os
import pickle
import argparse
import random
import numpy as np
import json
from multiprocessing import Process, Queue, cpu_count

from data import read_csv, normalize_data, BREAST_CANCER_COIMBRA_DATASET, GLASS_DATASET
from genetics import initialize_population, crossover, mutate, k_tounament, compute_fitness
from visualization import plot_graphs

def execute_trials(trials, global_history, best_fitness_global, best_fitness_test_global, num_variables, num_classes, train_X, train_y, test_X, test_y, args, queue=None):
    for trial in trials:
        print(f"*** Starting trial {trial} of {args.trials} ***")
        # Create output dir for trial
        if not os.path.exists(os.path.join(args.output_path, str(trial))):
            os.mkdir(os.path.join(args.output_path, str(trial)))
        
        # Create log file
        log_file = open(os.path.join(args.output_path, str(trial), "log.txt"), "w")

        # History with important statistics
        history = {}
        history['max_fitness'] = []
        history['avg_fitness'] = []
        history['min_fitness'] = []
        history['children_better_crossover'] = []
        history['children_worse_crossover'] = []
        history['children_better_mutation'] = []
        history['children_worse_mutation'] = []

        # Initialize population with random solutions (Ramped half-and-half)
        population = initialize_population(args.population_size, args.function_tree_size, num_variables)

        # Calculate initial population fitness
        fitness_population = []
        for tree in population:
            tree_fitness = compute_fitness(tree, train_X, train_y, num_classes)
            fitness_population.append(tree_fitness)
        
        # Evolutionary Loop
        for generation in range(args.generations):
            children = []
            fitness_children = []
            children_better_crossover = 0
            children_worse_crossover = 0
            children_better_mutation = 0
            children_worse_mutation = 0
            # Generate Children
            while len(children) < args.population_size:
                # Crossover
                if random.random() < args.crossover_prob:
                    # Parent Selection
                    p1, fitness_p1 = k_tounament(population, fitness_population, args.tournament_k)
                    p2, fitness_p2 = k_tounament(population, fitness_population, args.tournament_k)

                    avg_parent_fitness = (fitness_p1 + fitness_p2)/2
                
                    c1, c2 = crossover(p1, p2)

                    # Calculate children fitness
                    fitness_c1 = compute_fitness(c1, train_X, train_y, num_classes)
                    fitness_c2 = compute_fitness(c2, train_X, train_y, num_classes)

                    if fitness_c1 < avg_parent_fitness:
                        children_worse_crossover += 1
                    else:
                        children_better_crossover += 1
                    if fitness_c2 < avg_parent_fitness:
                        children_worse_crossover += 1
                    else:
                        children_better_crossover += 1

                    children.append(c1)
                    children.append(c2)
                    fitness_children.append(fitness_c1)
                    fitness_children.append(fitness_c2)
                
                # Mutation
                if random.random() < args.mutation_prob:
                    # Parent Selection
                    p, fitness_p = k_tounament(population, fitness_population, args.tournament_k)
                    
                    child = mutate(p, num_variables, args.function_tree_size)
                    
                    fitness_child = compute_fitness(child, train_X, train_y, num_classes)

                    if fitness_child < fitness_p:
                        children_worse_mutation += 1
                    else:
                        children_better_mutation += 1
                    
                    children.append(child)
                    fitness_children.append(fitness_child)
            
            # Update population
            if args.elitism:
                best_parent_i = np.argmax(fitness_population)
                worst_child_i = np.argmin(fitness_children)
                # Enforce that the best parent stays in the population
                children[worst_child_i] = population[best_parent_i]
                fitness_children[worst_child_i] = fitness_population[best_parent_i]

            # Change parents with children
            population = children
            fitness_population = fitness_children

            # Compute statistics
            max_fitness = np.max(fitness_population)
            avg_fitness = np.average(fitness_population)
            min_fitness = np.min(fitness_population)
            history['max_fitness'].append(max_fitness)
            history['avg_fitness'].append(avg_fitness)
            history['min_fitness'].append(min_fitness)
            history['children_better_crossover'].append(children_better_crossover)
            history['children_worse_crossover'].append(children_worse_crossover)
            history['children_better_mutation'].append(children_better_mutation)
            history['children_worse_mutation'].append(children_worse_mutation)

            log_file.write(f"Generation {generation+1}/{args.generations}: max_fitness={max_fitness:.4f} avg_fitness={avg_fitness:.4f} min_fitness={min_fitness:.4f}\n")
        
        # Get best found solution
        best_solution_i = np.argmax(fitness_population)
        best_solution = population[best_solution_i]
        best_fitness = fitness_population[best_solution_i]

        # Evaluate best solution on test data
        best_fitness_test = compute_fitness(best_solution, test_X, test_y, num_classes)

        # Write results
        log_file.write(f"Best fitness train: {best_fitness:.4f}\n")
        log_file.write(f"Best fitness test: {best_fitness_test:.4f}\n")

        if args.multiprocessing:
            queue.put((trial, best_fitness, best_fitness_test, history))
        else:
            best_fitness_global.append(best_fitness)
            best_fitness_test_global.append(best_fitness_test)
            global_history[trial] = history

        with open(os.path.join(args.output_path, str(trial), "history.pickle"), 'wb') as f:
            pickle.dump(history, f)
        
        log_file.close()
        print(f"*** Finished trial {trial} of {args.trials} ***")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset', type=str, required=True, choices=[BREAST_CANCER_COIMBRA_DATASET, GLASS_DATASET], help="Dataset name")
    parser.add_argument('--train_csv_path', type=str, required=True, help="Path to csv file containing training data")
    parser.add_argument('--test_csv_path', type=str, required=True, help="Path to csv file containing test data")
    parser.add_argument('--output_path', type=str, default="out/", help="Path to save output")
    parser.add_argument('--trials', type=int, default=10, help="Number of times to execute the algorithm")
    parser.add_argument('--population_size', type=int, default=100, help="Amount of functions in the population")
    parser.add_argument('--generations', type=int, default=100, help="Number of generations to execute")
    parser.add_argument('--function_tree_size', type=int, default=7, help="Maximum height of each function tree")
    parser.add_argument('--crossover_prob', type=float, default=0.9, help="Probability associated with the crossover operator")
    parser.add_argument('--mutation_prob', type=float, default=0.05, help="Probability associated with the mutation operator")
    parser.add_argument('--tournament_k', type=int, default=5, help="Number of solutions selected for each tournament during selection stage")
    parser.add_argument('--elitism', action='store_true', help="Use elitism")
    parser.add_argument('--multiprocessing', action='store_true', help="Use multiprocessing")
    args = parser.parse_args()

    if not os.path.exists(args.output_path):
        os.mkdir(args.output_path)

    # Read train and test data
    train_data = read_csv(args.train_csv_path)
    test_data = read_csv(args.test_csv_path)

    if args.dataset == BREAST_CANCER_COIMBRA_DATASET:
        train_y = train_data['Classification']
        train_X = train_data.drop(['Classification'], axis=1)
        
        test_y = test_data['Classification']
        test_X = test_data.drop(['Classification'], axis=1)
    elif args.dataset == GLASS_DATASET:
        train_y = train_data['glass_type']
        train_X = train_data.drop(['glass_type'], axis=1)
        
        test_y = test_data['glass_type']
        test_X = test_data.drop(['glass_type'], axis=1)

    # Normalize data
    train_X = normalize_data(train_X)
    test_X = normalize_data(test_X)

    num_classes = len(train_y.unique())
    num_variables = train_X.shape[1]

    global_history = {} # History with statistics for all trials
    best_fitness_global = []
    best_fitness_test_global = []

    # Execute the GP
    trials = list(range(1, args.trials+1, 1))
    if args.multiprocessing:
        n_cores = cpu_count()
        print("CPU_COUNT", n_cores)
        trials = np.array_split(trials, n_cores)

        queue = Queue()

        procs = []
        for trial_set in trials:
            p = Process(target=execute_trials, args=(trial_set, global_history, best_fitness_global, best_fitness_test_global, num_variables, num_classes, train_X, train_y, test_X, test_y, args, queue))
            procs.append(p)
            p.start()

        for p in procs: # Wait for all the created process to finish
            p.join()
        
        # Get results
        best_fitness_global = [0.0]*args.trials
        best_fitness_test_global = [0.0]*args.trials
        
        while not queue.empty():
            t, t_fitness, t_fitness_test, t_history = queue.get()
            global_history[t] = t_history
            best_fitness_global[t-1] = t_fitness
            best_fitness_test_global[t-1] = t_fitness_test
            
    else:
        execute_trials(trials, global_history, best_fitness_global, best_fitness_test_global, num_variables, num_classes, train_X, train_y, test_X, test_y, args)

    with open(os.path.join(args.output_path, "global_history.pickle"), 'wb') as f:
        pickle.dump(global_history, f)

    plot_graphs(global_history, f"{args.dataset} - pop_size:{args.population_size}, p_c:{args.crossover_prob:.2f}, p_m:{args.mutation_prob:.2f}, k:{args.tournament_k} {'- Elitism' if args.elitism else ''}", args.output_path)


if __name__ == '__main__':
    main()
