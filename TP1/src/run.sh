#!/bin/bash

# Extraia o arquivo zip com a base de dados (BaseDados.zip) no mesmo diretório deste script

python main.py --output_path out/ \
               --dataset breast_cancer_coimbra \
               --train_csv_path BaseDados/data/breast_cancer_coimbra_train.csv \
               --test_csv_path BaseDados/data/breast_cancer_coimbra_test.csv \
               --population_size 10 \
               --generations 10 \
               --function_tree_size 7 \
               --crossover_prob 0.9 \
               --mutation_prob 0.05 \
               --tournament_k 5 \
               --elitism \
               --trials 10 --multiprocessing
