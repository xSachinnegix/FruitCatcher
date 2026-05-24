import pygame
import sys
import random
import time

from pygame.locals import *

pygame.init()
pygame.display.set_caption("Fruit Catcher")
screen = pygame.display.set_mode((800, 600))
screen_w, screen_h = pygame.display.get_surface().get_size()

clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 28)
big_font = pygame.font.SysFont("arial", 50)
small_font = pygame.font.SysFont("arial", 20)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (220, 50, 50)
YELLOW = (255, 220, 0)
ORANGE = (255, 140, 0)
GREEN = (0, 180, 0)
GREY = (100, 100, 100)
BLUE = (100, 180, 255)
BROWN = (139, 90, 43)