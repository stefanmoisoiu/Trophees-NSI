import pygame

pygame.mixer.init()

def loadSounds(name: str, count: int):
    return [
        pygame.mixer.Sound(f"Sound/Abilities/{name}{i}.wav")
        for i in range(1, count + 1)
    ]


arrows = loadSounds("arrow", 5)
blunt = loadSounds("blunt", 2)
fireball = loadSounds("fireball", 3)
punches = loadSounds("punch", 3)
sword = loadSounds("sword", 3)
