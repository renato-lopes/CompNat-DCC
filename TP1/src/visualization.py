import os
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('tableau-colorblind10')

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
    plt.plot(stats["avg_fitness"][0], '--', label='Avg Fitness')
    plt.plot(stats["min_fitness"][0], '-', label='Min Fitness')
    plt.legend()
    plt.xlabel('Generation')
    plt.ylabel('Fitness')
    plt.xticks(X)
    plt.title(f'Max/Avg/Min Fitness per Generation\n{title}')
    plt.savefig(os.path.join(save_path, "fitness.png"))
    plt.close()

    # Bar graph
    data = [stats["children_better_crossover"][0], stats["children_worse_crossover"][0], stats["children_better_mutation"][0], stats["children_worse_mutation"][0]]
    fig = plt.figure(figsize=(8, 4))
    ax = fig.add_subplot(111)
    ax.bar(X - 0.2, data[0], color = 'b', width = 0.1)
    ax.bar(X - 0.1, data[1], color = 'g', width = 0.1)
    ax.bar(X + 0.0, data[2], color = 'r', width = 0.1)
    ax.bar(X + 0.1, data[3], color = 'm', width = 0.1)
    plt.legend(labels=['children_better_crossover', 'children_worse_crossover', 'children_better_mutation', 'children_worse_mutation'])
    ax.set_xlabel('Generation')
    ax.set_ylabel('Number of samples')
    ax.set_title(f'Parent/Children Comparison\n{title}')
    ax.set_xticks(X)
    ax.set_yticks(range(0, int(np.max(data)), 10))
    plt.savefig(os.path.join(save_path, "operators_comparison.png"))
    plt.close()

    # Fitness graph
    plt.figure(figsize=(8, 4))
    plt.plot(stats["equal_trees"][0], '-', label='Equal Trees')
    plt.legend()
    plt.xlabel('Generation')
    plt.ylabel('Number of Trees')
    plt.xticks(X)
    plt.title(f'Equal Trees in Population per Generation\n{title}')
    plt.savefig(os.path.join(save_path, "equal.png"))
    plt.close()
