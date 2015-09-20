import pygame

import data

from helpers import *

class Display:

    def __init__(self):

	self.inited = True

    def updateAll(self):

	data.text_group.update()
	data.block_group.update()
        data.anims_group.update()
	data.player_group.update()
        data.playerimg_group.update()
	data.monster_group.update()
        data.monsterimg_group.update()
	data.player_projectiles.update()
	data.monster_projectiles.update()
	data.crosshairs_group.update()

#    def drawGroup(self, group):

#        for object in group:
#            data.bg_surface.blit(object.image, object.rect.center)

    def drawAll(self):
        
	pygame.display.flip()
	data.screen.fill((42,40,45))
        data.bg_surface.fill((42,40,45))
	data.block_group.draw(data.bg_surface)
        data.anims_group.draw(data.bg_surface)
	data.monster_group.draw(data.bg_surface)
        data.monsterimg_group.draw(data.bg_surface)
	data.player_projectiles.draw(data.bg_surface)
	data.monster_projectiles.draw(data.bg_surface)
	data.player_group.draw(data.bg_surface)
        data.playerimg_group.draw(data.bg_surface)
	data.crosshairs_group.draw(data.bg_surface)
	data.text_group.draw(data.bg_surface)
        data.screen.blit(data.bg_surface,(data.bgs_x,data.bgs_y))
        data.screen.blit(data.player.weapon_list[data.player.current_weapon].icon,
                         (18,9))
        hearts_num = data.player.max_health / 2
        while hearts_num > 0:
            data.screen.blit(load_image("heart-container.png",-1),
                             (42+12*hearts_num,18))
            hearts_num -= 1
        hearts_num = data.player.health
        while hearts_num > 0:
            if hearts_num % 2 == 0:
                data.screen.blit(load_image("heart-r.png",-1),
                                 (42+6*hearts_num,18))
            else:
                data.screen.blit(load_image("heart-l.png",-1),
                                 (42+6*(hearts_num+1),18))
            hearts_num -= 1
