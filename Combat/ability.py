import math
import random

import pygame
from Base.animation import Animation
import Base.gridManager as gridManager
import Sound.audio as audio


class Ability:
    '''Classe qui permet de gérer une attaque d'une entite. ex: attaque au corps a corps, attaque a distance, etc...'''

    def __init__(self, damageRange: tuple[int, int], abilitySpeedRange: tuple[int, int], missChance: float,
                 upAnimation: Animation, downAnimation: Animation, leftAnimation: Animation, rightAnimation: Animation,
                 damageSounds : pygame.mixer.Sound = [], applyAttackAnimAdvancement: float = 1,cooldown:int = 0, enemyPredictPlayerAbility : bool = True,
                 idleAbilityIcon: pygame.Surface = None, hoverAbilityIcon: pygame.Surface = None, clickedAbilityIcon: pygame.Surface = None) -> None:
        # Damage range: =0,0 no damage, >0,0 damage, <0,0 heal
        self.upAnimation = upAnimation
        self.downAnimation = downAnimation
        self.leftAnimation = leftAnimation
        self.rightAnimation = rightAnimation

        self.damageRange = damageRange
        self.abilitySpeedRange = abilitySpeedRange
        self.missChance = missChance

        self.damageSounds = damageSounds

        self.applyAttackAnimAdvancement = applyAttackAnimAdvancement

        self.cooldown = cooldown
        self.currentCooldown = 0

        self.enemyPredictPlayerAbility = enemyPredictPlayerAbility

        self.idleAbilityIcon = idleAbilityIcon
        self.hoverAbilityIcon = hoverAbilityIcon
        self.clickedAbilityIcon = clickedAbilityIcon

    def GetDamage(self) -> int:
        '''Retourne les degats de l'attaque en fonction de la range de degats aleatoirement'''
        return random.randint(self.damageRange[0], self.damageRange[1])

    def Missed(self) -> bool:
        '''Retourne si l'attaque a rate ou non en fonction de la chance de rate aleatoirement'''
        return random.random() < self.missChance

    def GetSpeed(self) -> int:
        '''Retourne la vitesse de l'attaque en fonction de la range de vitesse aleatoirement'''
        return random.randint(self.abilitySpeedRange[0], self.abilitySpeedRange[1])

    def GetEnemyAttackShape(self, enemyPositon: tuple[int, int], playerPosition: tuple[int, int], entityPositions: list[tuple[int, int]]) -> gridManager.GridShape:
        '''Retourne la forme de l'attaque d'un ennemi en fonction de la position du joueur et de la position de l'enemie'''
        pass

    # list[tuple[shape, color, position]]
    def GetPlayerPreviewShapes(self, playerPosition: tuple[int, int], mousePositon: tuple[int, int], entityPositions: list[tuple[int, int]]) -> list[gridManager.GridShape]:
        '''Retourne les formes de la previsualisation de l'attaque d'un joueur en fonction de la position du joueur et de la position de la souris'''
        pass

    def GetPlayerAttackShape(self, playerPosition: tuple[int, int], mousePositon: tuple[int, int], entityPositions: list[tuple[int, int]]) -> gridManager.GridShape:
        '''Retourne la forme de l'attaque d'un joueur en fonction de la position du joueur et de la position de la souris'''
        pass

    def PlayDamageSounds(self):
        audio.PlayFromSoundList(self.damageSounds)

    def OnAbilityAnimationStarted(self, entity, shape: gridManager.GridShape, direction: str) -> None:
        pass

    def OnAbilityAnimationEnded(self, entity, shape: gridManager.GridShape, direction: str) -> None:
        pass

    def OnAbilityAttackApplied(self, entity, shape: gridManager.GridShape, direction: str) -> None:
        self.PlayDamageSounds()

    def ReduceAbilityCooldown(self) -> None:
        self.currentCooldown -= 1
        if self.currentCooldown < 0:
            self.currentCooldown = self.cooldown

    def GetAbilityDirection(self, targetPosition: tuple[int, int], position: tuple[int, int]) -> str:
        direction = [targetPosition[0] - position[0],
                     -(targetPosition[1] - position[1])]
        return gridManager.GetGridDirection(direction)

    def GetAnimation(self, direction: str) -> Animation:
        '''Retourne l'animation de l'attaque en fonction de la direction'''
        if direction == "UP":
            return self.upAnimation
        elif direction == "DOWN":
            return self.downAnimation
        elif direction == "LEFT":
            return self.leftAnimation
        elif direction == "RIGHT":
            return self.rightAnimation


