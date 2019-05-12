import pygame
from pygame.locals import *

class Bullet(pygame.sprite.Sprite):
	sheet = None;
	speed = 10;
	used = False;
	def __init__(self,surface,rect):
		super().__init__();
		self.surface = surface;
		self.rect = rect;
		self.sheet = pygame.image.load("./res/img/bullet.png").convert();

	def isUsed(self):
		return self.used;

	def setUsed(self,used,x,y):
		self.used = used;
		self.rect.x = x;
		self.rect.y = y;

	def update(self):
		if self.used:
			self.rect.move_ip(0,-self.speed)#bottom to top
		#限制範圍
		if self.rect.left < 0:
			self.die();
		elif self.rect.right > self.surface.get_width():
			self.die();
		if self.rect.top <= 0:
			self.die();
		elif self.rect.bottom >= self.surface.get_height():
			self.die();

	def die(self):
		self.used = False;
		self.rect.x = self.surface.get_width();
		self.rect.y = self.surface.get_height();

	def draw(self):
		self.surface.blit(self.sheet,self.rect);
