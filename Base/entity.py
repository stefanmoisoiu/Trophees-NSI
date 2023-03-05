import pygame
from Base.animation import Animation, AnimationManager
from Combat.ability import Ability
import Base.gridManager as gridManager

'''Classe qui permet de gérer les propriétés d'une entite'''


class EntityProperties:
    def __init__(self, name: str, description: str, startHealth: int, abilities: list[Ability], idleAnimation: Animation) -> None:
        self.name = name
        self.startHealth = startHealth
        self.description = description
        self.idleAnimation = idleAnimation
        self.animationManager = AnimationManager()
        self.animationManager.PlayAnimation(self.idleAnimation)
        self.abilities = abilities


'''Classe qui permet de gérer une entite dans le jeu, ex: joueur, ennemi'''


class Entity:
    def __init__(self, properties: EntityProperties, gridPosition: tuple[int, int] = (0, 0)) -> None:
        self.properties = properties
        self.gridPosition = gridPosition
        self.rect = pygame.Rect(
            gridPosition[0] * gridManager.gridPixelSize, gridPosition[1] * gridManager.gridPixelSize, gridManager.gridPixelSize, gridManager.gridPixelSize)
        self.health = self.properties.startHealth

    '''Affiche l'entite sur l'ecran'''

    def Display(self, screen) -> None:
        self.properties.animationManager.Display(
            screen, self.rect.topleft)

    '''Met a jour l'entite, ex: animation, position, etc...'''

    def Update(self, deltaTime: float) -> None:
        self.properties.animationManager.Update(deltaTime)
        self.rect.topleft = gridManager.GetWorldPosition(self.gridPosition)
