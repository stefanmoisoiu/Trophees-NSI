import pygame
from Base.animation import Animation, AnimationManager
from Combat.ability import Ability
import Base.gridManager as gridManager
import Combat.healthbar as healthbar
from Combat.playerAbilitiesUI import PlayerAbilitiesUI


class EntityProperties:
    '''Classe qui permet de gérer les propriétés d'une entite'''

    def __init__(self, name: str, description: str, startHealth: int, abilities: list[Ability],
                 idleAnimation: Animation,deathAnimation : Animation = None, onDamageAnimation:Animation = None) -> None:
        self.name = name
        self.startHealth = startHealth
        self.description = description

        self.idleAnimation = idleAnimation
        self.deathAnimation = deathAnimation
        self.onDamageAnimation = onDamageAnimation

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
        self.health = max(self.health,0)

        for callback in self.onDamage:
            callback(self, damage)
        for callback in self.onDamageValueless:
            callback()
        
        if self.health == 0:
            for callback in self.onDeath:
                callback(self)

    def Display(self, screen) -> None:
        '''Affiche l'entite sur l'ecran'''

        self.properties.animationManager.Display(
            screen, self.rect.topleft)

    def Update(self, deltaTime: float) -> None:
        '''Met a jour l'entite, ex: animation, position, etc...'''

        self.properties.animationManager.Update(deltaTime)
        self.rect.topleft = gridManager.GetWorldPosition(self.gridPosition)

    def GetEnemyAbility(self, playerPosition: tuple[int, int], entityPositions : list[tuple[int,int]]) -> Ability:
        '''Retourne l'attaque de l'ennemi en fonction de la position du joueur'''

        for i in range(len(self.properties.abilities) -1):
            
            if self.properties.abilities[i].currentCooldown > 0:
                self.properties.abilities[i].ReduceAbilityCooldown()
                continue
            self.properties.abilities[i].ReduceAbilityCooldown()

            abilityGridShape = self.properties.abilities[i].GetEnemyAttackShape(
                self.gridPosition, playerPosition, entityPositions)

            if playerPosition in abilityGridShape.shapePositions:
                return self.properties.abilities[i]
        
        if self.properties.abilities[-1].currentCooldown > 0:
            self.properties.abilities[-1].ReduceAbilityCooldown()
            return None
        return self.properties.abilities[-1]

def CreatePlayer(playerProperties : EntityProperties, gridPosition : tuple[int,int]):
    player = Entity(playerProperties, gridPosition=gridPosition)

    playerHealthbar = healthbar.CreateEntityHealthbar(player)
    __BindEntityFightAnimations(player, playerProperties)

    playerAbilitiesUI = PlayerAbilitiesUI(player, 1)
    playerAbilitiesUI.GenerateAbilityButtons()

    return (player,playerHealthbar,playerAbilitiesUI)

def CreateEnemy(enemyProperties: EntityProperties, gridPosition: tuple[int, int]):
    enemy = Entity(enemyProperties, gridPosition=gridPosition)

    enemyHealthbar = healthbar.CreateEntityHealthbar(enemy)
    __BindEntityFightAnimations(enemy, enemyProperties)

    return (enemy,enemyHealthbar)

def __BindEntityFightAnimations(entity : Entity, entityProperties : EntityProperties):
    if entityProperties.onDamageAnimation is not None:
        entity.onDamage += entityProperties.animationManager.PlayAnimation(entityProperties.onDamageAnimation,
                                                                           [(lambda: entityProperties.animationManager.PlayAnimation(entityProperties.idleAnimation), 1)])
    if entityProperties.deathAnimation is not None:
        entity.onDamage += entityProperties.animationManager.PlayAnimation(
            entityProperties.deathAnimation)
