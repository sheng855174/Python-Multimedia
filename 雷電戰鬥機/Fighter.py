import pygame
from pygame.locals import *


class Fighter(pygame.sprite.Sprite):
	speed = 10;
	life = 3;
	attack = 1;
	roleImage = None;
	sheet = None;
	invincible = False;
	def __init__(self,surface,rect):
		super().__init__();
		self.surface = surface;
		self.rect = rect;
		self.sheet = pygame.image.load("./res/img/figther.png").convert();

	def update(self, key):
		#移動
		if key[K_UP]:
			self.rect.move_ip(0,-self.speed)
		if key[K_DOWN]:
			self.rect.move_ip(0,self.speed)
		if key[K_LEFT]:
			self.rect.move_ip(-self.speed,0)
		if key[K_RIGHT]:
			self.rect.move_ip(self.speed,0)
		#限制範圍
		if self.rect.left < 0:
			self.rect.left = 0
		elif self.rect.right > self.surface.get_width():
			self.rect.right = self.surface.get_width()
		if self.rect.top <= 0:
			self.rect.top = 0
		elif self.rect.bottom >= self.surface.get_height():
			self.rect.bottom = self.surface.get_height()

	def draw(self):
		self.surface.blit(self.sheet,self.rect);

	def reduceLife(self):
		#無敵
		if self.invincible:
			return True;
		#reduce HP
		self.life = self.life - 1;
		self.ivincible = True;
		if self.life == 0:
			return False;
		else:
			return True;



