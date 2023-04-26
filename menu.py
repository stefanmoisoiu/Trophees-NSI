import pygame

from main import *

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Hermes Odyssey")

background = pygame.image.load("Sprites/Menu/bg.png")
background = pygame.transform.scale(background, ((background.get_width(), background.get_height())))
background_rect = screen.get_rect()

button_start = pygame.image.load("Sprites/Menu/start_button.png")
button_start = pygame.transform.scale(button_start, (400, 150))
button_start_rect = button_start.get_rect()
button_start_rect.center = (screen.get_width() / 2, screen.get_height() / 2)

button_setting = pygame.image.load("Sprites/Menu/setting_button.png")
button_setting = pygame.transform.scale(button_setting, (button_setting.get_width() * 1.5 , button_setting.get_height() * 1.5 ))
button_setting_rect = button_setting.get_rect()
button_setting_rect.center = (screen.get_width() / 2, screen.get_height() / 1.5)

button_arrow = pygame.image.load("Sprites/Menu/button_arrow.png")
button_arrow = pygame.transform.scale(button_arrow, (button_arrow.get_width() * 1.7 , button_arrow.get_height() * 1.7 ))
button_arrow_rect = button_arrow.get_rect()


state: str = "Menu"
running: bool = True


def menu_draw():
    screen.fill((0, 0, 0))
    screen.blit(background, background_rect.topleft)
    screen.blit(button_start, button_start_rect)
    screen.blit(button_setting, button_setting_rect)
    pygame.display.update()


def setting_draw():
    screen.fill((0, 0, 0))
    screen.blit(background, background_rect.topleft)
    screen.blit(button_arrow, button_arrow_rect.topleft)
    pygame.display.update()


def menu():
    '''Fonction qui gère le menu'''
    global state
    while state == "Menu":

        menu_draw()

        pygame.display.update()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                state = None
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_start_rect.collidepoint(event.pos):
                    state = "Game"
                elif button_setting_rect.collidepoint(event.pos):
                    state = "Setting"
                    setting()
        pygame.display.flip()


def setting():
    '''Fonction qui gère le setting'''
    global state
    while state == "Setting":

        setting_draw()

        pygame.display.update()
        
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                state = None
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_arrow_rect.collidepoint(event.pos):
                    state = "Menu"
                    menu()
        pygame.display.flip()


while running:
    if state == "Menu":
        menu()
    elif state == "Setting":
        setting()
    elif state == "Game":
        print("Game")
        running = False
        gameLoop(True)
    else:
        print("Error")
        running = False