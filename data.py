from pygame.locals import *

display = None

screen = None
screen_width = 720
screen_height = 540
bg_surface = None
bgs_x = 0
bgs_y = 0
screen_padding = 180
tile_size = 18

ms_per_refresh = 10
rounds_passed = 0

game_running = True

keys = [K_RIGHT, K_LEFT, K_UP, K_DOWN, K_z, K_x, K_a, K_s]

text_group = None
player = None
player_group = None
crosshairs_group = None
player_projectiles = None
monster_group = None
monster_projectiles = None
block_group = None
anims_group = None
playerimg_group = None
monsterimg_group = None

gravity = 0.5
terminal_velocity = 8.0
