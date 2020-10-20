import datetime
import random
import sys
import time
import pygame  
import pyttsx3
from random_word import RandomWords

gameIcon = pygame.image.load('images/background.jpg')
pygame.display.set_icon(gameIcon)

r = RandomWords()

engine = pyttsx3.init()
rate = engine.getProperty('rate')
engine.setProperty('rate', rate-70)
voices = engine.getProperty('voices')      
engine.setProperty('voice', voices[1].id)
volume = engine.getProperty('volume')   
engine.setProperty('volume',1.0) 
playWord = False

pygame.init() 

displayWidth = 1024
displayHeight = 768

screen = pygame.display.set_mode((displayWidth, displayHeight)) 

pygame.display.set_caption("Retro Readers")

WHITE = (255, 255, 255) 
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
DUNGEONGROUND = (129, 129, 128)
GROUND = (252, 216, 168)
BUTTONCLICK = (211, 92, 98)
BUTTONCOLOUR = (39, 53, 102)

b1x = 100 
b1y = displayHeight - 200
b1w = 200
b1h = 100
b2x = displayWidth / 2 - 100
b2y = displayHeight - 200
b2w = 200
b2h = 100
b3x = displayWidth - 300
b3y = displayHeight - 200
b3w = 200
b3h = 100
b4x = displayWidth - 175
b4y = 40
b4w = 150
b4h = 65

fontTitle = pygame.font.Font("fonts/OpenDyslexic-Bold.otf", 40) 
fontTitle2 = pygame.font.Font("fonts/OpenDyslexic-Bold.otf", 26) 

p1Title = fontTitle.render("Read", True, WHITE)
p1Rect = p1Title.get_rect(center=(b1x + b1w / 2, b1y + b1h / 2))

p2Title = fontTitle2.render("How To Play", True, WHITE)
p2Rect = p2Title.get_rect(center=(b2x + b2w / 2, b2y + b2h / 2))

p3Title = fontTitle.render("Spell", True, WHITE)
p3Rect = p3Title.get_rect(center=(b3x + b3w / 2, b3y + b3h / 2))

p4Title = fontTitle.render("Store", True, WHITE)
p4Rect = p4Title.get_rect(center=(b4x + b4w / 2, b4y + b4h / 2))

scoreFile = open('playerScore.txt', 'r+')

bIndex = int(scoreFile.readline())
pIndex = int(scoreFile.readline())
scoreFile.close()

backgroundImageList = ["images/background.jpg","images/background1.jpg","images/background2.jpg","images/background3.jpg"]
playerImageList = ["images/player.png","images/player1.png","images/player2.png","images/player3.png"]

backgroundImage = backgroundImageList[bIndex]
playerImage = playerImageList[pIndex]

clock = pygame.time.Clock() 
FPS = 120

TILESIZE = 128
GRIDWIDTH = displayWidth / TILESIZE 
GRIDHEIGHT = displayHeight / TILESIZE 

letterList = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
letterList2 = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]

wallImage = "images/rocks.png"

count = 0

player_sprites = pygame.sprite.Group() 
walls_sprites = pygame.sprite.Group()

music = pygame.mixer.music.stop() 
musicPlay = True 
currentSong = 'Overworld'

currentRoom = 0 

class Room: 
	def __init__(self): 
		self.roomData = []

	def draw(self):
		global currentRoom 
		global musicPlay
		global currentSong
		if musicPlay == True: 
			music = pygame.mixer.music.stop()
			if currentSong == 'Overworld':
				music = pygame.mixer.music.load('audio/Main.mp3')
				pygame.mixer.music.play(-1)
				musicPlay = False

		if currentRoom == 0: 
			self.file = open('room1.txt', 'r')
			walls_sprites.empty()
			currentRoom = -1 

		for line in self.file:
			self.roomData.append(line) 
		for row, tiles in enumerate(self.roomData):
			for col, tile in enumerate(tiles):
				if tile == '!':
					Wall(col, row)
				if tile in letterList:
					val = tile
					Letter(col, row, val)
		self.roomData.clear() 

class Letter(pygame.sprite.Sprite):
    def __init__(self, x, y, val):
        self.groups = walls_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.fontTitle = pygame.font.Font("fonts/OpenDyslexic-Regular.otf", 70) 

        if y == 1:
            self.image = self.fontTitle.render(val, True, (46,255,255)) 
        elif y == 2 or y == 3:
            self.image = self.fontTitle.render(val, True, (254,109,188)) 
        elif y == 4 or y == 5:
            self.image = self.fontTitle.render(val, True, (254,255,66)) 
        else:
            self.image = self.fontTitle.render(val, True, BLACK)

        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE + 35
        self.rect.y = y * TILESIZE

