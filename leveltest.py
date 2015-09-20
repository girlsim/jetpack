import pygame

import level
import tiles

from monsters import *

class LevelTest(level.Level):

    def __init__(self):
        spriteSheet = load_image("tiles/tiles-1.png",-1)
        wireImg = grab_sprite(spriteSheet,2,0,1,1)
        bendWireImg = grab_sprite(spriteSheet,3,0,1,1)
        self.tileList = [[[load_image("empty.png",-1)], False],
                         [[grab_sprite(spriteSheet,1,0,1,1)], True],  # wall
                         [[grab_sprite(spriteSheet,0,0,1,1)], False], # table
                         [[wireImg], False],                          # upwards wire
                         [[bendWireImg], False],                      # bending right wire
                         [[grab_sprite(spriteSheet,4,0,1,1)], False], # lamp
                         [[grab_sprite(spriteSheet,0,1,1,1)], False], # end of wire
                         [[grab_sprite(spriteSheet,1,1,1,1)], False], # arrow 1
                         [[grab_sprite(spriteSheet,2,1,1,1)], False], # arrow 2
                         [[pygame.transform.rotate(wireImg,270)], False],      # rightwards wire
                         [[pygame.transform.rotate(wireImg,180)], False],      # downwards wire
                         [[pygame.transform.rotate(bendWireImg,270)], False]]  # bending down wire

        level.Level.__init__(self,"images/maps/test.png")
   # 	self.map = \
   #            [[ 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0 ],
   #             [ 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0 ],
   # 		    [ 1, 1, 4, 9, 9, 9, 9, 9, 9, 9, 11, 1, 1, 1, 1 ],
   # 		    [ 1, 1, 3, 0, 0, 0, 0, 0, 0, 0, 10, 1, 1, 1, 1 ],
   # 		    [ 1, 1, 4, 9, 9, 5, 0, 0, 0, 0, 6, 7, 8, 0, 0 ],
   # 		    [ 1, 1, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
   # 		    [ 1, 1, 3, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0 ],
   # 		    [ 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 ],
   # 		    [ 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 ]]

        self.playerCoords = 5,29
        self.monsterList = [[Holkan,10,29],
                            [Holkan,18,31],
                            [Holkan,26,30],
                            [Holkan,32,10]]
