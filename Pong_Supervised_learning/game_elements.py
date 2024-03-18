import pygame
from random import randint
BLACK = (0,0,0)

class Paddle(pygame.sprite.Sprite):
	def __init__(self, color, width, height):
		super().__init__()

		#set
		self.image = pygame.Surface([width, height])
		self.image.fill(BLACK)
		self.image.set_colorkey(BLACK)

		#draw paddle
		pygame.draw.rect(self.image, color, [0, 0, width, height])

		#fetch rectangle
		self.rect = self.image.get_rect()


	#moving up
	def moveUp(self, pixels):
		self.rect.y -= pixels
		if self.rect.y < 0:
			self.rect.y = 0

	#moving down
	def moveDown(self, pixels):
		self.rect.y += pixels
		if self.rect.y > 400:
			self.rect.y = 400
   
	def goToPosition(self, position):
		if position >= 400:
			self.rect.y = 400
		elif position <= 0:
			self.rect.y = 0
		else:
			self.rect.y = position
   
   
class Ball(pygame.sprite.Sprite):
	def __init__(self, color, width, height):
		super().__init__()

		#set
		self.image = pygame.Surface([width, height])
		self.image.fill(BLACK)
		self.image.set_colorkey(BLACK)

		#draw ball
		pygame.draw.rect(self.image, color, [0, 0, width, height])

		#velocity
		self.velocity_x = randint(4,10)
		self.velocity_y = randint(-8,8)
    
		self.velocity = [self.velocity_x,self.velocity_y]

		#fetch rectangle
		self.rect = self.image.get_rect()
  

	#update
	def update(self):
		self.rect.x += self.velocity[0]
		self.rect.y += self.velocity[1]

	#bounce
	def bounce(self):
		self.velocity[0] = -self.velocity[0]
		self.velocity[1] = randint(-8,8)