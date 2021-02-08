import os
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('tableau-colorblind10')
from matplotlib.ticker import LinearLocator

computed_stats = {'max_fitness', 'avg_fitness', 'min_fitness', 'children_better_crossover', 'children_worse_crossover', 'children_better_mutation', 'children_worse_mutation', 'equal_trees'}

def get_stats_avg_std(global_history):
    data = {}
    for stat in computed_stats:
        data[stat] = []

    for i in global_history.keys():
        for stat in computed_stats:
            data[stat].append(global_history[i][stat])
    
    stats = {}
    for stat in computed_stats:
        stats[stat] = [np.average(data[stat], axis=0), np.std(data[stat], axis=0)]
    return stats

def plot_graphs(global_history, title, save_path):
    stats = get_stats_avg_std(global_history)

    X = np.arange(stats['children_better_crossover'][0].shape[0])
    # Fitness graph
    plt.figure(figsize=(8, 4))
    plt.plot(stats["max_fitness"][0], '-', label='Max Fitness')
    plt.fill_between(X, stats["max_fitness"][0]-stats["max_fitness"][1], stats["max_fitness"][0]+stats["max_fitness"][1], alpha=.1)
    plt.plot(stats["avg_fitness"][0], '--', label='Avg Fitness')
    plt.fill_between(X, stats["avg_fitness"][0]-stats["avg_fitness"][1], stats["avg_fitness"][0]+stats["avg_fitness"][1], alpha=.1)
    plt.plot(stats["min_fitness"][0], '-', label='Min Fitness')
    plt.fill_between(X, stats["min_fitness"][0]-stats["min_fitness"][1], stats["min_fitness"][0]+stats["min_fitness"][1], alpha=.1)
    plt.legend()
    plt.xlabel('Generation')
    plt.ylabel('Fitness')
    # plt.xticks(X)
    plt.title(f'Max/Avg/Min Fitness per Generation\n{title}')
    plt.savefig(os.path.join(save_path, "fitness.png"))
    plt.close()

    # Bar graph Crossover
    fig = plt.figure(figsize=(8, 4))
    ax = fig.add_subplot(111)
    ax.bar(X, stats["children_better_crossover"][0], color = 'b', width = 0.5)
    ax.bar(X, stats["children_worse_crossover"][0], bottom = stats["children_better_crossover"][0], color = 'r', width = 0.5)
    plt.legend(labels=['children_better_crossover', 'children_worse_crossover'])
    ax.set_xlabel('Generation')
    ax.set_ylabel('Number of trees')
    ax.set_title(f'Parent/Children Comparison - Crossover\n{title}')
    # ax.set_xticks(X)
    # ax.get_xaxis().set_major_locator(LinearLocator(numticks=20))
    # ax.set_yticks(range(0, int(np.max(data)), 10))
    plt.savefig(os.path.join(save_path, "crossover.png"))
    plt.close()

    # Bar graph Mutation
    fig = plt.figure(figsize=(8, 4))
    ax = fig.add_subplot(111)
    ax.bar(X, stats["children_better_mutation"][0], color = 'b', width = 0.5)
    ax.bar(X, stats["children_worse_mutation"][0], bottom = stats["children_better_mutation"][0], color = 'r', width = 0.5)
    plt.legend(labels=['children_better_mutation', 'children_worse_mutation'])
    ax.set_xlabel('Generation')
    ax.set_ylabel('Number of trees')
    ax.set_title(f'Parent/Children Comparison - Mutation\n{title}')
    # ax.set_xticks(X)
    # ax.get_xaxis().set_major_locator(LinearLocator(numticks=20))
    # ax.set_yticks(range(0, int(np.max(data)), 10))
    plt.savefig(os.path.join(save_path, "mutation.png"))
    plt.close()

    # Fitness graph
    fig = plt.figure(figsize=(8, 4))
    ax = fig.add_subplot(111)
    ax.bar(X, stats["equal_trees"][0], color = 'b', width = 0.5)
    plt.legend(labels=['equal_trees'])
    ax.set_xlabel('Generation')
    ax.set_ylabel('Number of trees')
    # plt.xticks(X)
    ax.set_title(f'Equal Trees in Population per Generation\n{title}')
    plt.savefig(os.path.join(save_path, "equal.png"))
    plt.close()
