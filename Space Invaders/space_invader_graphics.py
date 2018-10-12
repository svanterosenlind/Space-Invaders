import pygame
import os
from space_invaders import *


def setup_graphics():
    pygame.init()
    screen = pygame.display.set_mode((1200, 800))
    pygame.display.set_caption("Space Invaders")

    images = {}
    with os.scandir(".\images") as it:
        for entry in it:
            if entry.is_dir():
                imagelist = []
                with os.scandir(entry.path) as it2:
                    for image in it2:
                        imagelist.append(pygame.image.load(image.path))
                images[entry.name] = imagelist
            else:
                images[entry.name] = pygame.image.load(entry.path)

    font = pygame.font.SysFont("calibri", 14)
    return screen, font, images


def draw_shots(screen, game, images, mode):
    for shot in game.shots:
        if shot.variant == 1:
            screen.blit(images["invadershot"][mode], (shot.xpos, shot.ypos))
            print("Shot drawn")


def draw_invaders(screen, game, images, mode):
    screen.fill((0, 128, 255))
    for invadercol in game.invaders:
        for invader in invadercol:
            if invader.variant == 1:
                screen.blit(images['invader1'][mode], (invader.xpos, invader.ypos))
            elif invader.variant == 2:
                screen.blit(images['invader2'][mode], (invader.xpos, invader.ypos))
            elif invader.variant == 3:
                screen.blit(images['invader3'][mode], (invader.xpos, invader.ypos))


if __name__ == '__main__':
    game = Game()
    screen, font, images = setup_graphics()
    running = True
    invader_step = 20
    t = 0
    steps = 0
    invader_dir = 1
    invader_mode = 0
    shot_mode = 0
    while running:
        t += 1
        draw_shots(screen, game, images, shot_mode)
        draw_invaders(screen, game, images, invader_mode)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    left = True
                if event.key == pygame.K_RIGHT:
                    right = True
                if event.key == pygame.K_SPACE:
                    space = True

        if t % invader_step == 0:
            invader_dir = game.move_invaders(invader_dir)
            invader_mode = 1-invader_mode
            steps += 1
            if steps % 200 == 0:
                invader_step -= 2
        game.invader_shoot()
        game.move_shots()
        shot_mode = 1 - shot_mode
