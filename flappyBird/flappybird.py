import numpy as np
import pygame as pg
import setup as sp
import utils
from bird import Bird
from collections import deque
from neural_network import Neural_Network, NUM_WEIGHTS
from pipe import Pipe
from pygame.locals import *

image_wrapper = list()

def initialize():
    pg.init()
    display_surface = pg.display.set_mode((sp.WIN_WIDTH, sp.WIN_HEIGHT))
    image_wrapper.append(utils.load_images())

def terminate():
    pg.quit()

def play(neural_network=None, display=True):
    #pg.init()

    display_surface = pg.display.set_mode((sp.WIN_WIDTH, sp.WIN_HEIGHT))
    pg.display.set_caption('Pygame Flappy Bird')
    score_font = pg.font.SysFont(None, 32, bold=True)  # default font
    images = image_wrapper[0]

    bird = Bird(50, int(sp.WIN_HEIGHT/2 - Bird.HEIGHT/2), sp.BIRD_ANIMATE,
                (images['bird-wingup'], images['bird-wingdown']))

    pipes = deque()
    pipesTrash = deque()
    pipes.append(Pipe(images['pipe-end'], images['pipe-body']))

    score = 0
    done = False
    clock = 0

    while not done:
        # pg.time.delay(sp.SLEEP_TIME)
        clock += 1
        if clock % 100 == 0:
            pipes.append(Pipe(images['pipe-end'], images['pipe-body']))

        for e in pg.event.get():
            if e.type == QUIT or (e.type == KEYUP and e.key == K_ESCAPE):
                done = True
                break
            elif e.type == KEYUP and e.key == K_KP_PLUS:
                sp.SLEEP_TIME -= 5
            elif e.type == KEYUP and e.key == K_KP_MINUS:
                sp.SLEEP_TIME += 5

        to_jump = False
        if len(pipes) == 0:
            raise Exception("No pipes")
        if len(pipes) == 1 and not (neural_network is None):
            to_jump = evaluate(neural_network, bird, pipes[0], pipes[0])
        elif not (neural_network is None):
            to_jump = evaluate(neural_network, bird, pipes[0], pipes[1])

        if to_jump:
            bird.jump = sp.JUMP_TIME

        if bird.colides():
            done = True
            break

        if len(pipes) > 0 and pg.sprite.collide_mask(pipes[0], bird):
            done = True
            break

        if display:
            for x in range(0, sp.WIN_WIDTH, sp.WIN_BACKGROUND_SIZE):
                display_surface.blit(images['background'], (x, 0))

        for p in pipes:
            p.update()
            if display:
                display_surface.blit(p.image, p.rect)

        for p in pipesTrash:
            p.update()
            if display:
                display_surface.blit(p.image, p.rect)

        if len(pipes) > 0 and pipes[0].posx + Pipe.WIDTH < bird.x:
            pipesTrash.append(pipes.popleft())
            score += 1

        if len(pipesTrash) > 0 and pipesTrash[0].posx + Pipe.WIDTH < 0:
            pipesTrash.popleft()

        bird.update()
        if display:
            display_surface.blit(bird.image, bird.rect)

        if display:
            score_surface = score_font.render(str(score), True, (255, 255, 255))
            score_x = sp.WIN_WIDTH/2 - score_surface.get_width()/2
            display_surface.blit(score_surface, (score_x, sp.PIPE_SPACE))

        if display:
            pg.display.flip()
    
    if display:
        display_surface.fill( (0, 0, 0) )
        pg.display.flip()

    #pg.quit()
    return {'score': score, 'clock': clock}

# Return true if the decision is to jump
def evaluate(nn, bird, pipe1, pipe2):
    bird_y = bird.y
    bird_acc = bird.jump
    pipe1_x = pipe1.posx
    pipe2_x = pipe2.posx
    pipe1_y = pipe1.passage_center_y
    pipe2_y = pipe2.passage_center_y

    nn_input = [bird_y, bird_acc, pipe1_x, pipe1_y, pipe2_x, pipe2_y]

    nn_output = nn.feedforward(nn_input)
    # To jump or not to jump, that is the question
    jump = np.sign(nn_output) > 0
    return jump
