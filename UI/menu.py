import pygame 
import math 


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
button_setting_rect.y = math.ceil(screen.get_width() / 3.3)

state: str = "Menu"

while state == "Menu":

    screen.fill((0, 0, 0))
    screen.blit(background, (0, -200)) 
    screen.blit(button_start, button_start_rect)
    screen.blit(button_setting, button_setting_rect)
    
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT :
            state = None
            pygame.quit()  
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if button_start_rect.collidepoint(event.pos):
                state = "Game"
            elif button_setting_rect.collidepoint(event.pos):
                state = "Setting"

while state == "Setting":
    screen.fill((0, 0, 0))
    screen.blit(background, (0, -200)) 
    
            

# endregion
    pygame.display.flip()
    
