import os
import argparse
import numpy as np

from data import get_instances, INSTANCES, OPTIMAL_MAKESPAN
from aco import aco

from visualization import plot_graph, get_avg_std

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--instances_filepath', type=str, default="./jobshop1.txt", help="Path to file containing the instances")
    parser.add_argument('--instance', type=str, default="ft06", choices=INSTANCES, help="Instance identifier")
    parser.add_argument('--output_dir', type=str, default="./out", help="Path to save results")
    parser.add_argument('--trials', type=int, default=30, help="Amount of independent executions of the algorithm")
    parser.add_argument('--ants', type=int, default=100, help="Amount of ants")
    parser.add_argument('--iterations', type=int, default=100, help="Amount of iterations to execute")
    parser.add_argument('--pheromones_max', type=float, default=100.0, help="Maximum value for pheromone")
    parser.add_argument('--pheromones_min', type=float, default=1.0, help="Minimum value for pheromone")
    parser.add_argument('--alpha', type=float, default=1.0, help="Weight associated to the pheromone")
    parser.add_argument('--beta', type=float, default=2.0, help="Weight associated to the desirability")
    parser.add_argument('--evaporation_rate', type=float, default=0.1, help="Evaporation Rate")
    args = parser.parse_args()

    if not os.path.exists(args.output_dir):
        os.mkdir(args.output_dir)

    instance_data = get_instances(args.instances_filepath)[args.instance]

    trials_best_result = []
    trials_history = []
    for trial in range(args.trials):
        print(f"*** Started Trial [{trial+1}/{args.trials}] ***")
        best_result, history = aco(instance_data["njobs"], instance_data["nmachines"], instance_data["jobs_machines"], instance_data["jobs_costs"],
                                     args.ants, args.iterations, args.pheromones_max, args.pheromones_min, args.alpha, args.beta, args.evaporation_rate)
        print(f"*** Finished Trial [{trial+1}/{args.trials}]: best_result={best_result} ***")

        trials_best_result.append(best_result)
        trials_history.append(history)
    
    plot_graph(trials_history, f"instance:{args.instance}, trials:{args.trials}, ants:{args.ants}, pheromones_max:{args.pheromones_max}, pheromones_min:{args.pheromones_min}, evaporation_rate:{args.evaporation_rate}", args.output_dir)

    trials_best_result = np.array(trials_best_result)
    best_solution_avg, best_solutions_std = get_avg_std(trials_best_result)
    diff_avg, diff_std = get_avg_std(trials_best_result - OPTIMAL_MAKESPAN[args.instance])
    trials_with_optimal = np.sum(trials_best_result == OPTIMAL_MAKESPAN[args.instance])

    print(f"best_result: {best_solution_avg:.4f} {best_solutions_std:.4f}")
    print(f"diff_from_optimal: {diff_avg:.4f} {diff_std:.4f}")
    print(f"optimal_found: {trials_with_optimal}")

    with open(os.path.join(args.output_dir, "results.txt"), "w") as f:
        f.write(f"instance: {args.instance}\ntrials: {args.trials}\nants: {args.ants}\npheromones_max: {args.pheromones_max}\npheromones_min: {args.pheromones_min}\nevaporation_rate: {args.evaporation_rate}\nalpha: {args.alpha}\nbeta: {args.beta}\n")
        f.write(f"best_result: {best_solution_avg:.4f} {best_solutions_std:.4f}\n")
        f.write(f"diff_from_optimal: {diff_avg:.4f} {diff_std:.4f}\n")
        f.write(f"optimal_found: {trials_with_optimal}\n")


if __name__ == "__main__":
    main()

