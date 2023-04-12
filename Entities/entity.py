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

        self.onDamage = []
        self.onDamageValueless = []
        self.onDeath = []

    def Damage(self, damage: int) -> None:
        '''Inflige des degats a l'entite'''

        print(f"{self.properties.name} took {damage} damage")

        self.health -= damage
        for callback in self.onDamage:
            callback(self, damage)
        for callback in self.onDamageValueless:
            callback()

    def Display(self, screen) -> None:
        '''Affiche l'entite sur l'ecran'''

        self.properties.animationManager.Display(
            screen, self.rect.topleft)

    def Update(self, deltaTime: float) -> None:
        '''Met a jour l'entite, ex: animation, position, etc...'''

        self.properties.animationManager.Update(deltaTime)
        self.rect.topleft = gridManager.GetWorldPosition(self.gridPosition)

    def GetEnemyAbility(self, playerPosition: tuple[int, int]) -> Ability:
        '''Retourne l'attaque de l'ennemi en fonction de la position du joueur'''

        for i in range(len(self.properties.abilities) -1):
            if self.properties.abilities[i].currentCooldown > 0:
                self.properties.abilities[i].ReduceAbilityCooldown()
                continue
            self.properties.abilities[i].ReduceAbilityCooldown()

            abilityGridShape = self.properties.abilities[i].GetEnemyAttackShape(
                self.gridPosition, playerPosition)
            abilityPositions = gridManager.GetShapePositions(
                abilityGridShape.shape, abilityGridShape.position)
            if playerPosition in abilityPositions:
                return self.properties.abilities[i]
        
        if self.properties.abilities[-1].currentCooldown > 0:
            self.properties.abilities[-1].ReduceAbilityCooldown()
            return None
        return self.properties.abilities[-1]
