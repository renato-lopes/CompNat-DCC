import os
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('tableau-colorblind10')

def get_avg_std(data):
    return np.average(data, axis=0), np.std(data, axis=0)

def plot_graph(trials_history, title, save_dir):
    best_solutions = []
    worst_solutions = []
    average_solutions = []
    for trial_data in trials_history:
        trial_results_best = [np.min(trial_data[k]["ants_results"]) for k in trial_data.keys()]
        trial_results_worst = [np.max(trial_data[k]["ants_results"]) for k in trial_data.keys()]
        trial_results_average = [np.average(trial_data[k]["ants_results"]) for k in trial_data.keys()]
        best_solutions.append(trial_results_best)
        worst_solutions.append(trial_results_worst)
        average_solutions.append(trial_results_average)
    
    best_solutions_avg, best_solutions_std = get_avg_std(best_solutions)
    worst_solutions_avg, worst_solutions_std = get_avg_std(worst_solutions)
    average_solutions_avg, average_solutions_std = get_avg_std(average_solutions)

    X = np.arange(best_solutions_avg.shape[0])
    plt.figure(figsize=(10, 5))
    plt.plot(best_solutions_avg, '-', label='Best Solution')
    plt.fill_between(X, best_solutions_avg-best_solutions_std, best_solutions_avg+best_solutions_std, alpha=.1)
    plt.plot(average_solutions_avg, '-', label='Average Solution')
    plt.fill_between(X, average_solutions_avg-average_solutions_std, average_solutions_avg+average_solutions_std, alpha=.1)
    plt.plot(worst_solutions_avg, '-', label='Worst Solution')
    plt.fill_between(X, worst_solutions_avg-worst_solutions_std, worst_solutions_avg+worst_solutions_std, alpha=.1)
    plt.legend()
    plt.xlabel('Iteration')
    plt.ylabel('Makespan')
    plt.title(f'Makespan per Iteration\n{title}')
    plt.savefig(os.path.join(save_dir, "makespan.png"))
    plt.close()

