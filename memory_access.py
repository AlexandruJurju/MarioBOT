from enum import Enum
from constants import *


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


class SMBMemory:
    pass
