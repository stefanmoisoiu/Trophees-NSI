import pygame, sys
from pygame.locals import *

# set window size
width = 300
height = 400
red = (255,0,0)
black = (0,0,0)
grey = (217, 219, 186)
white = (255, 255, 255)
green = (99, 255, 38)
blue = (38, 204, 255)

# initilaise pygame
pygame.init()
root = pygame.display.set_mode((500,500),1, 16)
pygame.draw.rect(root, grey, Rect(0, 20, 300, 390)) #BG
pygame.draw.rect(root, green, [40, 205, 200, 120], 2) #zone temporaire
pygame.draw.rect(root, red, [150, 215, 34, 100], 1) #zone slider 2


#loop start
a = 265
MA_VARIABLE = 30

while True:

    if pygame.mouse.get_pressed()[0] != -0:
        a = pygame.mouse.get_pos()[1] - 0
        if a < 0:
            a = 0

    MA_VARIABLE += a

    pygame.draw.rect(root, blue, Rect(88, 215, 34, 100)) #zone bleu
    pygame.draw.rect(root, black, Rect(103, 215, 5, 100)) #axe 1
    pygame.draw.rect(root, red, [88, 215, 34, 100], 1) #zone slider 1
    pygame.draw.rect(root, black, Rect(90, a, 30, 10)) #rect noir
    pygame.display.update()


# check quit
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()