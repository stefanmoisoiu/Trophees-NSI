import math
import pygame
import Base.gridManager as gridManager

'''Classe qui permet de gérer une animation, ex: marcher, courir, sauter, etc...'''


class Animation:
    def __init__(self, spriteSheet: pygame.Surface, length: float = 1, loop: bool = True, horizontalFrames: int = 1, verticalFrames: int = 1, scale: float = 1.0, topleft: tuple[int, int] = (0, 0)) -> None:
        self.spriteSheet = spriteSheet
        self.horizontalFrames = horizontalFrames
        self.verticalFrames = verticalFrames
        self.loop = loop
        self.length = length
        self.topleft = topleft
        self.frames = GenerateAnimationFrames(
            spriteSheet, horizontalFrames, verticalFrames, scale)


'''Decoupe le spriteSheet en plusieurs frames et les retourne dans une liste de surfaces'''


def GenerateAnimationFrames(spriteSheet: pygame.Surface, horizontalFrames: int, verticalFrames: int, scale: float = 1.0) -> list[pygame.Surface]:
    frames = []
    frameWidth = spriteSheet.get_width() / horizontalFrames
    frameHeight = spriteSheet.get_height() / verticalFrames

    for i in range(verticalFrames):
        for j in range(horizontalFrames):

            frame = spriteSheet.subsurface(
                (j/horizontalFrames * spriteSheet.get_width(), i/verticalFrames * spriteSheet.get_height(), frameWidth, frameHeight))
            frame = pygame.transform.scale(
                frame, (int(frameWidth*scale), int(frameHeight*scale)))

            frames.append(frame)
    return frames


'''Classe qui permet de gérer toutes animations d'un objet'''


class AnimationManager:
    def __init__(self) -> None:
        self.currentAnimation: Animation = None
        self.advancement: float = 0.0

    '''Change l'animation qui est en cours de lecture et execute des fonctions a un avancement donne dans la PREMIERE boucle si elle est specifiee'''

    def PlayAnimation(self, animation: Animation, callbacks: list[tuple[callable, float]] = None) -> None:
        self.currentAnimation = animation
        self.callbacks = callbacks
        self.advancement = 0.0

    '''Retourne True si l'animation est finie, False sinon'''

    def AnimationFinished(self) -> bool:
        return self.currentAnimation is None or (self.advancement >= 1.0 and not self.currentAnimation.loop)

    # ------------------------------------------------------------------------------------------------------------------

    '''Affiche l'animation en cours de lecture'''

    def Display(self, screen, position: tuple[int, int]) -> None:
        if self.currentAnimation is None:
            return

        frameToDisplayIndex = min(math.floor(
            self.advancement * len(self.currentAnimation.frames)), len(self.currentAnimation.frames) - 1)
        frameToDisplay = self.currentAnimation.frames[frameToDisplayIndex]

        offset = (frameToDisplay.get_width() * self.currentAnimation.topleft[0],
                  frameToDisplay.get_height() * self.currentAnimation.topleft[1])

        screen.blit(frameToDisplay,
                    (position[0] - offset[0], position[1] - offset[1]))

    '''Met a jour l'animation l'avancee de l'animation en cours de lecture'''

    def Update(self, deltaTime: float) -> None:
        if self.currentAnimation is None:
            return

        if self.callbacks is not None and len(self.callbacks) > 0:
            for callback in self.callbacks:
                if self.advancement >= callback[1]:
                    callback[0]()
                    if self.callbacks is not None:
                        self.callbacks.remove(callback)

        if self.advancement >= 1:
            if self.currentAnimation.loop:
                self.advancement = 0.0
            else:
                return

        self.advancement += deltaTime / \
            len(self.currentAnimation.frames) / self.currentAnimation.length
