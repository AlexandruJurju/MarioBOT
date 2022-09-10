import numpy as np

from ai.individual import Individual
from ai.neural_network import NeuralNetwork
from constants import *
from memory_access import *


class MarioBot(Individual):
    def __init__(self, brain: NeuralNetwork):
        super().__init__(brain)

        self.is_alive = True
        self.won_level = False

        self.ttl = 500
        self.steps_alive = 0
        self.current_x = 0
        self.max_distance = 0
        self.score = 0

    # TODO find a fitness function
    def calculate_fitness(self):
        max(self.max_distance ** 1.8 - self.steps_alive ** 1.5 + min(max(self.max_distance - 50, 0), 1) * 2500 + self.won_level * 1e6, 0.00001)

    def model_to_neural_network_input_form(self, model: [int]) -> np.ndarray:
        nn_input = []
        for i in range(len(model)):
            for j in range(len(model[i])):
                nn_input.append(model[i][j])
        nn_input = np.array(nn_input).reshape((-1, 1))

        # new_model = np.zeros((10, 8))
        # for i in range(len(model)):
        #     for j in range(len(model[i])):
        #         new_model[i][j + 1] = model[i][j]
        #         if j == 0:
        #             new_model[i][j] = i + 1
        #
        # for i in range(len(new_model)):
        #     for j in range(len(new_model[i])):
        #         print(new_model[i][j], end=" ")
        #     print()

        return nn_input

    # return action from neural network input
    # check if mario is dead or has won level
    # update mario variables
    # check is mario is stuck -> dead
    def step(self, model: [], ram: np.ndarray):
        if is_player_dead(ram):
            self.is_alive = False

        if self.ttl == 0:
            self.is_alive = False

        if self.is_alive:
            self.steps_alive += 1
            self.current_x = get_mario_level_location(ram).x

            if self.current_x <= self.max_distance:
                self.ttl = self.ttl - 1
            else:
                self.ttl = 500

            if self.current_x > self.max_distance:
                self.max_distance = self.current_x

            processed_input = self.model_to_neural_network_input_form(model)
            nn_output = self.brain.feed_forward(processed_input)

            #         B  X  X  X  U  D  L  R  A
            action = [0, 0, 0, 0, 0, 0, 0, 0, 0]

            for i, output in enumerate(nn_output):
                if output > 0.5:
                    if i > 0:
                        action[i + 3] = 1
                    else:
                        action[0] = 1

            return action

        else:
            return []
