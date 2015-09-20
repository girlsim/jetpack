import pygame
import math
import random

import data
import objects

from helpers import *

########## BASIC RIFLE

class Rifle:

    def __init__(self, player):

        self.projectile = RifleBullet
        self.player = player
        self.max_bullets = 3 # max bullets in air
        self.current_bullets = 0
        self.icon = load_image("rifle-icon.png",-1)

    def fire(self):
        if self.current_bullets < self.max_bullets:
            data.player_projectiles.add(self.projectile(self.player.rect.center,
                                                        self.player.crosshairs.angle,
                                                        self.player, self))
            self.current_bullets += 1
        self.player.firing = False

class RifleBullet(objects.Object):

    def __init__(self, centerPoint, facing, player, weapon):

        objects.Object.__init__(self, centerPoint,
                                [load_image("bullet-1.png"), load_image("bullet-2.png")],
                                self.flyAI, player)

        self.damage = 2
        self.speed = 4
        self.facing = facing
        self.weapon = weapon # the weapon object which fired the bullet

        self.life_counter = 0
        self.life_max = 24 # disappear after a while

    def killSequence(self):
        self.weapon.current_bullets -= 1
        objects.Object.killSequence(self)

    def onHitMonster(self, monster):
        monster.damage(self.damage)
        # knockback is sort of whimpy right now, need to make it better
        monster.knockback(self.xMove/2, self.yMove/2)
        self.killSequence()

    def flyAI(self):

        objects.Object.updateImage(self)
	if self.facing == 0:
	    self.image = pygame.transform.rotate(self.image,180)
	objects.Object.moveWithAngle(self,self.facing,self.speed,False)
        self.rect.move_ip(self.xMove, self.yMove) # ignore walls/etc
        self.life_counter += 1

        self.impactMonster()

        if self.life_counter == self.life_max:
            self.killSequence()

########## FRISBEE

class Frisbee(objects.Object):

    def __init__(self,centerPoint,facing,player):

	objects.Object.__init__(self,centerPoint,[load_image("frisbee-1.png"),load_image("frisbee-2.png"),load_image("frisbee-3.png")],self.thrownAI,player)

	self.damage = 5
	self.max_accel = 12
	self.accel = 0

	self.facing = facing + 1
	self.counter = 0

    def update(self):

	objects.Object.update(self)
	objects.Object.updateImage(self)
	if self.facing == 271:
	    self.image = pygame.transform.rotate(self.image,270)

    def thrownAI(self):

	self.accel = self.max_accel
	objects.Object.moveWithAngle(self,self.facing,self.accel,False)
	self.rect.move_ip(self.xMove,self.yMove)
	self.counter += 1
	if self.counter == self.max_accel:
	    self.currentAI = self.reverseAI

    def reverseAI(self):

	if self.accel > 0:
	    self.accel -= 1
	elif self.accel < 0:
	    self.accel += 1
	else:
	    self.currentAI = self.returnAI
	objects.Object.moveWithAngle(self,self.facing,self.accel,False)

    def returnAI(self):

	if self.accel < self.max_accel:
	    self.accel += 1

	self.rect.move_ip(self.xMove,self.yMove)

	objects.Object.moveWithAngle(self,objects.Object.angleToObject(self,self.player),self.accel,False)

	if self.rect.colliderect(self.player.rect):
	    self.kill()

############# BOTTLE-ROCKET

class Rocket(objects.Object):

    def __init__(self,centerPoint,angle,player):

	objects.Object.__init__(self,centerPoint,[load_image("rocket-1.png",-1),load_image("rocket-2.png",-1),load_image("rocket-3.png",-1),load_image("rocket-4.png",-1),load_image("rocket-3.png",-1),load_image("rocket-2.png",-1)],self.flyAI,player)

	self.damage = 10
	self.max_accel = 8
	self.accel = 0

	self.angle = angle
	self.counter = 0

    def update(self):

	objects.Object.update(self)
	objects.Object.updateImage(self)
	self.image = pygame.transform.rotate(self.image,(self.angle*-1))

    def flyAI(self):

	if self.accel < self.max_accel:
	    self.accel += 1
	objects.Object.moveWithAngle(self,self.angle,self.accel,False)
	for block in data.block_group:
	    if self.rect.colliderect(block.rect):
		self.kill()

	left,right,top,bottom = objects.Object.hittingEdgeOfScreen(self)

	if left or right or top or bottom:
	    self.kill()


############ ALIEN FIREBALL

class Fireball(objects.Object):

    def __init__(self,centerPoint,angle,player):

	objects.Object.__init__(self,centerPoint,[load_image("fireball-1.png",-1),load_image("fireball-2.png",-1)],self.flyAI,player)

	self.damage = 5

	self.speed = 8
	self.angle = angle
	self.counter = 0

    def update(self):

	objects.Object.update(self)
	objects.Object.updateImage(self)
	self.image = pygame.transform.rotate(self.image,(self.angle*-1))

    def flyAI(self):

	objects.Object.moveWithAngle(self,self.angle,self.speed,False)

	if self.rect.colliderect(self.player.rect):
	    self.kill()
	    self.player.health -= self.damage

	left,right,top,bottom = objects.Object.hittingEdgeOfScreen(self)

	if left or right or top or bottom:
	    self.kill()
