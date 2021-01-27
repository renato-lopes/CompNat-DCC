""" Collection of functions and constant generators """
import random

def sum_f(a, b):
    return a+b

def sub_f(a, b):
    return a-b

def mul_f(a, b):
    return a*b

def div_f(a, b):
    return 0 if b == 0 else float(a)/b

def random_real():
    return random.uniform(-1, 1)

def random_variable_index(num_variables):
    return random.randrange(num_variables)

FUNCTIONS = [sum_f, sub_f, mul_f, div_f]
CONSTANTS = [random_real]
VARIABLES = [random_variable_index]

def get_random_function():
    return FUNCTIONS[random.randrange(len(FUNCTIONS))]

def get_random_constant():
    return CONSTANTS[random.randrange(len(CONSTANTS))]()

def get_random_variable(num_variables):
    return VARIABLES[random.randrange(len(VARIABLES))](num_variables)
