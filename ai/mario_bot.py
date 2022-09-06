from individual import Individual


class MarioBot(Individual):
    def __init__(self):
        super().__init__()

        self.score = 0
        self.ttl = 100

    def calculate_fitness(self):
        return 10