class Player(pygame.sprite.Sprite): 
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(playerImage) 
		self.image =  pygame.transform.scale(self.image,(TILESIZE, TILESIZE))
		self.rect = self.image.get_rect()
		self.rect.center = (displayWidth - 75, displayHeight - 50) 
		self.hitWall = False 

		self.score = 0
		self.drawTrue = False
		self.drawTrue2 = False
		self.word = ''
		self.typedWord = ''

		self.wList = ['apple','acute','banana','bus','cat','car','dog','down','ever','end','fun','fur','good','gum','hat','hello','it','intel','just','juice','kite','key','lose','line','money','more','nice','now','open','on','pool','pun','quilt','quit','rat','read','super','soak','tug','tub','umbrella','up','video','vibe','wash','win','xylophone','x-ray','yes','yell','zebra','zaps']

		self.fontTitle = pygame.font.Font("fonts/OpenDyslexic-Regular.otf", 40) 
		self.scoreTitle = self.fontTitle.render("Score: " + str(self.score), True, WHITE) 
		self.scoreRect = self.scoreTitle.get_rect(center=(100, displayHeight - 50)) 
		self.wordTitle = self.fontTitle.render(self.word, True, WHITE)
		self.wordRect = self.wordTitle.get_rect(center=(displayWidth / 2 - 50, displayHeight / 2))		
		self.wordTitle2 = self.fontTitle.render(self.typedWord, True, WHITE)
		self.wordRect2 = self.wordTitle2.get_rect(center=(displayWidth / 2 - 50, 65))		
	
	def update(self): 
		global currentRoom 
		global musicPlay
		global currentSong
		global playWord
		self.keyList = [pygame.K_a, pygame.K_b, pygame.K_c, pygame.K_d, pygame.K_e, pygame.K_f, pygame.K_g, pygame.K_h, pygame.K_i, pygame.K_j, pygame.K_k, pygame.K_l, pygame.K_m, pygame.K_n, pygame.K_o, pygame.K_p, pygame.K_q, pygame.K_r, pygame.K_s, pygame.K_t, pygame.K_u, pygame.K_v, pygame.K_w, pygame.K_x, pygame.K_y, pygame.K_z, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9]
		if event.type == pygame.KEYDOWN: 
			for i in self.keyList:
				if i == event.key:
					val2 = self.keyList.index(event.key)
					try:
						val3 = r.get_random_words(maxLength = 5)
						for i in val3:
							self.wList.append(i)
							if i[0] == letterList2[val2]:
								self.drawTrue = True
								self.word = i	
								self.wordTitle = self.fontTitle.render(i, True, BLACK)
								playWord = True
								break
							else:
								for j in self.wList:
									if j[0] == letterList2[val2]:
										self.drawTrue = True
										self.wordTitle = self.fontTitle.render(j, True, BLACK)
										self.word = j
										self.wList.remove(j)
										playWord = True
										break
					except Exception:
						for j in self.wList:
							if j[0] == letterList2[val2]:
								self.drawTrue = True
								self.wordTitle = self.fontTitle.render(j, True, BLACK)
								self.word = j
								self.wList.remove(j)
								playWord = True		
								break

	def update1(self): 
		global currentRoom 
		global musicPlay
		global currentSong
		global playWord		

		try:
			val3 = r.get_random_word(maxLength = 5)
			self.word = val3
			playWord = True		
		except Exception:
			for j in self.wList:
				self.word = j
				self.wList.remove(j)
				playWord = True	
				break

	def update2(self): 
		global currentRoom 
		global musicPlay
		global currentSong
		global playWord
		global count
		self.keyList = [pygame.K_a, pygame.K_b, pygame.K_c, pygame.K_d, pygame.K_e, pygame.K_f, pygame.K_g, pygame.K_h, pygame.K_i, pygame.K_j, pygame.K_k, pygame.K_l, pygame.K_m, pygame.K_n, pygame.K_o, pygame.K_p, pygame.K_q, pygame.K_r, pygame.K_s, pygame.K_t, pygame.K_u, pygame.K_v, pygame.K_w, pygame.K_x, pygame.K_y, pygame.K_z, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9]
		
		if event.type == pygame.KEYDOWN: 
			for i in self.keyList:
				if i == event.key:
					val2 = self.keyList.index(event.key)
					self.typedWord += letterList2[val2]
					self.wordTitle2 = self.fontTitle.render(self.typedWord, True, WHITE)
					self.drawTrue2 = True
					time.sleep(0.2)
					if self.typedWord == self.word:
						self.score += 5
						self.scoreTitle = self.fontTitle.render("Score: " + str(self.score), True, WHITE) 
						count = 0
						self.typedWord = ''
						self.wordTitle2 = self.fontTitle.render(self.typedWord, True, WHITE)
			if event.key == pygame.K_BACKSPACE:
				self.typedWord = self.typedWord[:-1]						
				self.wordTitle2 = self.fontTitle.render(self.typedWord, True, WHITE)
				time.sleep(0.2)

	def draw(self, surf):
		screen.blit(self.scoreTitle, self.scoreRect)
		if self.drawTrue:
			pygame.draw.rect(screen, WHITE, (displayWidth / 2 - 200, displayHeight / 2 - 150, 400, 300))
			screen.blit(self.wordTitle, self.wordRect)
		if self.drawTrue2:
			screen.blit(self.wordTitle2, self.wordRect2)

