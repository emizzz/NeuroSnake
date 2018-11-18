#try here your fitness functions, than add the in in the ai_config file


import math

def calculate_fitness_0(self):
    return math.floor(self.lifetime * (self.max_size ** 2))


def calculate_fitness_1(self):
    return math.floor(self.lifetime * 2 * (self.max_size ** 2))


def calculate_fitness_2(self):
    return math.floor(self.lifetime * self.max_size)


fitness_functions = [calculate_fitness_0, calculate_fitness_1, calculate_fitness_2]
