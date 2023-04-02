import pygame
import Base.events as events


class Button:
    def __init__(self, idleImage: pygame.Surface, hoverImage: pygame.Surface, clickImage: pygame.Surface, position: tuple[int, int], imgScale=1, action: callable = None, *actionArgs):
        self.idleImage = pygame.transform.scale(
            idleImage, (idleImage.get_width()*imgScale, idleImage.get_height()*imgScale))
        self.hoverImage = pygame.transform.scale(
            hoverImage, (hoverImage.get_width()*imgScale, hoverImage.get_height()*imgScale))
        self.clickImage = pygame.transform.scale(
            clickImage, (clickImage.get_width()*imgScale, clickImage.get_height()*imgScale))
        self.position = position
        self.action = action
        self.actionArgs = actionArgs
        self.image = self.idleImage
        self.rect = idleImage.get_rect()
        self.rect.topleft = self.position
        events.onLeftClick.append(self.OnClickEvent)

    def Display(self, screen):
        if self.image is None:
            return
        screen.blit(self.image, self.position)

    def MouseHovered(self):
        mousePos = pygame.mouse.get_pos()
        return self.rect.collidepoint(mousePos)

    def Update(self):
        self.rect.topleft = self.position
        if self.MouseHovered():
            if pygame.mouse.get_pressed()[0]:
                self.image = self.clickImage
            else:
                self.image = self.hoverImage
        else:
            self.image = self.idleImage

    def OnClickEvent(self):
        if self.MouseHovered() and self.action is not None:
            if len(self.actionArgs) > 0:
                self.action(*self.actionArgs)
            else:
                self.action()
