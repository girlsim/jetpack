import pygame
import math
import random

import data
import objects
import projectiles

from helpers import *

class Holkan(objects.Object):

    def __init__(self, centerPoint, player):

        objects.Object.__init__(self, centerPoint,
                                [pygame.transform.scale(
                    load_image("player/jetpack-hitbox.png",-1),(10,33))],
                                 self.loiterAI, player)
        self.standImages = [load_image("mayan-1.png",-1)]
        self.walkImages = [load_image("mayan-2.png",-1),
                           load_image("mayan-1.png",-1)]
        self.alertImages = [load_image("mayan-alert-1.png",-1)]
        self.attackFImages = [load_image("mayan-spearplant-1.png",-1),
                              load_image("mayan-spearplant-2.png",-1),
                              load_image("mayan-attack-f-1.png",-1),
                              load_image("mayan-attack-f-2.png",-1),
                              load_image("mayan-attack-f-3.png",-1),
                              load_image("mayan-attack-f-4.png",-1),
                              load_image("mayan-attack-f-5.png",-1),
                              load_image("mayan-attack-f-6.png",-1),
                              load_image("mayan-attack-f-7.png",-1),
                              load_image("mayan-attack-f-8.png",-1)]
        self.missFImages = [self.attackFImages[9],
                            self.attackFImages[9],
                            self.attackFImages[9],
                            load_image("mayan-attack-f-blink.png",-1),
                            self.attackFImages[9]]
        self.retractFImages = [self.attackFImages[9],
                               self.attackFImages[8],
                               self.attackFImages[7],
                               self.attackFImages[6],
                               self.attackFImages[5],
                               self.attackFImages[4],
                               self.attackFImages[3],
                               self.attackFImages[2],
                               self.attackFImages[1],
                               self.attackFImages[0]]
	self.impact_damage = 1
        self.health = 8
        self.speed = 1
        self.wander_max = 15
        self.attack_max = 9
        self.retract_max = 19
        self.breather_max = 10
        self.miss_max = 19
        self.vision_radius = 108 # distance the holkan can see
        self.attack_range = 50

        self.monster_image = objects.ObjectImage(self.rect.center, self,
                                                 self.player, self.standImages)
        data.monsterimg_group.add(self.monster_image)

    def update(self):

        objects.Object.update(self)
        objects.Object.basicMovement(self, self.xMove,
                                     self.fall_speed, False)
        objects.Object.impactPlayer(self)

    def spotPlayer(self): # can we see the player?
        dist = math.sqrt((self.player.rect.x - self.rect.x)**2 +
                         (self.player.rect.y - self.rect.y)**2)
        if dist <= self.vision_radius:
            return True
        else:
            return False

            self.currentAI = self.alertAI
            self.xMove = 0
            self.monster_image.frame_speed = 1
            self.monster_image.frame = 0

    def loiterAI(self):
        if self.spotPlayer():
            self.switchAI(self.alertAI, self.alertImages, 1)
        if random.randint(0,10) == 10:
            self.switchAI(self.wanderAI, self.walkImages, 4)
            if random.randint(0,1) == 0:
                self.facing = 0
                self.xMove = self.speed
            else:
                self.facing = 180
                self.xMove = self.speed * -1

    def wanderAI(self):
        if self.spotPlayer():
            self.switchAI(self.alertAI, self.alertImages, 1)
        self.AI_counter += 1
        if self.AI_counter == self.wander_max:
            self.switchAI(self.loiterAI, self.standImages, 1)

    def alertAI(self):
        if (self.player.rect.x > self.rect.x):
            self.facing = 0
        else:
            self.facing = 180
        if not self.spotPlayer():
            self.switchAI(self.loiterAI, self.standImages, 1)
        elif math.fabs(self.player.rect.x - self.rect.x) < self.attack_range:
            self.switchAI(self.attackFAI, self.attackFImages, 1)

    def attackFAI(self):
        self.AI_counter += 1
        if self.AI_counter == self.attack_max:
            self.switchAI(self.missAI, self.missFImages, 4)

    def missAI(self):
        self.AI_counter += 1
        if self.AI_counter == self.miss_max:
            self.switchAI(self.retractFAI, self.retractFImages, 2)

    def retractFAI(self): # failed attack
        self.AI_counter += 1
        if self.AI_counter == self.retract_max:
            self.switchAI(self.breatherAI, self.alertImages, 1)

    def breatherAI(self):
        self.AI_counter += 1
        if self.AI_counter == self.breather_max:
            self.switchAI(self.loiterAI, self.standImages, 1)

class Helicopter(objects.Object):

    def __init__(self,centerPoint,player):

	objects.Object.__init__(self,centerPoint,[load_image("helicopter-1.png",-1),load_image("helicopter-2.png",-1),load_image("helicopter-3.png",-1),load_image("helicopter-4.png",-1)],self.circleAI,player)


	self.angle = 0
	self.angleChange = 15

	self.speed = 6
	self.health = 8

	self.counter = 0
	self.max_counter = random.randint(10,20)
	self.aim_counter = 8

    def update(self):

	objects.Object.update(self)
	objects.Object.updateImage(self)

    def circleAI(self):

	objects.Object.moveWithAngle(self,self.angle,self.speed,True)
	self.angle += self.angleChange
	self.counter += 1
	if self.counter == self.max_counter:
	    self.currentAI = self.aimAI
	    self.counter = 0
	    self.max_counter = random.randint(10,20)

    def aimAI(self):

	self.counter += 1
	if self.counter == self.aim_counter:
	    self.counter = 0
	    self.angle = random.randint(0,359)
	    self.angleChange *= -1
	    self.currentAI = self.circleAI

	    data.monster_projectiles.add(projectiles.Fireball(self.rect.center,objects.Object.angleToObject(self,self.player),self.player))
