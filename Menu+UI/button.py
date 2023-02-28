import pygame
import Base.events as events


class Button:
    def __init__(self, idleImage: pygame.Surface, hoverImage: pygame.Surface, clickImage: pygame.Surface, position: tuple[int, int], action: callable = None):
        self.idleImage = idleImage
        self.hoverImage = hoverImage
        self.clickImage = clickImage
        self.position = position
        self.action = action
        self.image = self.idleImage
        self.rect = self.image.get_rect()
        self.rect.topleft = self.position
        events.onLeftClick.append(self.OnClickEvent)

    def Display(self, screen):
        screen.blit(self.image, self.position)

    def Update(self):
        mousePos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mousePos):
            if pygame.mouse.get_pressed()[0]:
                self.image = self.clickImage
            else:
                self.image = self.hoverImage
        else:
            self.image = self.idleImage

    def OnClickEvent(self):
        if self.action is not None:
            self.action()
