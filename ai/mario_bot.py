from ai.individual import Individual
from ai.neural_network import NeuralNetwork


class MarioBot(Individual):
    def __init__(self, brain: NeuralNetwork):
        super().__init__(brain)

        self.score = 0
        self.distance = 0
        self.ttl = 100

    def calculate_fitness(self):
        return self.fitness
