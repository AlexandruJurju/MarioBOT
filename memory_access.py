import typing
from enum import Enum
from collections import namedtuple
import numpy as np

from constants import *

Point = namedtuple('Point', ['x', 'y'])


class EnemyType(Enum):
    green_koopa1 = 0x00
    red_koopa1 = 0x01
    buzzy_beetle = 0x02
    red_koopa2 = 0x03
    green_koopa2 = 0x04
    hammer_brother = 0x05
    goomba = 0x06
    blooper = 0x07
    bullet_bill = 0x08
    green_koopa_paratroopa = 0x09
    grey_cheep_cheep = 0x0A
    red_cheep_cheep = 0x0B
    pobodoo = 0x0C
    piranha_plant = 0x0D
    green_paratroppa_jump = 0x0E
    bowser_flame1 = 0x10
    lakitu = 0x11
    spiny_egg = 0x13
    fly_cheep_cheep = 0x14
    bowser_flame2 = 0x15


class StaticTile(Enum):
    empty = 0x00
    fake = 0x01
    ground = 0x54
    pipe_top1 = 0x12
    pipe_top2 = 0x13
    pipe_bottom1 = 0x14
    pipe_bottom2 = 0x15
    flagpole_top = 0x24
    flagpole = 0x25
    coin_block1 = 0xC0
    coin_block2 = 0xC1
    coin = 0xC2
    breakable_block = 0x51


class DynamicTile(Enum):
    mario = 0xAA
    static_lift1 = 0x24
    static_lift2 = 0x25
    vertical_lift1 = 0x26
    vertical_lift2 = 0x27
    horizontal_lift = 0x28
    falling_static_lift = 0x29
    horizontal_moving_lift = 0x2A
    double_lift1 = 0x2B
    double_lift2 = 0x2C
    vine = 0x2F
    flagpole = 0x30
    start_flag = 0x30
    star_flag = 0x31
    jump_spring = 0x32
    warpzone = 0x34


# Super Mario Bros can have 5 enemies max on screen, most enemy variables go from base_address to base_address+4, one address for each enemy

# enemy X position in level contains the index of the 256 wide square that the enemy is currently standing on
# to get enemy level X = enemy_x_position_in_level * + enemy_x_position_on_screen
# 0x006E-0x0072	, 5 enemies max , first enemy address starts at 0x06E
enemy_x_position_in_level = 0x006E
# 5 enemies from 0x87 to 0x8B 0x0087/B
enemy_x_position_on_screen = 0x0087
# 0x03AE-0x03B2
enemy_x_position_within_current_screen_offset = 0x03AE

# Enemy y pos on screen (multiply with value at 0x00B6/A to get level y pos)
enemy_y_position_on_screen = 0x00CF
# 0x03B9/D
enemy_y_position_within_current_screen_offset = 0x03B9

# Enemy hitboxes (5x4 bytes, <<x1,y1> <x2,y2>>)
# multiply enemy_x = ram[base + enemy_count * 4]
# each hitbox contains coordinates for top-left and bottom-right corner
# TODO enemy pos with hitboxes
enemy_hitbox_base = 0x04B0

# 0x000F-0x0013 , bool if enemy is drawn on screen
enemy_drawn = 0x000F
enemy_type = 0x0016

# 1-right 2-left
player_direction = 0x0003
# 1-right 2-left
player_moving_direction = 0x0045

# player position in level contains the number of 256 units traveled in X direction
# to get level player X  ->  player_x_position_in_level * 256 + player_x_position_on_screen
player_x_position_in_level = 0x006D
player_x_position_on_screen = 0x0086
player_x_position_within_current_screen_offset = 0x03AD

# Player Y pos on screen (multiply with value at 0x00B5 to get level y pos)
# level Y position isn't needed, local Y is good enough
player_y_position_on_screen = 0x00CE
player_y_position_within_current_screen_offset = 0x03B8

# Player vertical screen position viewport = 1 | above viewport = 0 | anywhere below viewport is >1
player_vertical_screen_position = 0x00B5

# Player hitbox (1x4 bytes, <<x1,y1> <x2,y2>>)
# TODO get player position with hitboxes
player_hitbox = 0x04AC


