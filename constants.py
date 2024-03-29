from ai.neural_network import NeuralNetwork

WIDTH, HEIGHT = 1000, 650
MAX_FPS = 10000

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

MAX_ENEMIES = 5
GAME_RESOLUTION = (256, 240)
TILE_SIZE = 16
GRID_SIZE = (16, 15)

RIGHT_VIEW = 5
LEFT_VIEW = 1
UP_VIEW = 8
DOWN_VIEW = 1

MINIMAL_VIEW_WIDTH = RIGHT_VIEW + LEFT_VIEW + 1
MINIMAL_VIEW_HEIGHT = UP_VIEW + DOWN_VIEW + 1
INPUT_SIZE_ROW_COUNT = MINIMAL_VIEW_WIDTH * MINIMAL_VIEW_HEIGHT + MINIMAL_VIEW_HEIGHT
INPUT_SIZE_NORMAL = MINIMAL_VIEW_WIDTH * MINIMAL_VIEW_HEIGHT

BOT_TTL = 100

NN_CONFIG = {
    "L1": [INPUT_SIZE_NORMAL, 12],
    "L2": [12, 6]
    # UP DOWN LEFT RIGHT A B
}

MUTATION_RATE = 0.05
SBX_ETA = 100
GAUSSIAN_MUTATION_SCALE = 0.2

NUM_PARENTS_FOR_MATING = 5
NUM_OFFSPRING = 10

GENERAL_NEURAL_NET = NeuralNetwork(NN_CONFIG)
