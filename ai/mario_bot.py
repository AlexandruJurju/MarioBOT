from ai.individual import Individual
from ai.neural_network import NeuralNetwork


class MarioBot(Individual):
    def __init__(self, brain: NeuralNetwork):
        super().__init__(brain)

        self.is_alive = True
        self.won_level = False

        self.ttl = 100
        self.steps_alive = 0
        self.distance_traveled = 0
        self.score = 0

    def calculate_fitness(self):
        return self.fitness
