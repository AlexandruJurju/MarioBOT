from ai.neural_network import NeuralNetwork


class Individual:
    def __init__(self, brain: NeuralNetwork):
        self.fitness = 0
        self.brain = brain

    def calculate_fitness(self):
        pass
