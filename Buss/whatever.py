from pygame import *
import pygame

if __name__ == "__main__":
    # initialize the pygame module
    pygame.init()
    # load and set the logo
    background = pygame.image.load("background.png")
    red_bus_small = pygame.image.load("red_bus_small.png")

    # pygame.display.set_icon(logo)
    pygame.display.set_caption("Bus Simulator 2018")

    # create a surface on screen that has the size of 240 x 180
    screen = pygame.display.set_mode((1400, 660))

    red_bus_small.set_colorkey((255, 255, 255))

    images = [background, red_bus_small]