class StartScreen: 
	def __init__(self): 
		global music 
		music = pygame.mixer.music.stop() 
		music = pygame.mixer.music.load('audio/Title.mp3')
		music = pygame.mixer.music.set_volume(0.1)
		pygame.mixer.music.play(-1)		
		screen.fill(BLACK)

		self.fontTitle = pygame.font.Font("fonts/OpenDyslexic-Regular.otf", 15)
		self.background2Image = pygame.image.load("images/startScreen.png")
		self.background2Image = pygame.transform.scale(self.background2Image,(displayWidth, displayHeight))
		self.background2Rect = self.background2Image.get_rect()
		self.background2Rect.center = (displayWidth / 2, displayHeight / 2) 

	def draw(self, surf): 
		screen.blit(self.background2Image, (self.background2Rect)) 
	
start = StartScreen() 

player = Player() 
player_sprites.add(player) 

pointsFile = open('playerPoints.txt', 'r+')

player.score = int(pointsFile.readline())
player.scoreTitle = player.fontTitle.render("Score: " + str(player.score), True, WHITE) 
player.scoreRect = player.scoreTitle.get_rect(center=(100, 50))  
pointsFile.close()

room = Room() 

startLoop = True 
game1p = False
game2p = False

background2Image = pygame.image.load(backgroundImage)
background2Image = pygame.transform.scale(background2Image,(displayWidth, displayHeight))
background2Rect = background2Image.get_rect()
background2Rect.center = (displayWidth / 2, displayHeight / 2)

