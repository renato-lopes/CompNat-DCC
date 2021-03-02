import os
import argparse
import numpy as np

from data import get_instances, INSTANCES
from aco import aco


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--instances_filepath', type=str, default="./jobshop1.txt", help="Path to file containing the instances")
    parser.add_argument('--instance', type=str, default="ft06", choices=INSTANCES, help="Instance identifier")
    args = parser.parse_args()

    instance_data = get_instances(args.instances_filepath)[args.instance]

    # instance_data = {
    #     "njobs": 3,
    #     "nmachines": 3,
    #     "jobs_machines": [[0, 1, 2], [0, 2, 1], [1, 0, 2]],
    #     "jobs_costs": [[3, 3, 2], [1, 5, 3], [3, 2, 3]]
    # }

    # instance_data = {
    #     "njobs": 3,
    #     "nmachines": 3,
    #     "jobs_machines": [[0], [1], [2]],
    #     "jobs_costs": [[1], [1], [1]]
    # }

    best_makespan, history = aco(instance_data["njobs"], instance_data["nmachines"], instance_data["jobs_machines"], instance_data["jobs_costs"], 10, 100)
    print(best_makespan)

if __name__ == "__main__":
    main()

