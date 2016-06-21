import pygame as pg
from pygame.locals import *
import setup as sp

class Bird(pg.sprite.Sprite):

	WIDTH = HEIGHT = 32
	#SINK_SPEED = 0.18
	#CLIMB_SPEED = 0.3
	#CLIMB_DURATION = 333.3

	def __init__(self, x, y, animate, images):

		super(Bird, self).__init__()
		self.x, self.y = x, y
        #self.msec_to_climb = msec_to_climb
		self._animate_time = animate
		self._animate = -animate
		self.jump = sp.GRAVITY 
		self._img_wingup, self._img_wingdown = images
		self._mask_wingup = pg.mask.from_surface(self._img_wingup)
		self._mask_wingdown = pg.mask.from_surface(self._img_wingdown)

	def update(self, delta_frames=1):
		#not die
		if self.y > sp.WIN_HEIGHT:
			self.jump = sp.JUMP_TIME
			self.y = sp.WIN_HEIGHT/2

		self.y += int(self.jump)
		if(self.jump < sp.GRAVITY):
			self.jump += sp.GRAVITY/6
		elif(self.jump < sp.GRAVITY*2):
			self.jump += sp.GRAVITY/40

	def colides(self):
		return self.y <= 0 or self.y + Bird.WIDTH >= sp.WIN_HEIGHT


	@property
	def image(self):		
		if(self._animate > self._animate_time):
			self._animate = -self._animate_time
		self._animate += 1 
		if self._animate > 0:
			img = self._img_wingup
		else:
			img = self._img_wingdown 

		angle = (float(self.jump)/sp.GRAVITY)*-30
		return pg.transform.rotate(img, angle)

	@property
	def mask(self):
		if self._animate > 0:
			return self._mask_wingup
		else:
			return self._mask_wingdown

	@property
	def rect(self):
		return Rect(self.x, self.y, Bird.WIDTH, Bird.HEIGHT)
		
