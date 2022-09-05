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


def get_mario_location_in_level(ram: np.ndarray):
    # gets mario position with global X and screen Y
    # multiply x with 256 because screen is 256 wide,
    mario_x = ram[player_x_position_in_level] * 256 + ram[player_x_position_on_screen]
    mario_y = ram[player_y_position_within_current_screen_offset]

    return Point[mario_x, mario_y]


def get_mario_location_on_screen(ram: np.ndarray):
    mario_x = ram[player_x_position_within_current_screen_offset]
    mario_y = ram[player_y_position_within_current_screen_offset]

    return Point[mario_x, mario_y]


def get_tile(x, y, ram: np.ndarray):
    page = (x // 256) % 2
    # print(page)
    # print(str((x % 256) // 16))
    sub_x = (x % 256) // 16
    sub_y = (y - 32) // 16

    addr = 0x500 + page * 208 + sub_y * 16 + sub_x

    return ram[addr]


def get_enemy_positions_in_level(ram: np.ndarray):
    enemies = []

    for enemy_count in range(MAX_ENEMIES):
        is_enemy = ram[enemy_drawn + enemy_count]

        if is_enemy:
            enemy_x = ram[enemy_x_position_in_level + enemy_count] * 256 + ram[enemy_x_position_on_screen + enemy_count]

            enemy_y = ram[enemy_y_position_on_screen + enemy_count]

            enemies.append(Point(enemy_x, enemy_y))


def get_tiles(ram: np.ndarray):
    pass
