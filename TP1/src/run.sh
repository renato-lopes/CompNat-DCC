#!/bin/bash

python main.py --dataset breast_cancer_coimbra \
               --train_csv_path BaseDados/data/breast_cancer_coimbra_train.csv \
               --test_csv_path BaseDados/data/breast_cancer_coimbra_test.csv \
               --population_size 10 \
               --generations 5 \
               --function_tree_size 7 \
               --crossover_prob 0.9 \
               --mutation_prob 0.05 \
               --tournament_k 2 \
               --elitism \
               --output_path out_2 --trials 3 --multiprocessing

