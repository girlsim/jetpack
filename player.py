import pygame
import math
import random

import data
import objects

from projectiles import *

from helpers import *

class Jetpack(objects.Object):

    def __init__(self, centerPoint):
	self.frame = 0
	self.standImages = [load_image("player/jetpack-stand.png",-1)]
        self.runImages = [load_image("player/jetpack-run-01.png",-1),
                          load_image("player/jetpack-run-02.png",-1),
                          load_image("player/jetpack-run-03.png",-1),
                          load_image("player/jetpack-run-04.png",-1),
                          load_image("player/jetpack-run-05.png",-1),
                          load_image("player/jetpack-run-06.png",-1),
                          load_image("player/jetpack-run-07.png",-1),
                          load_image("player/jetpack-run-08.png",-1),
                          load_image("player/jetpack-run-09.png",-1),
                          load_image("player/jetpack-run-10.png",-1),
                          load_image("player/jetpack-run-11.png",-1),
                          load_image("player/jetpack-run-12.png",-1)]
        self.jumpImages = [load_image("player/jetpack-run.png",-1)]
	self.imageList = [load_image("player/jetpack-hitbox.png",-1)]
	self.image = self.imageList[self.frame]

	objects.Object.__init__(self, centerPoint, self.imageList, None, self)
	self.rect = self.image.get_rect()
	self.rect.center = centerPoint

	self.health = 6
	self.max_health = 6

	self.xMove,self.yMove = 0.0,0.0

        # air movement stuff
	self.max_accel = 4.0
	self.y_accel_rate = 1.0
	self.x_accel_rate = 1.0
	self.x_accel, self.y_accel = 0.0,0.0
	self.airborne = False
        self.wobble = 1 # + = down, - = up
        self.wobble_counter = 0
        self.wobble_max = 5
        self.putt_counter = 0
        self.putt_max = 2

        # ground movement stuff
        self.jump_start = False
        self.g_accel_rate = 1.0
        self.g_max_accel = 3.0
        self.jump_accel = 8.0
        self.g_x_accel = 0.0

        self.running = False

	self.firing = False
	self.weapon_list = [Rifle(self)]
	self.current_weapon = 0

	self.crosshairs = Crosshairs(self.rect.center,self)
	data.crosshairs_group = pygame.sprite.RenderPlain((self.crosshairs))

        self.monster_image = objects.ObjectImage(self.rect.center, self, self,
                                                [load_image("player/jetpack-stand.png",-1)]
                                                )
        data.playerimg_group = pygame.sprite.RenderPlain((self.monster_image))

    def update(self):


	self.updateAccel()
	self.handleFire()

        if self.airborne:
            self.putt_counter += 1
            if self.putt_counter == self.putt_max:
                self.putt_counter = 0
                putt = Putt(self.rect.center,self)
                data.anims_group.add(putt)

        objects.Object.basicMovement(self, self.xMove, self.yMove + self.wobble,
                                     True)

        if self.falling:
            self.monster_image.imageList = self.jumpImages
            self.monster_image.frame_speed = 1
            self.monster_image.frame = 0
        elif not self.running and self.xMove != 0 or self.running and self.monster_image.imageList == self.jumpImages:
            self.running = True
            self.monster_image.imageList = self.runImages
            self.monster_image.frame_speed = 2
            self.monster_image.frame = 0
        elif self.xMove == 0:
            self.running = False
            self.monster_image.imageList = self.standImages
            self.monster_image.frame_speed = 1
            self.monster_image.frame = 0
        else:
            objects.Object.updateImage(self);


    def handleFire(self):

	if self.firing:
            self.weapon_list[self.current_weapon].fire()

    def updateAccel(self):

        if self.airborne == True:
            self.xMove += self.x_accel
            self.yMove += self.y_accel

            if self.xMove > self.max_accel:
                self.xMove = self.max_accel
            elif self.xMove < -self.max_accel:
                self.xMove = -self.max_accel

            if self.yMove > self.max_accel:
                self.yMove = self.max_accel
            elif self.yMove < -self.max_accel:
                self.yMove = -self.max_accel

            if self.x_accel == 0: # airbreak
                self.xMove = self.xMove / 1.2
                if self.xMove > 0 and self.xMove < 0.25:
                    self.xMove = 0.0
                if self.xMove < 0 and self.xMove > -0.25:
                    self.xMove = 0.0
            if self.y_accel == 0:
                self.yMove = self.yMove / 1.2
                if self.yMove > 0 and self.yMove < 0.25:
                    self.yMove = 0.0
                if self.yMove < 0 and self.yMove > -0.25:
                    self.yMove = 0.0

            self.wobble_counter += 1
            if self.wobble_counter == self.wobble_max:
                self.wobble_counter = 0
                self.wobble = -self.wobble

        else: # not airborne

            if self.jump_start:
                if not self.falling:
                    self.falling = True
                    self.fall_speed = -self.jump_accel

            self.xMove += self.g_x_accel
            self.yMove = self.fall_speed

            if self.xMove > self.g_max_accel:
                self.xMove = self.g_max_accel
            elif self.xMove < -self.g_max_accel:
                self.xMove = -self.g_max_accel

            if self.g_x_accel == 0:
                self.xMove = self.xMove / 1.6
                if self.xMove > 0 and self.xMove < 0.25:
                    self.xMove = 0.0
                if self.xMove < 0 and self.xMove > -0.25:
                    self.xMove = 0.0

    def commandKeyDown(self, key):
	if (key == data.keys[0]):
            if self.airborne:
                self.x_accel += self.x_accel_rate
            else:
                self.g_x_accel += self.g_accel_rate
	    self.facing = 0
	elif (key == data.keys[1]):
            if self.airborne:
                self.x_accel += -self.x_accel_rate
            else:
                self.g_x_accel += -self.g_accel_rate
	    self.facing = 180
	elif (key == data.keys[2]):
            if self.airborne:
                self.y_accel += -self.y_accel_rate
        elif (key == data.keys[3]):
            if self.airborne:
                self.y_accel += self.y_accel_rate
	elif (key == data.keys[4]):
		self.firing = True
        elif (key == data.keys[5]):
            if not self.falling and not self.airborne:
                self.jump_start = True
	elif (key == data.keys[6]):
	    self.current_weapon -= 1
	    if self.current_weapon < 0:
		self.current_weapon = len(self.weapon_list)-1
	elif (key == data.keys[7]):
	    self.current_weapon += 1
	    if self.current_weapon >= len(self.weapon_list):
		self.current_weapon = 0
	# else: needs object interaction

    def commandKeyUp(self, key):
	if (key == data.keys[0]):
            if self.airborne:
                self.x_accel += -self.x_accel_rate
            else:
                self.g_x_accel += -self.g_accel_rate
	elif (key == data.keys[1]):
            if self.airborne:
                self.x_accel += self.x_accel_rate
            else:
                self.g_x_accel += self.g_accel_rate
        elif (key == data.keys[2]):
            if self.airborne:
                self.y_accel += self.y_accel_rate
        elif (key == data.keys[3]):
            if self.airborne:
                self.y_accel += -self.y_accel_rate
        elif (key == data.keys[5]):
            if not self.airborne:
                self.jump_start = False