class MeleeAbility(Ability):
    '''Classe qui permet de gérer une attaque au corps a corps: il y a 4 directions possibles'''

    def __init__(self, damageRange: tuple[int, int], abilitySpeedRange: tuple[int, int], missChance: float,
                 upAnimation: Animation, downAnimation: Animation, leftAnimation: Animation, rightAnimation: Animation,
                 shapeUp: list[str], shapeDown: list[str], shapeLeft: list[str], shapeRight: list[str],
                 shapeColor: tuple[int, int, int], damageSounds: pygame.mixer.Sound = [], applyAttackAnimAdvancement: float = 1, cooldown: int = 0, enemyPredictPlayerAbility: bool = True,
                 idleAbilityIcon: pygame.Surface = None, hoverAbilityIcon: pygame.Surface = None, clickedAbilityIcon: pygame.Surface = None):
        super().__init__(damageRange, abilitySpeedRange, missChance, upAnimation, downAnimation, leftAnimation, rightAnimation,
                         damageSounds,applyAttackAnimAdvancement, cooldown, enemyPredictPlayerAbility, idleAbilityIcon, hoverAbilityIcon, clickedAbilityIcon)
        self.shapeUp = shapeUp
        self.shapeDown = shapeDown
        self.shapeLeft = shapeLeft
        self.shapeRight = shapeRight
        self.shapeColor = shapeColor

    def GetPlayerPreviewShapes(self, playerPosition: tuple[int, int], mousePositon: tuple[int, int], entityPositions: list[tuple[int, int]]) -> list[gridManager.GridShape]:
        return [self.GetMeleeAttackShape(playerPosition, mousePositon)]

    def GetPlayerAttackShape(self, playerPosition: tuple[int, int], mousePositon: tuple[int, int], entityPositions: list[tuple[int, int]]) -> gridManager.GridShape:
        return self.GetMeleeAttackShape(playerPosition, mousePositon)

    def GetEnemyAttackShape(self, enemyPositon: tuple[int, int], playerPosition: tuple[int, int], entityPositions: list[tuple[int, int]]) -> gridManager.GridShape:
        return self.GetMeleeAttackShape(enemyPositon, playerPosition)

    def GetMeleeAttackShape(self, position: tuple[int, int], targetPosition: tuple[int, int]) -> gridManager.GridShape:

        strDir = self.GetAbilityDirection(targetPosition, position)

        shapeToUse = []
        if strDir == "UP":
            shapeToUse = self.shapeUp
        elif strDir == "DOWN":
            shapeToUse = self.shapeDown
        elif strDir == "LEFT":
            shapeToUse = self.shapeLeft
        elif strDir == "RIGHT":
            shapeToUse = self.shapeRight
        
        shapePositions = gridManager.GetShapePositions(shapeToUse,position)
        return gridManager.GridShape(shapePositions, self.shapeColor)


