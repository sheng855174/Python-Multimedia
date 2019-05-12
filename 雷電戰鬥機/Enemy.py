import pygame
import random
from pygame.locals import *

class Enemy(pygame.sprite.Sprite):
	sheet = None;
	speed = 1;
	x = 0;
	start_ticks = 0;
	dead = False;
	def __init__(self,surface,rect):
		super().__init__();
		self.surface = surface;
		self.rect = rect;
		self.sheet = pygame.image.load("./res/img/enemy.png").convert();
		self.speed = random.randint(1, 5);
		self.x = random.randint(-1, 1);

	def update(self):
		seconds = (pygame.time.get_ticks()-self.start_ticks)/1000;
		if self.dead and seconds>1:#復活
			self.sheet = pygame.image.load("./res/img/enemy.png").convert();
			self.rect.y = 0;
			self.rect.x = random.randint(0,self.surface.get_width());
			self.speed = random.randint(1, 5);
			self.dead = False;
		self.rect.move_ip(self.x,self.speed)#top to bottom
		#限制範圍
		if not self.dead:
			if self.rect.left < 0:
				self.die();
			elif self.rect.right > self.surface.get_width():
				self.die();
			if self.rect.top <= 0:
				self.die();
			elif self.rect.bottom >= self.surface.get_height():
				self.die();

	def die(self):
		self.dead = True;
		self.sheet = pygame.image.load("./res/img/boom.jpg").convert();
		self.speed = 0;
		self.start_ticks = pygame.time.get_ticks();


	def draw(self):
		self.surface.blit(self.sheet,self.rect);
