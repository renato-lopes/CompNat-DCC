""" Collection of functions and constant generators """
import random

class sum_f:
    def __call__(self, a, b):
        return a+b
    
    def __str__(self):
        return "SUM"

class sub_f:
    def __call__(self, a, b):
        return a-b
    
    def __str__(self):
        return "SUB"

class mul_f:
    def __call__(self, a, b):
        return a*b
    
    def __str__(self):
        return "MUL"

class div_f:
    def __call__(self, a, b):
        return 0 if b == 0 else float(a)/b
    
    def __str__(self):
        return "DIV"

def random_real():
    return random.uniform(-1, 1)

def random_variable_index(num_variables):
    return random.randrange(num_variables)

FUNCTIONS = [sum_f(), sub_f(), mul_f(), div_f()]
CONSTANTS = [random_real]
VARIABLES = [random_variable_index]

def get_random_function():
    return FUNCTIONS[random.randrange(len(FUNCTIONS))]

def get_random_constant():
    return CONSTANTS[random.randrange(len(CONSTANTS))]()

def get_random_variable(num_variables):
    return VARIABLES[random.randrange(len(VARIABLES))](num_variables)