def get_mario_level_location(ram: np.ndarray) -> Point:
    # gets mario position with global X and screen Y
    # multiply x with 256 because screen is 256 wide,
    mario_x = ram[player_x_position_in_level] * 256 + ram[player_x_position_on_screen]
    mario_y = ram[player_y_position_within_current_screen_offset]

    return Point(mario_x, mario_y)


def get_mario_screen_location(ram: np.ndarray):
    mario_x = ram[player_x_position_within_current_screen_offset]
    mario_y = ram[player_y_position_within_current_screen_offset] * ram[player_vertical_screen_position] + 16

    return Point(mario_x, mario_y)


def get_enemies_level_locations(ram: np.ndarray) -> typing.List:
    enemies = []

    for enemy_count in range(MAX_ENEMIES):
        is_enemy = ram[enemy_drawn + enemy_count]

        if is_enemy:
            enemy_x = ram[enemy_x_position_in_level + enemy_count] * 256 + ram[enemy_x_position_on_screen + enemy_count]

            enemy_y = ram[enemy_y_position_on_screen + enemy_count]

            enemies.append(Point(enemy_x, enemy_y))
    return enemies


def get_enemies_screen_locations(ram: np.ndarray):
    enemies = []

    for enemy_count in range(MAX_ENEMIES):
        is_enemy = ram[enemy_drawn + enemy_count]

        if is_enemy:
            enemy_x = ram[enemy_x_position_on_screen + enemy_count]

            enemy_y = ram[enemy_y_position_on_screen + enemy_count]

            enemies.append(Point(enemy_x, enemy_y))

    return enemies


def get_address_from_coordinates(x, y):
    page = (x // 256) % 2
    sub_x = (x % 256) // 16
    sub_y = (y - 32) // 16
    address = 0x500 + page * 208 + sub_y * 16 + sub_x
    return address


def get_tile(x, y, ram: np.ndarray):
    address = get_address_from_coordinates(x, y)
    return ram[address]


# TODO better get_tiles function
# TODO inverse i and j
def get_tiles(ram: np.ndarray):
    tile_map = {}
    row = 0
    col = 0

    mario_level_position = get_mario_level_location(ram)
    mario_screen_position = get_mario_screen_location(ram)
    enemies = get_enemies_level_locations(ram)

    start_x = mario_level_position.x - mario_screen_position.x

    for y in range(0, 240, 16):
        for x in range(start_x, start_x + 256, 16):
            pos = (row, col)
            tile = get_tile(x, y, ram)

            if row < 2:
                tile_map[pos] = StaticTile.empty
            else:
                tile_map[pos] = StaticTile.empty

                for static_tile in StaticTile:
                    if static_tile.value == tile:
                        tile_map[pos] = static_tile

                for dynamic_tile in DynamicTile:
                    if dynamic_tile.value == tile:
                        tile_map[pos] = dynamic_tile

                for enemy in enemies:
                    model_x = (enemy.x - start_x) // 16 + 1
                    model_y = enemy.y // 16 + 1
                    tile_map[(model_y, model_x)] = EnemyType.goomba

                mario_model_position = get_mario_model_location(ram)
                tile_map[mario_model_position] = DynamicTile.mario

            col += 1
        col = 0
        row += 1
    return tile_map


# TODO inverse Y AND X !!!!!!
def get_mario_model_location(ram: np.ndarray):
    mario_level_position = get_mario_level_location(ram)
    mario_screen_position = get_mario_screen_location(ram)

    mario_model_x = mario_screen_position.x // TILE_SIZE + 1
    mario_model_y = mario_level_position.y // TILE_SIZE + 1

    return Point(mario_model_y, mario_model_x)


def model_map_from_tile_map(tile_map: {}):
    model = np.zeros((15, 16))

    for i in range(15):
        for j in range(16):
            pos = (i, j)
            current_tile = tile_map[pos]

            if current_tile == StaticTile.empty:
                model[i][j] = 0
            if current_tile == StaticTile.ground:
                model[i][j] = 1
            if current_tile == EnemyType.goomba:
                model[i][j] = -1

            print(model[i][j], end=" ")
        print()
    print()
