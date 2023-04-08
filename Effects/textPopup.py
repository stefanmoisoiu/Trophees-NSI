import pygame
import math

from Base.timer import Timer


class TextPopupAdditionalProperties:
    '''A class to display a text on the screen'''
    def __init__(self, font: pygame.font.Font, color: tuple[int, int, int] = (255, 255, 255), startFadingAt: float = 0.5, duration: int = 1):
        self.color = color
        self.startFadingAt = startFadingAt
        self.duration = duration
        self.timer = Timer(duration, lambda: None)
        self.font = font


class TextPopup:
    '''A class to display a text on the screen'''
    def __init__(self, text: str, startPosition: tuple[int, int], endPosition: tuple[int, int], additionalProperties: TextPopupAdditionalProperties, onPopupEnd: callable = None):
        self.text = text
        self.startPosition = startPosition
        self.endPosition = endPosition
        self.additionalProperties = additionalProperties

        self.timer = Timer(additionalProperties.duration, [self.Die])
        if onPopupEnd is not None:
            self.timer.callbacks.append(onPopupEnd)

        self.surface = self.additionalProperties.font.render(
            self.text, True, self.additionalProperties.color)
        self.rect = self.surface.get_rect()
        self.rect.center = self.startPosition

        self.alive = True

    def Die(self):
        '''Fonction qui gère la mort du joueur'''
        self.alive = False

    def SurfaceByAdvancement(self, baseSurface: pygame.Surface, advancement: float) -> pygame.Surface:
        '''Fonction qui met à jour la surface de l'affichage'''
        if advancement < self.additionalProperties.startFadingAt:
            return baseSurface

        transparentSurface = baseSurface.copy()
        remappedAdvancement = (
            advancement - self.additionalProperties.startFadingAt) * 1 / self.additionalProperties.startFadingAt

        transparentSurface.set_alpha(int(255 * (1-remappedAdvancement)))
        return transparentSurface

    def Update(self, deltaTime: float):
        '''Fonction qui met à jour le joueur'''
        if not self.alive:
            return

        self.timer.Update(deltaTime)
        easedAdvancement = math.sin(self.timer.advancement * math.pi/2)
        offset = ((self.endPosition[0] - self.startPosition[0]) * easedAdvancement,
                  (self.endPosition[1] - self.startPosition[1]) * easedAdvancement)
        self.rect.center = (
            self.startPosition[0]+offset[0], self.startPosition[1]+offset[1])

    def Display(self, screen: pygame.Surface):
        screen.blit(self.SurfaceByAdvancement(
            self.surface, self.timer.advancement), self.rect.topleft)


pygame.init()

normalPopup = TextPopupAdditionalProperties(
    pygame.font.Font("Fonts/Retro Gaming.ttf", 30), (255, 255, 255), 0.5, 1)
damagePopup = TextPopupAdditionalProperties(
    pygame.font.Font("Fonts/Retro Gaming.ttf", 30), (255, 0, 0), 0.5, 1)
healPopup = TextPopupAdditionalProperties(
    pygame.font.Font("Fonts/Retro Gaming.ttf", 30), (0, 255, 0), 0.5, 1)
missPopup = TextPopupAdditionalProperties(
    pygame.font.Font("Fonts/Retro Gaming.ttf", 30), (150, 150, 150), 0.5, 1)

activePopups: list[TextPopup] = []
