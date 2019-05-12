import pygame
import time
import random
from Fighter import *
from Enemy import *
from Bullet import *

def main():
	#menu
	game_intro()
	#set into game
	white = (255,255,255);
	global running;
	running = True;
	#set background
	backgroundSpeed = 2;
	backgroundRect = pygame.Rect(0, 0,screen_width,screen_height);
	sheet = pygame.image.load("./res/img/background.jpg").convert();
	sheet2 = sheet.copy();
	pos_y1  = -screen_height;
	pos_y2  = 0;
	start_ticks = 0;
	dodged = 0;
	#set fighter
	fighter = Fighter(gameDisplay,pygame.Rect(screen_width/2,screen_height-100,50,50));
	fighterDownSound = pygame.mixer.Sound("./res/sounds/fighter_down.wav");
	#set enemy
	enemyDownSound = pygame.mixer.Sound("./res/sounds/fighter_down.wav");
	max_enemyNumber = 10;
	enemies = [];
	for enemy in range(max_enemyNumber):
		enemy_x = random.randint(0,screen_width);
		enemies.append(Enemy(gameDisplay,pygame.Rect(enemy_x,0,50,50)));
	#set bullet
	bulletSound = pygame.mixer.Sound("./res/sounds/fire.wav");
	max_bulletNumber = 50;
	bulletIndex = 0;
	bullets = [];
	for bullet in range(max_bulletNumber):
		bullets.append(Bullet(gameDisplay,pygame.Rect(screen_width,screen_height,30,10)));
	#into game
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False;
			if event.type == pygame.KEYDOWN:#射擊事件
				pygame.mixer.Sound.play(bulletSound);
				if event.key == pygame.K_SPACE and not bullets[bulletIndex].isUsed():
					bullets[bulletIndex].setUsed(True,(fighter.rect.x+25),fighter.rect.y);
					bulletIndex = bulletIndex + 1;
					if bulletIndex == max_bulletNumber:
						bulletIndex = 0;
		#background move
		pos_y1 += backgroundSpeed;
		pos_y2 += backgroundSpeed;
		if pos_y1 > 0:
			pos_y1 = -screen_height
		if pos_y2 > screen_height:
			pos_y2 = 0
		#collision check
		for enemy in enemies:
			if pygame.sprite.collide_rect(fighter,enemy):
				seconds = (pygame.time.get_ticks()-start_ticks)/1000;
				if seconds > 3:
					pygame.mixer.Sound.play(fighterDownSound);
					fighter.invincible = False;
					if fighter.reduceLife():
						enemy.die();
						start_ticks = pygame.time.get_ticks();
					else:#END
						largeText = pygame.font.SysFont("comicsansms",30);
						TextSurf, TextRect = text_objects_color("END GAME!!!", largeText,(255,255,255));
						TextRect.center = ((screen_width/2),(screen_width/2));
						gameDisplay.blit(TextSurf, TextRect);
						pygame.display.update();
						time.sleep(5);
						quit();
			for bullet in bullets:
				if pygame.sprite.collide_rect(enemy,bullet):
					if bullet.isUsed():
						pygame.mixer.Sound.play(enemyDownSound);
						dodged = dodged + 1;
						enemy.die();
						bullet.die();
		#event
		key = pygame.key.get_pressed();
		fighter.update(key);
		#draw
		gameDisplay.blit(sheet,(0, pos_y1),backgroundRect);
		gameDisplay.blit(sheet2,(0, pos_y2),backgroundRect);
		fighter.draw();
		for enemy in enemies:
			enemy.update();
			enemy.draw();
		for bullet in bullets:
			bullet.update();
			bullet.draw();
		#text
		things_dodged(gameDisplay,dodged);
		things_life(gameDisplay,fighter.life);
		#update
		pygame.display.update();
		clock.tick(50);
	quitgame();

def game_intro():
	white = (255,255,255);
	red = (200,0,0);
	green = (0,200,0);
	bright_red = (255,0,0);
	bright_green = (0,255,0);
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit();
				quit();
		gameDisplay.fill(white);
		largeText = pygame.font.SysFont("comicsansms",30)
		TextSurf, TextRect = text_objects("Shut Bee!!!", largeText)
		TextRect.center = ((screen_width/2),(screen_width/2))
		gameDisplay.blit(TextSurf, TextRect)
		button("GO!",300,450,100,50,green,bright_green,startgame)
		button("Quit",100,450,100,50,red,bright_red,quitgame)
		pygame.display.update()
		clock.tick(15)

def button(msg,x,y,w,h,ic,ac,action=None):
	mouse = pygame.mouse.get_pos()
	click = pygame.mouse.get_pressed()
	if x+w > mouse[0] > x and y+h > mouse[1] > y:
		pygame.draw.rect(gameDisplay, ac,(x,y,w,h))
		if click[0] == 1 and action != None:
			action()
	else:
		pygame.draw.rect(gameDisplay, ic,(x,y,w,h))
	smallText = pygame.font.SysFont("comicsansms",20)
	textSurf, textRect = text_objects(msg, smallText)
	textRect.center = ( (x+(w/2)), (y+(h/2)) )
	gameDisplay.blit(textSurf, textRect)

def text_objects(text, font):
	black = (0,0,0)
	textSurface = font.render(text, True, black)
	return textSurface, textSurface.get_rect()
def text_objects_color(text,font,color):
	textSurface = font.render(text, True, color)
	return textSurface, textSurface.get_rect()
	
def quitgame():
	pygame.mixer.music.stop();
	pygame.quit();
	quit();

def startgame():
	global running;
	running = False;
def things_dodged(gameDisplay,count):
	font = pygame.font.SysFont(None, 25);
	text = font.render("Source: " + str(count), True,(255,255,255));
	gameDisplay.blit(text,(screen_width-100,0));
def things_life(gameDisplay,count):
	font = pygame.font.SysFont(None, 25);
	text = font.render("Life: " + str(count), True,(255,255,255));
	gameDisplay.blit(text,(screen_width-100,20));



#init pygame
pygame.init();
bgm = pygame.mixer.Sound("./res/sounds/bg_music.wav");
pygame.mixer.Sound.play(bgm);

#set window pygame
screen_height = 780;
screen_width = 500;
window_title = "小蜜蜂!!!";
gameDisplay = pygame.display.set_mode((screen_width,screen_height));
pygame.display.set_caption(window_title);
clock = pygame.time.Clock();
running = True;

#run main
main();