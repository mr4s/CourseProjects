import pygame

global WINDOW_WIDTH
global WINDOW_HEIGHT

global GREEN
global WHITE

global display_surface

global FPS
global clock

global CAR_SIZE

WINDOW_WIDTH  = 1280
WINDOW_HEIGHT = 736

display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

GREEN = (0, 255, 0)
WHITE = (255, 255, 255)

#Set FPS and clock
FPS   = 60
clock = pygame.time.Clock()

CAR_SIZE = (64, 64)
