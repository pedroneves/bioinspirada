import pygame as pg
import setup as sp
import numpy as np
from pygame.locals import *
from bird import Bird

class Pipe(pg.sprite.Sprite):

	WIDTH = 80
	def __init__(self, pipe_end_img, pipe_body_img):

		super(Pipe, self).__init__()
		#self.height = height
		self.posx = sp.WIN_WIDTH -1
		self.pipe_end_img = pipe_end_img
		self.pipe_body_img = pipe_body_img

		self.image = pg.Surface((Pipe.WIDTH, sp.WIN_HEIGHT), pg.SRCALPHA, 32)
		self.image.convert()
		self.image.fill((0,0,0,0))
		total_pip_body_peices = int(
			(sp.WIN_HEIGHT -
				3 * Bird.HEIGHT -
				3 * sp.PIPE_SPACE) /
				sp.PIPE_SPACE
			)

		self.bottom_pieces = np.random.randint(1, total_pip_body_peices)
		self.top_pieces = total_pip_body_peices - self.bottom_pieces

		for i in range(1, self.bottom_pieces + 1):
			pices_pos = (0, sp.WIN_HEIGHT - i*sp.PIPE_SPACE)
			self.image.blit(pipe_body_img, pices_pos)
		bottom_pipe_end_y = sp.WIN_HEIGHT - self.bottom_pieces * sp.PIPE_SPACE
		bottom_end_piece_pos = (0, bottom_pipe_end_y - sp.PIPE_SPACE)
		self.image.blit(pipe_end_img, bottom_end_piece_pos)

		for i in range(self.top_pieces):
			self.image.blit(pipe_body_img, (0, i * sp.PIPE_SPACE))
		top_pipe_end_y = self.top_pieces * sp.PIPE_SPACE
		self.image.blit(pipe_end_img, (0, top_pipe_end_y))

		self.top_pieces += 1
		self.bottom_pieces += 1

        # for collision detection
		self.mask = pg.mask.from_surface(self.image)



	def update(self):
		self.posx -= sp.PIPE_ANIMATE

	@property
	def rect(self):
		return Rect(self.posx, 0, Pipe.WIDTH, sp.PIPE_SPACE)
		