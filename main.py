import pygame

from pygame.locals import *

import data
import player
import display
import monsters
import tiles
import worlds

from helpers import *

class Main:

    def __init__(self):
        pygame.init()
        data.screen = pygame.display.set_mode((data.screen_width,data.screen_height))
        data.text_group = pygame.sprite.Group()
        data.player = player.Jetpack((250,450))
        data.player_group = pygame.sprite.RenderPlain((data.player))
        data.player_projectiles =pygame.sprite.Group()
        data.monster_group = pygame.sprite.Group()
        data.monster_projectiles = pygame.sprite.Group()
        data.block_group = pygame.sprite.Group() # group for obstructing tiles
        #  data.tiles_group = pygame.sprite.Group() # group for background tiles
        data.anims_group = pygame.sprite.Group()
        data.monsterimg_group = pygame.sprite.Group()
        self.world = worlds.TestWorld()
        self.level = self.world.levels[0]()
        data.bg_surface = pygame.Surface(((data.tile_size+1)*len(self.level.map[0]),
                                          (data.tile_size+1)*len(self.level.map)))
        self.display = display.Display()
        data.display = self.display
        self.loadLevel()

    def gameLoop(self):
        while data.game_running:
            pygame.time.wait(data.ms_per_refresh)
            data.rounds_passed += 1
            pygame.event.pump()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == KEYDOWN:
                    data.player.commandKeyDown(event.key)
                elif event.type == KEYUP:
                    data.player.commandKeyUp(event.key)
            self.display.updateAll()
            self.display.drawAll()

    def loadLevel(self):
        x,y = 0,0
        while y < len(self.level.map):
            x = 0
            while x < len(self.level.map[y]):
                index = self.level.tileList[self.level.map[y][x]]
                tile = tiles.Tile((x*(data.tile_size+1)+data.tile_size/2,
                                   y*(data.tile_size+1)+data.tile_size/2),
                                  index[0], index[1])
                #       tile = self.level.tileList[self.level.map[y][x]](
                #                    (x*36+18,y*36+18))
                if tile.wall:
                    data.block_group.add(tile)
                else:
                    data.anims_group.add(tile)
                x += 1
            y += 1
        x,y = self.level.playerCoords
        data.player.rect.x = x*data.tile_size
        data.player.rect.y = y*data.tile_size
        self.centerOnPlayer()
        for monster in self.level.monsterList:
            data.monster_group.add(monster[0]((monster[1]*data.tile_size,
                                               monster[2]*data.tile_size),
                                              data.player))

    def centerOnPlayer(self):
        data.bgs_x = data.screen_width / 2 - data.player.rect.x
        data.bgs_y = data.screen_height / 2 - data.player.rect.y

if __name__ == "__main__":
    MainWindow = Main()
    MainWindow.gameLoop()