while startLoop: 
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			startLoop = False

	screen.fill(BLACK) 
	start.draw(screen) 
 
	mouse = pygame.mouse.get_pos() 
	click = pygame.mouse.get_pressed()

	if b1x+b1w > mouse[0] > b1x and b1y+b1h > mouse[1] > b1y:
		pygame.draw.rect(screen, BUTTONCLICK, (b1x,b1y,b1w,b1h))
		if click[0] == 1:
			game1p = True
			musicPlay = True
			currentSong = "Overworld"
	else:
		pygame.draw.rect(screen, BUTTONCOLOUR, (b1x,b1y,b1w,b1h))
	pygame.draw.rect(screen, BLACK, (b1x - 5,b1y - 5,b1w + 10,b1h + 10), 10)

	
	if b3x+b3w > mouse[0] > b3x and b3y+b3h > mouse[1] > b3y: 
		pygame.draw.rect(screen, BUTTONCLICK, (b3x,b3y,b3w,b3h))
		if click[0] == 1: 
			game2p = True
			musicPlay = True
			currentSong = "Overworld"
	else:
		pygame.draw.rect(screen, BUTTONCOLOUR, (b3x,b3y,b3w,b3h))
	pygame.draw.rect(screen, BLACK, (b3x - 5,b3y - 5,b3w + 10,b3h + 10), 10)

	if b2x+b2w > mouse[0] > b2x and b2y+b2h > mouse[1] > b2y:
		instImage = pygame.image.load("images/instructions.png")
		instRect = instImage.get_rect()
		instRect.center = (displayWidth / 2, displayHeight / 2)
		screen.blit(instImage, instRect)
	else:
		pygame.draw.rect(screen, BUTTONCOLOUR, (b2x,b2y,b2w,b2h))
		pygame.draw.rect(screen, BLACK, (b2x - 5,b2y - 5,b2w + 10,b2h + 10), 10)
		pygame.draw.rect(screen, BLACK, (b4x - 5,b4y - 5,b4w + 10,b4h + 10), 10)
		screen.blit(p1Title, p1Rect) 
		screen.blit(p2Title, p2Rect) 
		screen.blit(p3Title, p3Rect) 

	if b4x+b4w > mouse[0] > b4x and b4y+b4h > mouse[1] > b4y: 
		screen.fill(BUTTONCOLOUR)
		storeImage = pygame.image.load("images/store.png")
		storeRect = storeImage.get_rect()
		storeRect.center = (displayWidth / 2, displayHeight / 2)
		screen.blit(storeImage, storeRect)
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN: 
				if event.key == pygame.K_1 and player.score >= 20:
					backgroundImage = backgroundImageList[1]
					background2Image = pygame.image.load(backgroundImage)
					player.score -= 20
					player.scoreTitle = player.fontTitle.render("Score: " + str(player.score), True, WHITE) 
					player.scoreRect = player.scoreTitle.get_rect(center=(100, 50))  
				if event.key == pygame.K_2 and player.score >= 20:
					backgroundImage = backgroundImageList[2]
					background2Image = pygame.image.load(backgroundImage)
					player.score -= 20
					player.scoreTitle = player.fontTitle.render("Score: " + str(player.score), True, WHITE) 
					player.scoreRect = player.scoreTitle.get_rect(center=(100, 50))  
				if event.key == pygame.K_3 and player.score >= 20:
					backgroundImage = backgroundImageList[3]
					background2Image = pygame.image.load(backgroundImage)
					player.score -= 20
					player.scoreTitle = player.fontTitle.render("Score: " + str(player.score), True, WHITE) 
					player.scoreRect = player.scoreTitle.get_rect(center=(100, 50))  
				if event.key == pygame.K_4 and player.score >= 50:
					playerImage = playerImageList[1]
					player.image = pygame.image.load(playerImage)  
					player.image =  pygame.transform.scale(player.image,(TILESIZE, TILESIZE))	
					player.score -= 50
					player.scoreTitle = player.fontTitle.render("Score: " + str(player.score), True, WHITE) 
					player.scoreRect = player.scoreTitle.get_rect(center=(100, 50))  
				if event.key == pygame.K_5 and player.score >= 50:
					playerImage = playerImageList[2]
					player.image = pygame.image.load(playerImage) 
					player.image =  pygame.transform.scale(player.image,(TILESIZE, TILESIZE))	
					player.score -= 50
					player.scoreTitle = player.fontTitle.render("Score: " + str(player.score), True, WHITE) 
					player.scoreRect = player.scoreTitle.get_rect(center=(100, 50))  
				if event.key == pygame.K_6 and player.score >= 50:
					playerImage = playerImageList[3]
					player.image = pygame.image.load(playerImage) 
					player.image =  pygame.transform.scale(player.image,(TILESIZE, TILESIZE))	
					player.score -= 50
					player.scoreTitle = player.fontTitle.render("Score: " + str(player.score), True, WHITE) 
					player.scoreRect = player.scoreTitle.get_rect(center=(100, 50))  
		player.scoreRect = player.scoreTitle.get_rect(center=(100, 50))  
		screen.blit(player.scoreTitle, player.scoreRect)
	else:
		pygame.draw.rect(screen, BUTTONCOLOUR, (b4x,b4y,b4w,b4h))
		pygame.draw.rect(screen, BLACK, (b4x - 5,b4y - 5,b4w + 10,b4h + 10), 10)
		screen.blit(p4Title, p4Rect) 

	pygame.display.update() 
	clock.tick(FPS) 

	while game1p:
		for event in pygame.event.get(): 
			if event.type == pygame.QUIT:
				scoreFile1 = open('playerScore.txt', 'r+')
				scoreFile1.write(str(backgroundImageList.index(backgroundImage)) + "\n" + str((playerImageList.index(playerImage))))
				scoreFile1.close()
				scoreFile2 = open('playerPoints.txt', 'r+')
				scoreFile2.write(str(player.score))
				scoreFile2.close()
				game1p = False	
				game2p =  False
				startLoop = False	

		room.draw() 

		screen.fill(BLACK) 
		player_sprites.update()

		if playWord == True:
			engine.say(player.word)
			engine.runAndWait()
			playWord = False

		screen.blit(background2Image, (background2Rect)) 
		
		walls_sprites.draw(screen) 
		
		player_sprites.draw(screen) 
		player.draw(screen)

		pygame.display.update()

		clock.tick(FPS) 

	while game2p:
		for event in pygame.event.get(): 
			if event.type == pygame.QUIT:
				scoreFile1 = open('playerScore.txt', 'r+')
				scoreFile1.write(str(backgroundImageList.index(backgroundImage)) + "\n" + str((playerImageList.index(playerImage))))
				scoreFile1.close()
				scoreFile2 = open('playerPoints.txt', 'r+')
				scoreFile2.write(str(player.score))
				scoreFile2.close()
				game1p = False	
				startLoop = False
				game2p = False
		room.draw() 

		screen.fill(BLACK) 
		while count == 0:
			player.update1() 
			count = 1
		player.update2()

		screen.blit(background2Image, (background2Rect)) 
		
		walls_sprites.draw(screen) 
		
		player_sprites.draw(screen) 
		player.draw(screen) 

		pygame.display.update() 

		clock.tick(FPS) 

		if playWord == True:
			time.sleep(2)
			engine.say(player.word)
			engine.runAndWait()
			playWord = False
			time.sleep(1)

pygame.quit() 
sys.exit()