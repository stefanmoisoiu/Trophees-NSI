import math
import pygame

'''Classe qui permet de gérer une animation, ex: marcher, courir, sauter, etc...'''


class Animation:
    def __init__(self, spriteSheet: pygame.Surface, length: float = 1, loop: bool = True, horizontalFrames: int = 1, verticalFrames: int = 1) -> None:
        self.spriteSheet = spriteSheet
        self.horizontalFrames = horizontalFrames
        self.verticalFrames = verticalFrames
        self.loop = loop
        self.length = length
        self.frames = GenerateAnimationFrames(
            spriteSheet, horizontalFrames, verticalFrames)


'''Decoupe le spriteSheet en plusieurs frames et les retourne dans une liste de surfaces'''


def GenerateAnimationFrames(spriteSheet: pygame.Surface, horizontalFrames: int, verticalFrames: int) -> list[pygame.Surface]:
    frames = []
    frameWidth = spriteSheet.get_width() / horizontalFrames
    frameHeight = spriteSheet.get_height() / verticalFrames

    for i in range(verticalFrames):
        for j in range(horizontalFrames):
            frames.append(spriteSheet.subsurface(
                (j/horizontalFrames * spriteSheet.get_width(), i/verticalFrames * spriteSheet.get_height(), frameWidth, frameHeight)))
    return frames


'''Classe qui permet de gérer toutes animations d'un objet'''


class AnimationManager:
    def __init__(self) -> None:
        self.currentAnimation: Animation = None
        self.advancement: float = 0.0

    '''Change l'animation qui est en cours de lecture et execute une fonction a la fin de la PREMIERE boucle si elle est specifiee'''

    def PlayAnimation(self, animation: Animation, onFinishCallback: callable = None) -> None:
        self.currentAnimation = animation
        self.onFinishCallback = onFinishCallback
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

        screen.blit(frameToDisplay, position)

    '''Met a jour l'animation l'avancee de l'animation en cours de lecture'''

    def Update(self, deltaTime: float) -> None:
        if self.currentAnimation is None:
            return

        if self.advancement >= 1.0:
            if self.onFinishCallback is not None:
                self.onFinishCallback()
                self.onFinishCallback = None

            if self.currentAnimation.loop:
                self.advancement = 0.0
            else:
                return

        self.advancement += deltaTime / \
            len(self.currentAnimation.frames) / self.currentAnimation.length
