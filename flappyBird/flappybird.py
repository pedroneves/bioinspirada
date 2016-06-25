import numpy as np
import pygame as pg
import setup as sp
import utils
from bird import Bird
from collections import deque
from neural_network import Neural_Network, NUM_WEIGHTS
from pipe import Pipe
from pygame.locals import *


def testfn():
    from random import uniform
    weights = [uniform(-1, 1) for i in range(NUM_WEIGHTS)]
    net = Neural_Network(weights)
    ret = play(net)
    return ret

def play(neural_network=None):
    pg.init()

    display_surface = pg.display.set_mode((sp.WIN_WIDTH, sp.WIN_HEIGHT))
    pg.display.set_caption('Pygame Flappy Bird')

    images = utils.load_images()
    score_font = pg.font.SysFont(None, 32, bold=True)  # default font

    bird = Bird(50, int(sp.WIN_HEIGHT/2 - Bird.HEIGHT/2), sp.BIRD_ANIMATE,
                (images['bird-wingup'], images['bird-wingdown']))

    pipes = deque()
    pipesTrash = deque()

    score = 0
    done = False
    clock = 0
    #pipes.append(pipe(np.random.randint(sp.WIN_HEIGHT - sp.PIP_SPACE)))
    pipes.append(Pipe(images['pipe-end'], images['pipe-body']))
    while not done:
        pg.time.delay(sp.SLEEP_TIME)
        clock += 1
        if clock % 100 == 0:
            pipes.append(Pipe(images['pipe-end'], images['pipe-body']))

    # Handle this 'manually'.  If we used pygame.time.set_timer(),
    # pipe addition would be messed up when paused.
    #if not (paused or frame_clock % msec_to_frames(PipePair.ADD_INTERVAL)):
    #    pp = PipePair(images['pipe-end'], images['pipe-body'])
    #    pipes.append(pp)

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
        if len(pipes) == 1:
            to_jump = evaluate(neural_network, bird, pipes[0], pipes[0])
        else:
            to_jump = evaluate(neural_network, bird, pipes[0], pipes[1])
        
        if to_jump:
            bird.jump = sp.JUMP_TIME

        if bird.colides():
            done = True
            break

        if len(pipes) > 0 and pg.sprite.collide_mask(pipes[0], bird):
            done = True
            break

    # check for collisions
    #pipe_collision = any(p.collides_with(bird) for p in pipes)
    #if pipe_collision or 0 >= bird.y or bird.y >= WIN_HEIGHT - Bird.HEIGHT:
    #    done = True

        for x in range(0, sp.WIN_WIDTH, sp.WIN_BACKGROUND_SIZE):
            display_surface.blit(images['background'], (x, 0))

        for p in pipes:
            p.update()
            display_surface.blit(p.image, p.rect)

        for p in pipesTrash:
            p.update()
            display_surface.blit(p.image, p.rect)

        if len(pipes) > 0 and pipes[0].posx + Pipe.WIDTH < bird.x:
            pipesTrash.append(pipes.popleft())
            score += 1

        if len(pipesTrash) > 0 and pipesTrash[0].posx + Pipe.WIDTH < 0:
            pipesTrash.popleft()
    #while pipes and not pipes[0].visible:
    #    pipes.popleft()

    #for p in pipes:
    #    p.update()
    #    display_surface.blit(p.image, p.rect)

        bird.update()
        display_surface.blit(bird.image, bird.rect)

    # update and display score
    #for p in pipes:
    #    if p.x + PipePair.WIDTH < bird.x and not p.score_counted:
    #        score += 1
    #        p.score_counted = True

        score_surface = score_font.render(str(score), True, (255, 255, 255))
        score_x = sp.WIN_WIDTH/2 - score_surface.get_width()/2
        display_surface.blit(score_surface, (score_x, sp.PIPE_SPACE))

        pg.display.flip()
    #frame_clock += 1
    pg.quit()
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

