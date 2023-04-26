import pygame


class Dialogue:
    def __init__(self, speakers: list[tuple[str, pygame.Surface]], dialogue: list[tuple[str, str]]) -> None:
        self.speakers = speakers
        # Speakers exemple : [("Cephale", pygame.image.load("cephale-icon.png")),("Guarde 1", pygame.image.load("guarde-icon.png"))]
        self.dialogue = dialogue
        # Dialogue exemple : [("Guarde 1","Halte !"), ("Cephale", "Vous ne m'attraperez pas !")]