class RangedAbility(Ability):
    '''Classe qui permet de gérer une attaque a distance: il y a la zone ou l'entite peut attaquer et l'AOE (Area of effect) de l'attaque'''

    def __init__(self, damageRange: tuple[int, int], abilitySpeedRange: tuple[int, int], missChance: float,
                 upAnimation: Animation, downAnimation: Animation, leftAnimation: Animation, rightAnimation: Animation,
                 zoneShape: list[str], AOEShape: list[str], zoneColor: tuple[int, int, int], AOEColor: tuple[int, int, int],
                 damageSounds: pygame.mixer.Sound = [], applyAttackAnimAdvancement: float = 1, cooldown: int = 0, enemyPredictPlayerAbility: bool = True,
                 idleAbilityIcon: pygame.Surface = None, hoverAbilityIcon: pygame.Surface = None, clickedAbilityIcon: pygame.Surface = None):

        super().__init__(damageRange, abilitySpeedRange, missChance, upAnimation, downAnimation, leftAnimation, rightAnimation,
                         damageSounds,applyAttackAnimAdvancement, cooldown, enemyPredictPlayerAbility, idleAbilityIcon, hoverAbilityIcon, clickedAbilityIcon)
        self.zoneShape = zoneShape
        self.AOEShape = AOEShape
        self.zoneColor = zoneColor
        self.AOEColor = AOEColor

    def GetPlayerPreviewShapes(self, playerPosition: tuple[int, int], mousePositon: tuple[int, int], entityPositions: list[tuple[int, int]]) -> list[gridManager.GridShape]:
        zoneShape = self.GetZoneShape(playerPosition, entityPositions)
        return [zoneShape, self.GetAOEShape(zoneShape,playerPosition, mousePositon, entityPositions)]

    def GetPlayerAttackShape(self, playerPosition: tuple[int, int], mousePositon: tuple[int, int], entityPositions: list[tuple[int, int]]) -> gridManager.GridShape:
        zoneShape = self.GetZoneShape(playerPosition, entityPositions)
        return self.GetAOEShape(zoneShape,playerPosition, mousePositon, entityPositions)

    def GetEnemyAttackShape(self, enemyPositon: tuple[int, int], playerPosition: tuple[int, int], entityPositions: list[tuple[int, int]]) -> gridManager.GridShape:
        zoneShape = self.GetZoneShape(enemyPositon, entityPositions)
        return self.GetAOEShape(zoneShape,enemyPositon, playerPosition, entityPositions)
    
    def GetZoneShape(self, position: tuple[int, int], entityPositions: list[tuple[int, int]]) -> gridManager.GridShape:
        return gridManager.GridShape(gridManager.GetShapePositions(self.zoneShape, position),self.zoneColor)

    def GetAOEShape(self,zoneShape : gridManager.GridShape, position: tuple[int, int], targetPosition: tuple[int, int], entityPositions: list[tuple[int, int]]) -> gridManager.GridShape:
        """Retourne la forme de l'AOE de l'attaque d'un joueur en fonction de la position du joueur et de la position de la souris"""

        if zoneShape.shapePositions == []:
            return None

        # get closest AOE position to mouse in zone

        closestPositonIndex = 0
        smallestDistanceNorm = 9999999
        for i in range(len(zoneShape.shapePositions)):
            direction = (targetPosition[0] - zoneShape.shapePositions[i][0],
                         targetPosition[1] - zoneShape.shapePositions[i][1])
            distanceNorm = math.sqrt(sum(j**2 for j in direction))
            if distanceNorm < smallestDistanceNorm:
                smallestDistanceNorm = distanceNorm
                closestPositonIndex = i
        
        shapePositions = gridManager.GetShapePositions(
            self.AOEShape, zoneShape.shapePositions[closestPositonIndex])
        return gridManager.GridShape(shapePositions, self.AOEColor)


class MovementAbility(RangedAbility):
    def __init__(self, abilitySpeedRange: tuple[int, int],
                 upAnimation: Animation, downAnimation: Animation, leftAnimation: Animation, rightAnimation: Animation,
                 zoneShape: list[str], zoneColor: tuple[int, int, int], targetColor: tuple[int, int, int],
                 damageSounds: pygame.mixer.Sound = [], applyAttackAnimAdvancement: float = 1, cooldown: int = 0, enemyPredictPlayerAbility: bool = True,
                 idleAbilityIcon: pygame.Surface = None, hoverAbilityIcon: pygame.Surface = None, clickedAbilityIcon: pygame.Surface = None):

        super().__init__((0, 0), abilitySpeedRange, 0, upAnimation, downAnimation, leftAnimation, rightAnimation, zoneShape, ["F"],
                         zoneColor, targetColor, damageSounds, applyAttackAnimAdvancement, cooldown, enemyPredictPlayerAbility, idleAbilityIcon, hoverAbilityIcon, clickedAbilityIcon)

    def OnAbilityAttackApplied(self, entity, shape: gridManager.GridShape, direction: str) -> None:
        self.PlayDamageSounds()

        if shape is None or shape.shapePositions is None or shape.color is None:
            return
        newPos = random.choice(shape.shapePositions)
        entity.gridPosition = newPos
    
    def GetZoneShape(self, position: tuple[int, int], entityPositions: list[tuple[int, int]]) -> gridManager.GridShape:
        newZone = gridManager.GetShapePositions(self.zoneShape, position)

        for entityPosition in entityPositions:
            if entityPosition in newZone:
                newZone.remove(entityPosition)

        return gridManager.GridShape(newZone, self.zoneColor)
