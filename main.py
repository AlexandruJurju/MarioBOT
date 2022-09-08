import retro
import pygame

from memory_access import *

from ai.mario_bot import MarioBot
from ai.genetic_algorithm import *
from ai.neural_network import NeuralNetwork

player_action = [0, 0, 0, 0, 0, 0, 0, 0, 0]
bot_action = [0, 0, 0, 0, 0, 0, 0, 0, 0]


class SuperMarioBros:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("SMB")

        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        self.fps_clock = pygame.time.Clock()
        self.running = True

        self.env = retro.make(game='SuperMarioBros-Nes', state='Level1-1')
        self.env.reset()

        print(self.env.buttons)

    def process_events(self):
        global player_action
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                if event.key == pygame.K_UP:
                    player_action = [1, 0, 0, 0, 0, 0, 0, 0, 1]
                if event.key == pygame.K_RIGHT:
                    player_action = [1, 0, 0, 0, 0, 0, 0, 1, 0]
                if event.key == pygame.K_LEFT:
                    player_action = [1, 0, 0, 0, 0, 0, 1, 0, 0]
                if event.key == pygame.K_r:
                    self.env.reset()

    def run(self):
        global bot_action
        bot = MarioBot(NeuralNetwork(NN_CONFIG))
        bot.brain.init_random_neural_net()

        while self.running:
            self.window.fill(WHITE)
            # self.process_events()
            print(bot_action)

            observation, reward, done, info = self.env.step(bot_action)
            ram = self.env.get_ram()
            full_tile_map = get_tiles(ram)

            active_tile_map = self.get_active_model_view(full_tile_map, ram)

            bot_action = bot.step(model_map_from_tile_map(active_tile_map), ram)

            self.redraw_windows(observation, full_tile_map, active_tile_map)

            self.fps_clock.tick(MAX_FPS)

    def redraw_windows(self, observation, tile_map, active_tile_map):
        # emulator game window
        self.draw_emulator_window(observation)

        # main model
        self.draw_model_view(tile_map, 550, 25, 15)

        # minimal view
        self.draw_model_view(active_tile_map, 550, 300, 15)
        self.draw_highlight_model_view(active_tile_map, 550, 25, 15)

        pygame.display.update()

    def get_active_model_view(self, tile_map, ram):
        if get_mario_model_location(ram).x < 7:
            active_tile_map = self.get_dynamic_model_view(tile_map, get_mario_model_location(ram))
        else:
            active_tile_map = self.get_static_model_view(tile_map, Point(7, 4), Point(13, 13))
        return active_tile_map

    def draw_emulator_window(self, rgb_array):
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

    def draw_tile_from_from_tile_map(self, current_tile, x_position, y_position, square_size):
        if current_tile == StaticTile.empty:
            pygame.draw.rect(self.window, (53, 81, 92), pygame.Rect(x_position, y_position, square_size, square_size))

        elif current_tile == StaticTile.ground:
            pygame.draw.rect(self.window, (155, 103, 60), pygame.Rect(x_position, y_position, square_size, square_size))

        elif current_tile == StaticTile.pipe_top1 or current_tile == StaticTile.pipe_top2 \
                or current_tile == StaticTile.pipe_bottom1 or current_tile == StaticTile.pipe_bottom2:
            pygame.draw.rect(self.window, (0, 190, 0), pygame.Rect(x_position, y_position, square_size, square_size))

        elif current_tile == EnemyType.goomba:
            pygame.draw.rect(self.window, (255, 64, 64), pygame.Rect(x_position, y_position, square_size, square_size))

        elif current_tile == DynamicTile.mario:
            pygame.draw.rect(self.window, (255, 255, 0), pygame.Rect(x_position, y_position, square_size, square_size))

        else:
            pygame.draw.rect(self.window, (155, 103, 60), pygame.Rect(x_position, y_position, square_size, square_size))

        pygame.draw.rect(self.window, (255, 255, 255), pygame.Rect(x_position, y_position, square_size, square_size), width=1)

    def get_static_model_view(self, tile_map: {}, top_left_corner: Point, bottom_right_corner: Point):
        static_tile_map = {}
        for row in range(15):
            for col in range(16):
                if top_left_corner.y <= row <= bottom_right_corner.y and bottom_right_corner.x >= col >= top_left_corner.x:
                    static_tile_map[(row, col)] = tile_map[(row, col)]

        return static_tile_map

    def get_dynamic_model_view(self, tile_map: {}, mario_location: Point):
        dynamic_tile_map = {}
        for row in range(mario_location.y - UP_VIEW, mario_location.y + DOWN_VIEW + 1):
            for col in range(mario_location.x - LEFT_VIEW, mario_location.x + RIGHT_VIEW + 1):
                # if within model matrix
                if (0 <= row < 15) and (0 <= col < 16):
                    pos = (row, col)
                    dynamic_tile_map[pos] = tile_map[pos]

        return dynamic_tile_map

    def draw_model_view(self, tile_map: {}, x_offset, y_offset, square_size):
        for row in range(15):
            for col in range(16):
                pos = (row, col)
                draw_x = col * square_size + x_offset
                draw_y = row * square_size + y_offset

                if pos in tile_map:
                    current_tile = tile_map[pos]
                    self.draw_tile_from_from_tile_map(current_tile, draw_x, draw_y, square_size)
                else:
                    pygame.draw.rect(self.window, (128, 128, 128), pygame.Rect(draw_x, draw_y, square_size, square_size), width=3)

    def draw_highlight_model_view(self, tile_map: {}, x_offset, y_offset, square_size):
        for row in range(15):
            for col in range(16):
                pos = (row, col)
                draw_x = col * square_size + x_offset
                draw_y = row * square_size + y_offset

                if pos in tile_map:
                    pygame.draw.rect(self.window, (24, 115, 204), pygame.Rect(draw_x, draw_y, square_size, square_size), width=2)

    # TODO draw neural network
    def draw_neural_network(self):
        pass


if __name__ == '__main__':
    game = SuperMarioBros()
    game.run()
