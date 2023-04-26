import pygame
import dialogueManager

test1_speakers = [("Cephale", pygame.image.load("Sprites/Entities/Player/icon.png")),
                  ("Guarde", pygame.image.load("Sprites/Entities/Enemy/guarde-icon.png"))]
test1_dialogue = [
    ("Guarde", "Halte, arretez vous !"),
    ("Cephale", "Vous ne m'attraperez jamais !")
]
test1 = dialogueManager.Dialogue(test1_speakers, test1_dialogue)
