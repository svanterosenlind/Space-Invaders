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
                images[entry.name[:-4]] = pygame.image.load(entry.path)

    font = pygame.font.SysFont("calibri", 14)
    return screen, font, images


def draw_mouse_pos(screen, fn, x, y):
    pos_text = fn.render(f"{x}, {y}", True, (0, 0, 0))
    screen.blit(pos_text, (10, 10))


def draw_shots(screen, game, images, mode):
    for shot in game.shots:
        if shot.variant == 1:
            screen.blit(images["invadershot"][mode], (shot.xpos, shot.ypos))
        if shot.variant == 2:
            screen.blit(images["spaceshipshot"], (shot.xpos, shot.ypos))


def draw_invaders(screen, game, images, mode):
    for invadercol in game.invaders:
        for invader in invadercol:
            if invader is None:
                continue
            if invader.variant == 1:
                screen.blit(images['invader1'][mode], (invader.xpos, invader.ypos))
            elif invader.variant == 2:
                screen.blit(images['invader2'][mode], (invader.xpos, invader.ypos))
            elif invader.variant == 3:
                screen.blit(images['invader3'][mode], (invader.xpos, invader.ypos))


def draw_barricades(screen, game, images):
    for bar in game.barricades:
        screen.blit(images["barricade"], (bar.xpos, bar.ypos))


def draw_spaceship(screen, game, images):
    screen.blit(images["spaceship"], (game.spaceship.xpos, game.spaceship.ypos))


if __name__ == '__main__':
    game = Game()
    screen, font, images = setup_graphics()
    running = True
    invader_step = 100
    shot_step = 64
    t = 0
    steps = 0
    left = False
    right = False
    space = False
    invader_dir = 1
    invader_mode = 0
    shot_mode = 0
    shot_timer = 0
    cl = pygame.time.Clock()
    while running:
        cl.tick(200)
        t += 1
        screen.fill((0, 128, 255))
        draw_mouse_pos(screen, font, pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
        draw_shots(screen, game, images, shot_mode)
        draw_invaders(screen, game, images, invader_mode)
        draw_barricades(screen, game, images)
        draw_spaceship(screen, game, images)
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
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    left = False
                if event.key == pygame.K_RIGHT:
                    right = False
                if event.key == pygame.K_SPACE:
                    space = False
        if t % invader_step == 0:
            invader_dir = game.move_invaders(invader_dir)
            invader_mode = 1-invader_mode
            steps += 1
            if steps % 200 == 0:
                invader_step -= 2
        game.move_spaceship(left, right)
        game.spaceship_shoot(space)
        game.invader_shoot()
        game.move_shots()
        if t % shot_step == 0:
            shot_mode = 1 - shot_mode
        if shot_timer != 0:
            shot_timer -= 1
        if space and shot_timer == 0:
            shot_timer = 24

        game.detect_shot_collisions()