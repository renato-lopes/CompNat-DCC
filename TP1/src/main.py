import argparse

from data import read_csv, BREAST_CANCER_COIMBRA_DATASET, GLASS_DATASET
from genetics import initialize_population, crossover, mutate
from clustering import Metric, cluster_data, compute_fmi

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset', type=str, choices=[BREAST_CANCER_COIMBRA_DATASET, GLASS_DATASET], help="Dataset name")
    parser.add_argument('--train_csv_path', type=str, help="Path to csv file containing training data")
    parser.add_argument('--test_csv_path', type=str, help="Path to csv file containing test data")
    parser.add_argument('--population_size', type=str, help="Amount of functions in the population")
    parser.add_argument('--generations', type=int, help="Number of generations to execute")
    parser.add_argument('--function_tree_size', type=int, help="Maximum height of each function tree")
    parser.add_argument('--crossover_prob', type=float, help="Probability associated with the crossover operator")
    parser.add_argument('--mutation_prob', type=float, help="Probability associated with the mutation operator")
    parser.add_argument('--tournament_k', type=int, help="Number of solutions selected for each tournament during selection stage")
    parser.add_argument('--elitism', action='store_true', help="Use elitism")
    args = parser.parse_args()

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

    num_classes = len(train_y.unique())
    num_variables = train_X.shape[1]

    pop = initialize_population(10, 7, num_variables)

    metric = Metric(pop[3])

    clusters = cluster_data(train_X, num_classes, metric)
    print(compute_fmi(num_classes, clusters, train_y))



if __name__ == '__main__':
    main()
