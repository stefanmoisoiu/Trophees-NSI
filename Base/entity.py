import pygame
from Base.animation import Animation, AnimationManager
from Combat.ability import Ability
import Base.gridManager as gridManager

class EntityProperties:
    '''Classe qui permet de gérer les propriétés d'une entite'''
    def __init__(self, name: str, description: str, startHealth: int, abilities: list[Ability], idleAnimation: Animation) -> None:
        self.name = name
        self.startHealth = startHealth
        self.description = description
        self.idleAnimation = idleAnimation
        self.animationManager = AnimationManager()
        self.animationManager.PlayAnimation(self.idleAnimation)
        self.abilities = abilities


class Entity:
    '''Classe qui permet de gérer une entite dans le jeu, ex: joueur, ennemi'''
    
    def __init__(self, properties: EntityProperties, gridPosition: tuple[int, int] = (0, 0)) -> None:
        self.properties = properties
        self.gridPosition = gridPosition
        self.rect = pygame.Rect(
            gridPosition[0] * gridManager.gridPixelSize, gridPosition[1] * gridManager.gridPixelSize, gridManager.gridPixelSize, gridManager.gridPixelSize)
        self.health = self.properties.startHealth

    

    def Display(self, screen) -> None:
        '''Affiche l'entite sur l'ecran'''
        
        self.properties.animationManager.Display(
            screen, self.rect.topleft)

    

    def Update(self, deltaTime: float) -> None:
        '''Met a jour l'entite, ex: animation, position, etc...'''
        
        self.properties.animationManager.Update(deltaTime)
        self.rect.topleft = gridManager.GetWorldPosition(self.gridPosition)
