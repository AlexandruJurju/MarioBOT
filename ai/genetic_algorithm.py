import copy
import random
import numpy as np

from typing import List, Tuple, Optional, Union
from individual import Individual
from neural_network import *


# GA selection , selects snake with percentage based on snake fitness // chance for snake to be selected is directly proportional with snake fitness
def roulette_selection(population: List[Individual], individuals_to_select: int) -> List[Individual]:
    selected = []
    # sum of fitness of all snakes in a population, used to select snakes
    sum_pop_fitness = sum(individual.fitness for individual in population)

    # for number of individuals to select : choose a random fitness between 0:pop_fit_sum and initialize current_fitness with 0
    # loop over all snakes in population and sum their fitness with current fitness, if
    for i in range(individuals_to_select):
        random_fitness = random.uniform(0, sum_pop_fitness)
        current_fitness = 0
        for individual in population:
            current_fitness += individual.fitness
            if current_fitness >= random_fitness:
                selected.append(individual)
                break

    return selected


def tournament_selection(population: List[Individual], individuals_to_select: int) -> List[Individual]:
    pass


def two_point_roulette_selection(population: List[Individual], individuals_to_select: int) -> List[Individual]:
    pass


def elitist_selection(population: List[Individual], individuals_to_select: int) -> List[Individual]:
    selected = sorted(population, key=lambda snake: snake.fitness, reverse=True)
    return selected[:individuals_to_select]


# numpy matrix has shape (row_count, col_count)
# swaps weights from a parent to a child from a random row until the end
def one_point_crossover(parent1: NeuralNetwork, parent2: NeuralNetwork) -> Tuple[NeuralNetwork, NeuralNetwork]:
    child1 = copy.deepcopy(parent1)
    child2 = copy.deepcopy(parent2)

    architecture = parent1.neural_net_architecture

    for layer in architecture:
        matrix_rows, matrix_cols = parent1.weights[layer].shape
        rand_row = random.randint(0, matrix_rows)

        # all columns , rows from 0 to rand_row
        child1.weights[layer][:rand_row, :] = parent2.weights[layer][:rand_row, :]
        child2.weights[layer][:rand_row, :] = parent1.weights[layer][:rand_row, :]

        matrix_rows, matrix_cols = parent1.biases[layer].shape
        rand_row = random.randint(0, matrix_rows)

        child1.biases[layer][:rand_row, :] = parent2.biases[layer][:rand_row, :]
        child2.biases[layer][:rand_row, :] = parent1.biases[layer][:rand_row, :]

    return child1, child2


# only swaps weights and biases between 2 random rows from the parent
def two_point_crossover(parent1: NeuralNetwork, parent2: NeuralNetwork) -> Tuple[NeuralNetwork, NeuralNetwork]:
    child1 = copy.deepcopy(parent1)
    child2 = copy.deepcopy(parent2)

    architecture = parent1.neural_net_architecture

    for layer in architecture:
        matrix_rows, matrix_cols = parent1.weights[layer].shape
        rand_row1 = random.randint(0, matrix_rows)
        rand_row2 = random.randint(rand_row1, matrix_rows)

        # all columns , rows from 0 to rand_row
        child1.weights[layer][rand_row1:rand_row2, :] = parent2.weights[layer][rand_row1:rand_row2, :]
        child2.weights[layer][rand_row1:rand_row2, :] = parent1.weights[layer][rand_row1:rand_row2, :]

        matrix_rows, matrix_cols = parent1.biases[layer].shape
        rand_row1 = random.randint(0, matrix_rows)
        rand_row2 = random.randint(rand_row1, matrix_rows)

        child1.biases[layer][rand_row1:rand_row2, :] = parent2.biases[layer][rand_row1:rand_row2, :]
        child2.biases[layer][rand_row1:rand_row2, :] = parent1.biases[layer][rand_row1:rand_row2, :]

    return child1, child2


def uniform_crossover(parent1: np.ndarray, parent2: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    pass


def arithmetic_crossover(parent1: np.ndarray, parent2: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    pass


def whole_mutation(child: NeuralNetwork, mutation_rate: float) -> NeuralNetwork:
    pass


def gaussian_mutation() -> None:
    pass


def random_uniform_mutation(c) -> None:
    pass


def simulated_binary_crossover(parent1: np.ndarray, parent2: np.ndarray, eta: float) -> Tuple[np.ndarray, np.ndarray]:
    pass


def single_point_binary_crossover(parent1: np.ndarray, parent2: np.ndarray, major='r') -> Tuple[np.ndarray, np.ndarray]:
    pass