class Crosshairs(objects.Object):

    def __init__(self,centerPoint,player):

	self.visibleImages = [load_image("crosshairs.png",-1)]
	self.invisibleImages = [load_image("empty.png",-1)]
	objects.Object.__init__(self,centerPoint,self.invisibleImages,self.crosshairAI,player)

	self.visible = False
	self.angle = 0
	self.angleChange = 0

    def update(self):

	objects.Object.update(self)
	objects.Object.updateImage(self)
	self.image = pygame.transform.rotate(self.image,(self.angle*-1))

    def crosshairAI(self):

	if self.visible:
	    self.imageList = self.visibleImages
	    self.angle += self.angleChange
	else:
	    self.imageList = self.invisibleImages
	    self.angle = self.player.facing

	self.rect.center = self.player.rect.center
	self.rect.y -= 9

class Putt(objects.Object):

    def __init__(self,centerPoint,player):

        self.images = [load_image("putt-1.png",-1),
                       load_image("putt-1.png",-1), load_image("putt-2.png",-1),
                       load_image("putt-3.png",-1), load_image("putt-4.png",-1),
                       load_image("putt-5.png",-1), load_image("putt-6.png",-1)]
        objects.Object.__init__(self,centerPoint,self.images,self.puttAI,player)
        if self.player.x_accel == 0 and self.player.y_accel == 0: # hovering
            self.yMove = 4

    def puttAI(self):

        self.rect.y += self.yMove
        self.updateImage()
        if self.frame == 0:
            self.kill()
        
