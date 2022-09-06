import retro
import pygame
import numpy as np

from constants import *
from memory_access import *

player_action = [1, 0, 0, 0, 0, 0, 0, 0, 0]


class SuperMarioBros:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("SMB")

        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        self.fps_clock = pygame.time.Clock()
        self.running = True

        self.env = retro.make(game='SuperMarioBros-Nes', state='Level1-1')
        observation = self.env.reset()

        print(self.env.buttons)
        print(self.env.observation_space.shape)  # Dimensions of a frame
        print(self.env.action_space.n)  # Number of actions our agent can take

    def process_events(self):
        global player_action
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                if event.key == pygame.K_UP:
                    player_action = [0, 0, 0, 0, 0, 0, 0, 0, 1]
                if event.key == pygame.K_RIGHT:
                    player_action = [0, 0, 0, 0, 0, 0, 0, 1, 0]
                if event.key == pygame.K_LEFT:
                    player_action = [0, 0, 0, 0, 0, 0, 1, 0, 0]
                if event.key == pygame.K_r:
                    self.env.reset()

    def run(self):

        top_left_corner = Point(6, 4)
        bottom_right_corner = Point(15, 13)
        observation_x = 10
        observation_y = 10

        while self.running:
            self.window.fill(WHITE)
            self.process_events()

            observation, reward, done, info = self.env.step(player_action)
            ram = self.env.get_ram()

            self.draw_game_windows(observation)
            tile_map = get_tiles(ram)
            self.draw_model_from_tile_map(tile_map)
            model_map_from_tile_map(tile_map)

            pygame.display.update()
            self.fps_clock.tick(MAX_FPS)

    def draw_game_windows(self, rgb_array):
        # draw game window from np array
        game_window = np.swapaxes(rgb_array, 0, 1)
        new_surf = pygame.pixelcopy.make_surface(game_window)
        new_surf = pygame.transform.scale2x(new_surf)
        self.window.blit(new_surf, (25, 25))

    def draw_snes_controller(self, action: []):
        square_base_x = 600
        square_base_y = 500
        square_width = 50
        square_height = 50
        square_distance = 65

        circle_base_x = square_base_x + square_distance * 4
        circle_base_y = square_base_y + 25
        circle_radius = 20
        circle_distance = 65

        controller_left_corner = (square_base_x - 25, square_base_y - 100)
        controller_width_height = ((circle_base_x + circle_distance) - square_base_x + square_distance + circle_distance, square_height * 5)

        pygame.draw.rect(self.window, (0, 125, 200), pygame.Rect(controller_left_corner, controller_width_height))

        # get a map of form BUTTON : 0 if buttons is not pressed, 1 if button is pressed
        buttons = self.env.buttons
        colors = {}
        for i, button in enumerate(buttons):
            # colors[button] = action[i]
            if action[i] == 1:
                colors[button] = GREEN
            else:
                colors[button] = BLACK

        # LEFT
        pygame.draw.rect(self.window, colors["LEFT"], pygame.Rect(square_base_x, square_base_y, square_width, square_height))

        # RIGHT
        pygame.draw.rect(self.window, colors["RIGHT"], pygame.Rect(square_base_x + square_distance * 2, square_base_y, square_width, square_height))

        # UP
        pygame.draw.rect(self.window, colors["UP"], pygame.Rect(square_base_x + square_distance, square_base_y - square_distance, square_width, square_height))

        # DOWN
        pygame.draw.rect(self.window, colors["DOWN"], pygame.Rect(square_base_x + square_distance, square_base_y + square_distance, square_width, square_height))

        # Y CIRCLE
        pygame.draw.circle(self.window, colors["Y"], (circle_base_x, circle_base_y), circle_radius)

        # X CIRCLE
        pygame.draw.circle(self.window, colors["X"], (circle_base_x + circle_distance, circle_base_y - circle_distance), circle_radius)

        # B CIRCLE
        pygame.draw.circle(self.window, colors["B"], (circle_base_x + circle_distance, circle_base_y + circle_distance), circle_radius)

        # A CIRCLE
        pygame.draw.circle(self.window, colors["Y"], (circle_base_x + circle_distance + circle_distance, circle_base_y), circle_radius)

    # TODO inverse i and j
    def border_observation_area(self, top_left_corner: Point, bottom_right_corner: Point):
        square_size = 20
        x_offset = 600
        y_offset = 50

        for i in range(15):
            for j in range(16):
                pos = (i, j)
                draw_x = j * square_size + x_offset
                draw_y = i * square_size + y_offset

                if top_left_corner.y <= i <= bottom_right_corner.y and bottom_right_corner.x >= j >= top_left_corner.x:
                    pygame.draw.rect(self.window, (255, 0, 0), pygame.Rect(draw_x, draw_y, square_size, square_size), width=1)

    def draw_model_from_tile_map(self, tile_map: {}):
        square_size = 15
        x_offset = 600
        y_offset = 25

        for row in range(15):
            for col in range(16):
                pos = (row, col)
                current_tile = tile_map[pos]
                draw_x = col * square_size + x_offset
                draw_y = row * square_size + y_offset

                self.draw_square_from_tile(current_tile, draw_x, draw_y, square_size)

    # TODO inverse i and j
    # TODO draw observable area around mario, like in mario kart
    def draw_observation_area(self, top_left_corner: Point, bottom_right_corner: Point, tile_map: {}, mario_location: Point):
        square_size = 25
        x_offset = 500
        y_offset = 225

        print(mario_location)
        model_map_from_tile_map(tile_map)

        for i in range(mario_location.x - 5, mario_location.x + 5):
            for j in range(mario_location.y - 5, mario_location.y + 5):

                if (0 <= i <= 16) and (0 <= j <= 15):
                    pos = (i, j)
                    current_tile = tile_map[pos]
                    draw_x = i * square_size + x_offset
                    draw_y = j * square_size + y_offset

                    if top_left_corner.y <= i <= bottom_right_corner.y and bottom_right_corner.x >= j >= top_left_corner.x:
                        self.draw_square_from_tile(current_tile, draw_x, draw_y, square_size)

    def draw_square_from_tile(self, current_tile, draw_x, draw_y, square_size):
        if current_tile == StaticTile.empty:
            pygame.draw.rect(self.window, (53, 81, 92), pygame.Rect(draw_x, draw_y, square_size, square_size))

        elif current_tile == StaticTile.ground:
            pygame.draw.rect(self.window, (155, 103, 60), pygame.Rect(draw_x, draw_y, square_size, square_size))

        elif current_tile == StaticTile.pipe_top1 or current_tile == StaticTile.pipe_top2 \
                or current_tile == StaticTile.pipe_bottom1 or current_tile == StaticTile.pipe_bottom2:
            pygame.draw.rect(self.window, (0, 190, 0), pygame.Rect(draw_x, draw_y, square_size, square_size))

        elif current_tile == EnemyType.goomba:
            pygame.draw.rect(self.window, (255, 64, 64), pygame.Rect(draw_x, draw_y, square_size, square_size))

        elif current_tile == DynamicTile.mario:
            pygame.draw.rect(self.window, (255, 255, 0), pygame.Rect(draw_x, draw_y, square_size, square_size))

        else:
            pygame.draw.rect(self.window, (155, 103, 60), pygame.Rect(draw_x, draw_y, square_size, square_size))

        pygame.draw.rect(self.window, (255, 255, 255), pygame.Rect(draw_x, draw_y, square_size, square_size), width=1)


if __name__ == '__main__':
    game = SuperMarioBros()
    game.run()
