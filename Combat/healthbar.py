import pygame
import math


class Healthbar:
    '''Display a healthbar on the screen'''
    def __init__(self, size: tuple[int, int], direction: str, offsetFromPos: tuple[int, int] = (0, 0), fullColor: tuple[int, int, int] = (0, 255, 0), emptyColor: tuple[int, int, int] = (255, 0, 0)) -> None:
        self.size = size
        self.fullColor = fullColor
        self.emptyColor = emptyColor
        self.offsetFromPos = offsetFromPos
        self.direction = direction
        self.percentage = 1

        # Healthbar Directions:
        # R to L
        # L to R
        # U to D
        # D to U

    def SetPercentage(self, newPercentage: float):
        '''Set the percentage of the healthbar'''
        self.percentage = newPercentage

    def GetFullHealthbar(self) -> tuple[int, int, int, int]:
        '''Get the full healthbar'''
        if self.direction == "R to L":
            return (0, 0, self.size[0] * self.percentage, self.size[1])
        if self.direction == "L to R":
            return (self.size[0] * (1-self.percentage), 0, self.size[0] * self.percentage, self.size[1])
        if self.direction == "U to D":
            return (0, 0, self.size[0], self.size[1] * self.percentage)
        if self.direction == "D to U":
            return (0, self.size[1] * (1-self.percentage), self.size[0], self.size[1] * self.percentage)
        print("Invalid Healthbar Direction !")
        return (0, 0, 0, 0)

    def Display(self, screen: pygame.Surface, pos: tuple[int, int]):
        '''Display the healthbar on the screen at the center of a given position + offset'''

        emptyHealthbarRect = pygame.Rect(
            pos[0] + self.offsetFromPos[0] - self.size[0] / 2, pos[1] + self.offsetFromPos[1] - self.size[1] / 2, self.size[0], self.size[1])
        pygame.draw.rect(screen, self.emptyColor, emptyHealthbarRect)

        fullHealthbarInfo = self.GetFullHealthbar()
        fullHealthbarRect = pygame.Rect(math.ceil(pos[0] + self.offsetFromPos[0] + fullHealthbarInfo[0] - self.size[0] / 2),
                                        math.ceil(
                                            pos[1] + self.offsetFromPos[1] + fullHealthbarInfo[1] - self.size[1] / 2),
                                        fullHealthbarInfo[2], fullHealthbarInfo[3])
        pygame.draw.rect(screen, self.fullColor, fullHealthbarRect)
