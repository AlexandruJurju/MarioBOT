import copy
import random
import numpy as np

from typing import List, Tuple, Optional
from ai.individual import Individual
from ai.neural_network import NeuralNetwork


# =========== SELECTION ===========

# GA selection , selects individual with percentage based on individual fitness
# Chance for and individual to be selected from population is directly proportional with its fitness
def roulette_selection(population: List[Individual], individuals_to_select: int) -> List[Individual]:
    selected = []
    sum_pop_fitness = sum(individual.fitness for individual in population)

    # Choose a random value between 0 and sum_pop_fitness
    # Loop over individuals in population and sum their fitness in current_fitness, if current_fitness >= random_fitness then the individual is selected
    for i in range(individuals_to_select):
        random_fitness = random.uniform(0, sum_pop_fitness)
        current_fitness = 0
        for individual in population:
            current_fitness += individual.fitness
            if current_fitness >= random_fitness:
                selected.append(individual)
                break

    return selected


def tournament_selection(population: List[Individual], individuals_to_select: int, tournament_size: int) -> List[Individual]:
    selected = []
    for i in range(individuals_to_select):
        tournament = np.random.choice(population, tournament_size)
        selected.append(max(tournament, key=lambda individual: individual.fitness))


def two_point_roulette_selection(population: List[Individual], individuals_to_select: int) -> List[Individual]:
    pass


# Returns the best n individuals from a population by fitness
def elitist_selection(population: List[Individual], individuals_to_select: int) -> List[Individual]:
    selected = population.sort(key=lambda individual: individual.fitness, reverse=True)
    return selected[:individuals_to_select]


# =========== CROSSOVER ===========

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


def uniform_crossover(parent1: NeuralNetwork, parent2: NeuralNetwork) -> Tuple[np.ndarray, np.ndarray]:
    pass


def arithmetic_crossover(parent1: np.ndarray, parent2: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    pass


def simulated_binary_crossover(parent1: NeuralNetwork, parent2: NeuralNetwork, eta: float) -> Tuple[NeuralNetwork, NeuralNetwork]:
    child1 = copy.deepcopy(parent1)
    child2 = copy.deepcopy(parent2)

    for layer in parent1.neural_net_architecture:
        parent1_weights = parent1.weights[layer]
        parent2_weights = parent2.weights[layer]

        rand = np.random.random(parent1_weights.shape)
        gamma = np.empty(parent1_weights.shape)

        gamma[rand <= 0.5] = (2 * rand[rand <= 0.5]) ** (1.0 / (eta + 1))
        gamma[rand > 0.5] = (1.0 / (2.0 * (1.0 - rand[rand > 0.5]))) ** (1.0 / (eta + 1))

        child1.weights[layer] = 0.5 * ((1 + gamma) * parent1_weights + (1 - gamma) * parent2_weights)
        child2.weights[layer] = 0.5 * ((1 - gamma) * parent1_weights + (1 + gamma) * parent2_weights)

        child1.weights[layer] = np.clip(child1.weights[layer], -1, 1)
        child2.weights[layer] = np.clip(child2.weights[layer], -1, 1)

    for layer in parent1.neural_net_architecture:
        parent1_biases = parent1.biases[layer]
        parent2_biases = parent2.biases[layer]

        rand = np.random.random(parent1_biases.shape)
        gamma = np.empty(parent1_biases.shape)

        gamma[rand <= 0.5] = (2 * rand[rand <= 0.5]) ** (1.0 / (eta + 1))
        gamma[rand > 0.5] = (1.0 / (2.0 * (1.0 - rand[rand > 0.5]))) ** (1.0 / (eta + 1))

        child1.biases[layer] = 0.5 * ((1 + gamma) * parent1_biases + (1 - gamma) * parent2_biases)
        child2.biases[layer] = 0.5 * ((1 - gamma) * parent1_biases + (1 + gamma) * parent2_biases)

        child1.biases[layer] = np.clip(child1.biases[layer], -1, 1)
        child2.biases[layer] = np.clip(child2.biases[layer], -1, 1)

    return child1, child2


def uniform_binary_crossover(parent1: NeuralNetwork, parent2: NeuralNetwork) -> Tuple[np.ndarray, np.ndarray]:
    pass


def single_point_binary_crossover(parent1: NeuralNetwork, parent2: NeuralNetwork) -> Tuple[NeuralNetwork, NeuralNetwork]:
    child1 = copy.deepcopy(parent1)
    child2 = copy.deepcopy(parent2)

    for layer in parent1.neural_net_architecture:
        matrix_rows, matrix_cols = parent1.weights[layer].shape
        row = np.random.randint(0, matrix_rows)
        col = np.random.randint(0, matrix_cols)


# =========== MUTATION ===========

def whole_mutation(child: NeuralNetwork, mutation_rate: float) -> NeuralNetwork:
    pass


def gaussian_mutation(individual: NeuralNetwork, mutation_probability: float, scale: Optional[float]) -> None:
    for layer in individual.neural_net_architecture:
        # Matrix of True and False , used for finding out what index will be mutated
        mutation_array = np.random.random(individual.weights[layer].shape) < mutation_probability
        gauss_mutation = np.random.normal(size=individual.weights[layer].shape)

        if scale:
            gauss_mutation[mutation_array] *= scale

        individual.weights[layer][mutation_array] += gauss_mutation[mutation_array]

    for layer in individual.neural_net_architecture:
        mutation_array = np.random.random(individual.biases[layer].shape) < mutation_probability
        gauss_mutation = np.random.normal(size=individual.biases[layer].shape)

        if scale:
            gauss_mutation[mutation_array] *= scale

        individual.biases[layer][mutation_array] += gauss_mutation[mutation_array]


def random_uniform_mutation(c):
    pass
