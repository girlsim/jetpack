import pygame
import math
import random

import data

class Object(pygame.sprite.Sprite):

    def __init__(self,centerPoint,imageList,activeAI,player):
	self.player = player
	self.imageList = imageList
	self.frame = 0
        self.frame_speed = 1 # see image function for clarification
	self.image = self.imageList[self.frame/self.frame_speed]
	
	pygame.sprite.Sprite.__init__(self)
	self.rect = self.image.get_rect()
	self.rect.center = centerPoint
	
	self.impact_damage = 0
	self.dying = False
        self.falling = False
        self.fall_speed = 0
        self.facing = 0
	self.xMove,self.yMove = 0,0
        self.monster_image = None
        self.AI_counter = 0

	self.currentAI = activeAI

    def update(self):

	    self.currentAI()

    def impactPlayer(self):

        if (self.rect.colliderect(self.player.rect)):
            self.player.damage(self.impact_damage)
            # todo: need to make this actually work........
            # todo todo: need to figure out why I thought this wasn't working
            if (self.rect.x > self.player.rect.x):
                self.player.knockback(-3, -3)
            else:
                self.player.knockback(3, -3)

    def impactMonster(self):
        for mob in data.monster_group:
            if self.rect.colliderect(mob.rect):
                self.onHitMonster(mob)                

    def onHitMonster(self, monster):
        pass

    def damage(self, amount):
        self.health -= amount
        if self.health < 0:
            self.health = 0
        self.dying = True
        # TODO: DIE
        data.text_group.add(Text(self.rect.center,
                        "-" + str(amount), (255,40,40)))
        # todo: different colors for monsters/player?
            
    def knockback(self, x, y):
        self.xMove += x
        self.yMove += y
        

    def updateImage(self):

	self.image = self.imageList[self.frame/self.frame_speed]
	self.frame += 1
	if self.frame >= len(self.imageList) * self.frame_speed:
	    self.frame = 0

    def killSequence(self):
        self.kill()

    def switchAI(self, currentAI, imageList, frame_speed):

        self.xMove = 0
        self.monster_image.frame_speed = frame_speed
        self.monster_image.frame = 0
        self.monster_image.imageList = imageList
        self.currentAI = currentAI
        self.AI_counter = 0

    def basicMovement(self,x_move,y_move,move_screen): # same movement as player

        if self.falling:
            self.fall_speed += data.gravity
            if self.fall_speed > data.terminal_velocity:
                self.fall_speed = data.terminal_velocity
        else:
            self.fall_speed = 0

	self.rect.x += x_move
        if move_screen:
            x,y = self.rect.center
            x += data.bgs_x
            if x < data.screen_padding and x_move < 0:
                data.bgs_x -= x_move
            elif x > data.screen_width - data.screen_padding and x_move > 0:
                data.bgs_x -= x_move

	for block in data.block_group:
	    if self.rect.colliderect(block.rect):
		if self.rect.y - 36 <= block.rect.y:
		    if x_move > 0:
			self.rect.right = block.rect.left
		    elif x_move < 0:
			self.rect.left = block.rect.right

	self.rect.y += y_move
        self.falling = True
        if move_screen:
            x,y = self.rect.center
            y += data.bgs_y
            if y < data.screen_padding and y_move:
                data.bgs_y -= y_move
            elif y > data.screen_height - data.screen_padding and y_move:
                data.bgs_y -= y_move

	for block in data.block_group:
	    if self.rect.colliderect(block.rect):
		if self.rect.x - 36 <= block.rect.x and self.rect.x + 36 >= block.rect.x:
		    if y_move > 0:
			self.rect.bottom = block.rect.top
                        self.falling = False
                    elif y_move < 0:
                        self.rect.top = block.rect.bottom
                        self.yMove = 0
                        self.fall_speed = 0

    def moveWithAngle(self,angle,speed,stopAtBlocks):

	rotation = (math.pi / 180) * angle
	self.xMove = math.cos(rotation) * speed
	self.yMove = math.sin(rotation) * speed
	if stopAtBlocks:
	    self.rect.x += self.xMove
	    for block in data.block_group:
		if self.rect.colliderect(block.rect):

		    if self.xMove > 0:
			self.rect.right = block.rect.left
		    if self.xMove < 0:
			self.rect.left = block.rect.right
	    self.rect.y += self.yMove
	    for block in data.block_group:
		if self.rect.colliderect(block.rect):
		    if self.yMove > 0:
			self.rect.bottom = block.rect.top
		    if self.yMove < 0:
			self.rect.top = block.rect.bottom
	else:
	    self.rect.move_ip(self.xMove,self.yMove)

    def angleToObject(self,object):

	vector = Vector.from_points(self.rect.center,object.rect.center)
	vector.normalize()
	angle = math.atan2(vector.y,vector.x)
	angle *= 180 / math.pi
	return angle

    def hittingEdgeOfScreen(self):

	left,right,top,bottom = False,False,False,False

	if self.rect.x < 0:
	    left = True
	elif self.rect.x > data.screen_width:
	    right = True
	if self.rect.y < 0:
	    top = True
	elif self.rect.y > data.screen_height:
	    bottom = True

	return left,right,top,bottom

