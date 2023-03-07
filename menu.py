import pygame
import math
from UI.button import Button


screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
pygame.display.set_caption("Jeu de role")

background = pygame.image.load("Sprites/Menu/bg.jpg")

button_start = pygame.image.load("Sprites/Menu/start_button.png")
button_start = pygame.transform.scale(button_start, (400, 150))
button_start_rect = button_start.get_rect()
button_start_rect.x = math.ceil(screen.get_width() / 3.33)
button_start_rect.y = math.ceil(screen.get_width() / 3)

button_setting = pygame.image.load("Sprites/Menu/setting_button.jpg")
button_setting = pygame.transform.scale(button_setting, (400, 150))
button_setting_rect = button_setting.get_rect()
button_setting_rect.x = math.ceil(screen.get_width() / 3.33)
button_setting_rect.y = math.ceil(screen.get_width() / 2)

button_arrow = pygame.image.load("Sprites/Menu/button_arrow.png")
button_arrow = pygame.transform.scale(button_arrow, (400, 150))
button_arrow_rect = button_arrow.get_rect()


state: str = "Menu"


def menu_draw():
    screen.fill((0, 0, 0))
    screen.blit(background, (0, -200))
    screen.blit(button_start, button_start_rect)
    screen.blit(button_setting, button_setting_rect)
    pygame.display.update()


def setting_draw():
    screen.fill((0, 0, 0))
    screen.blit(background, (0, -200))
    screen.blit(button_arrow, button_arrow_rect)
    pygame.display.update()


def menu():
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


if state == "Menu":
    menu()
elif state == "Setting":
    setting()
