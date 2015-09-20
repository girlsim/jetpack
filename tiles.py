import pygame

from helpers import *

class Tile(pygame.sprite.Sprite):

    def __init__(self,centerPoint,imageList,wall):
	self.imageList = imageList
	self.frame = 0
	self.image = imageList[self.frame]
	pygame.sprite.Sprite.__init__(self)
	self.rect = self.image.get_rect()
	self.rect.center = centerPoint

	self.wall = wall
        self.spawn = False

    def update(self):
	self.image = self.imageList[self.frame]
	self.frame += 1
	if self.frame >= len(self.imageList):
	    self.frame = 0

class StoneWall(Tile):

    def __init__(self,centerPoint):
	imageList = [load_image("stonewall.png")]
	Tile.__init__(self,centerPoint,imageList,True)

class Empty(Tile):

    def __init__(self,centerPoint):
	imageList = [load_image("empty.png",-1)]
	Tile.__init__(self,centerPoint,imageList,False)