class Vector: # With apologies to mister McGugan. I'm sure he doesn't mind.

    def __init__(self, x=0.0, y=0.0):
	self.x = x
	self.y = y

    @classmethod
    def from_points(cls,pa,pb):
	return cls(pb[0]-pa[0],pb[1]-pa[1])

    def get_magnitude(self):
	return math.sqrt(self.x**2 + self.y**2)

    def normalize(self):
	magnitude = self.get_magnitude()
	if self.x != 0:
	    self.x /= magnitude
	if self.y != 0:
	    self.y /= magnitude

class ObjectImage(Object):

    def __init__(self, centerPoint, master, player, images):

        self.images = images
        self.master = master
        Object.__init__(self, centerPoint, self.images,
                                self.imgAI, player)

    def update(self):

        Object.updateImage(self)
        Object.update(self)

    def imgAI(self):

        self.updateImages()
        self.rect.center = self.master.rect.center

    def updateImages(self):
	self.image = self.imageList[self.frame/self.frame_speed]
	if self.master.facing == 180 or self.master.xMove < 0:
	    self.image = pygame.transform.flip(self.image, True, False)

class Text(pygame.sprite.Sprite):

    def __init__(self,centerPoint,text,color):
        pygame.sprite.Sprite.__init__(self)
        if pygame.font:
            font = pygame.font.Font(None, 12)
        self.image = font.render(text
                                       , 1, color)
        self.rect = self.image.get_rect()
        x,y = centerPoint
        self.rect.x = x
        self.rect.y = y

        self.stored_y = self.rect.y
        self.bounce = random.randint(-6,-3)
        self.slide = random.randint(-3,3)
        self.going = "up"

        self.death_counter = 0
        self.death_max = 40
	self.dead = False

    def update(self):

        self.rect.x += self.slide
	if not self.dead:
            for block in data.block_group:
                if self.rect.colliderect(block.rect):
                    if self.rect.y - 36 <= block.rect.y:
                        if self.slide > 0:
                            self.rect.right = block.rect.left
                        elif self.slide < 0:
                            self.rect.left = block.rect.right
		        self.slide = -self.slide

        self.rect.y += self.bounce
	if not self.dead:
            for block in data.block_group:
                if self.rect.colliderect(block.rect):
                    if self.rect.x - 36 <= block.rect.x and self.rect.x + 36 >= block.rect.x:
                        if self.bounce > 0:
                            self.rect.bottom = block.rect.top
                        elif self.bounce < 0:
                            self.rect.top = block.rect.bottom
		        self.bounce = -self.bounce * .80

	self.bounce += data.gravity
	if self.bounce > data.terminal_velocity:
	    self.bounce = data.terminal_velocity

        self.death_counter += 1
        if self.death_counter >= self.death_max:
            self.dead = True

        self.image.set_alpha((100-self.death_counter))
