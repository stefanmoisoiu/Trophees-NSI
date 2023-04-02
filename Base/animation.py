import math
import pygame
import Base.gridManager as gridManager


class Animation:
    '''Classe qui permet de gérer une animation, ex: marcher, courir, sauter, etc...'''

    def __init__(self, spriteSheet: pygame.Surface, length: float = 1, loop: bool = True, horizontalFrames: int = 1, verticalFrames: int = 1, flip: bool = False, scale: float = 1.0, topleft: tuple[int, int] = (0, 0)) -> None:
        self.spriteSheet = spriteSheet
        self.horizontalFrames = horizontalFrames
        self.verticalFrames = verticalFrames
        self.loop = loop
        self.length = length
        self.topleft = topleft
        self.frames = GenerateAnimationFrames(
            spriteSheet, horizontalFrames, verticalFrames, flip, scale)


def GenerateAnimationFrames(spriteSheet: pygame.Surface, horizontalFrames: int, verticalFrames: int, flip: bool, scale: float = 1.0) -> list[pygame.Surface]:
    '''Decoupe le spriteSheet en plusieurs frames et les retourne dans une liste de surfaces'''

    frames = []
    frameWidth = spriteSheet.get_width() / horizontalFrames
    frameHeight = spriteSheet.get_height() / verticalFrames

    for i in range(verticalFrames):
        for j in range(horizontalFrames):

            frame = spriteSheet.subsurface(
                (j/horizontalFrames * spriteSheet.get_width(), i/verticalFrames * spriteSheet.get_height(), frameWidth, frameHeight))
            frame = pygame.transform.scale(
                frame, (int(frameWidth*scale), int(frameHeight*scale)))
            if flip:
                frame = pygame.transform.flip(frame, True, False)

            frames.append(frame)
    return frames


class AnimationManager:
    '''Classe qui permet de gérer toutes animations d'un objet'''

    def __init__(self) -> None:
        self.currentAnimation: Animation = None
        self.advancement: float = 0.0

    def PlayAnimation(self, animation: Animation, callbacks: list[tuple[callable, float]] = None) -> None:
        '''Change l'animation qui est en cours de lecture et execute des fonctions a un avancement donne dans la PREMIERE boucle si elle est specifiee'''

        self.currentAnimation = animation
        self.callbacks = callbacks
        self.advancement = 0.0

    def AnimationFinished(self) -> bool:
        '''Retourne True si l'animation est finie, False sinon'''

        return self.currentAnimation is None or (self.advancement >= 1.0 and not self.currentAnimation.loop)

    # ------------------------------------------------------------------------------------------------------------------

    def Display(self, screen, position: tuple[int, int]) -> None:
        '''Affiche l'animation en cours de lecture'''

        if self.currentAnimation is None:
            return

        frameToDisplayIndex = min(math.floor(
            self.advancement * len(self.currentAnimation.frames)), len(self.currentAnimation.frames) - 1)
        frameToDisplay = self.currentAnimation.frames[frameToDisplayIndex]

        offset = (frameToDisplay.get_width() * self.currentAnimation.topleft[0],
                  frameToDisplay.get_height() * self.currentAnimation.topleft[1])

        screen.blit(frameToDisplay,
                    (position[0] - offset[0], position[1] - offset[1]))

    def Update(self, deltaTime: float) -> None:
        '''Met a jour l'animation l'avancee de l'animation en cours de lecture'''

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
