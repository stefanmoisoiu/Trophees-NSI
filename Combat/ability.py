import math
import random

import pygame
from Base.animation import Animation
import Base.gridManager as gridManager




class Ability:
    '''Classe qui permet de gérer une attaque d'une entite. ex: attaque au corps a corps, attaque a distance, etc...'''
    
    def __init__(self, damageRange: tuple[int, int], abilitySpeedRange: tuple[int, int], missChance: float, upAnimation: Animation, downAnimation: Animation, leftAnimation: Animation, rightAnimation: Animation,
                 applyAttackAnimAdvancement: float = 1, idleAbilityIcon: pygame.Surface = None, hoverAbilityIcon: pygame.Surface = None, clickedAbilityIcon: pygame.Surface = None) -> None:
        # Damage range: =0,0 no damage, >0,0 damage, <0,0 heal
        self.upAnimation = upAnimation
        self.downAnimation = downAnimation
        self.leftAnimation = leftAnimation
        self.rightAnimation = rightAnimation

        self.damageRange = damageRange
        self.abilitySpeedRange = abilitySpeedRange
        self.missChance = missChance
        self.applyAttackAnimAdvancement = applyAttackAnimAdvancement
        self.idleAbilityIcon = idleAbilityIcon
        self.hoverAbilityIcon = hoverAbilityIcon
        self.clickedAbilityIcon = clickedAbilityIcon

    

    def GetDamage(self) -> int:
        '''Retourne les degats de l'attaque en fonction de la range de degats aleatoirement'''
        
        print(self.damageRange)
        return random.randint(self.damageRange[0], self.damageRange[1])

    def Missed(self) -> bool:
        return random.random() < self.missChance

    def GetSpeed(self) -> int:
        '''Retourne la vitesse de l'attaque en fonction de la range de vitesse aleatoirement'''
        
        return random.randint(self.abilitySpeedRange[0], self.abilitySpeedRange[1])


    def GetEnemyAttackShape(self, enemyPositon: tuple[int, int], playerPosition: tuple[int, int]) -> gridManager.GridShape:
        '''Retourne la forme de l'attaque d'un ennemi en fonction de la position du joueur et de la position de l'entite qui attaque'''
        
        pass

    # list[tuple[shape, color, position]]
    def GetPlayerPreviewShapes(self, playerPosition: tuple[int, int], mousePositon: tuple[int, int]) -> list[gridManager.GridShape]:
        '''Retourne les formes de la previsualisation de l'attaque d'un joueur en fonction de la position du joueur et de la position de la souris'''
        
        pass

    def GetPlayerAttackShape(self, playerPosition: tuple[int, int], mousePositon: tuple[int, int]) -> gridManager.GridShape:
        '''Retourne la forme de l'attaque d'un joueur en fonction de la position du joueur et de la position de la souris'''
        
        pass

    def OnAbilityAnimationStarted(self, entity, shape: gridManager.GridShape, direction: str) -> None:
        pass

    def OnAbilityAnimationEnded(self, entity, shape: gridManager.GridShape, direction: str) -> None:
        pass

    def OnAbilityAttackApplied(self, entity, shape: gridManager.GridShape, direction: str) -> None:
        pass

    def GetAbilityDirection(self, targetPosition: tuple[int, int], position: tuple[int, int]) -> str:
        direction = [targetPosition[0] - position[0],
                     -(targetPosition[1] - position[1])]
        return gridManager.GetGridDirection(direction)

    def GetAnimation(self, direction: str) -> Animation:
        print(direction)
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
                 shapeColor: tuple[int, int, int], applyAttackAnimAdvancement: float = 1,
                 idleAbilityIcon: pygame.Surface = None, hoverAbilityIcon: pygame.Surface = None, clickedAbilityIcon: pygame.Surface = None):
        super().__init__(damageRange, abilitySpeedRange, upAnimation, downAnimation, leftAnimation, rightAnimation,
                         applyAttackAnimAdvancement, idleAbilityIcon, hoverAbilityIcon, clickedAbilityIcon)
        self.shapeUp = shapeUp
        self.shapeDown = shapeDown
        self.shapeLeft = shapeLeft
        self.shapeRight = shapeRight
        self.shapeColor = shapeColor

    def GetPlayerPreviewShapes(self, playerPosition: tuple[int, int], mousePositon: tuple[int, int]) -> list[gridManager.GridShape]:
        return [self.GetMeleeAttackShape(playerPosition, mousePositon)]

    def GetPlayerAttackShape(self, playerPosition: tuple[int, int], mousePositon: tuple[int, int]) -> gridManager.GridShape:
        return self.GetMeleeAttackShape(playerPosition, mousePositon)

    def GetEnemyAttackShape(self, enemyPositon: tuple[int, int], playerPosition: tuple[int, int]) -> gridManager.GridShape:
        return self.GetMeleeAttackShape(enemyPositon, playerPosition)

    def GetMeleeAttackShape(self, position: tuple[int, int], targetPosition: tuple[int, int]) -> gridManager.GridShape:

        strDir = self.GetAbilityDirection(targetPosition, position)

        if strDir == "UP":
            return gridManager.GridShape(self.shapeUp, self.shapeColor, position)
        elif strDir == "DOWN":
            return gridManager.GridShape(self.shapeDown, self.shapeColor, position)
        elif strDir == "LEFT":
            return gridManager.GridShape(self.shapeLeft, self.shapeColor, position)
        elif strDir == "RIGHT":
            return gridManager.GridShape(self.shapeRight, self.shapeColor, position)



class RangedAbility(Ability):
    '''Classe qui permet de gérer une attaque a distance: il y a la zone ou l'entite peut attaquer et l'AOE (Area of effect) de l'attaque'''
    
    def __init__(self, damageRange: tuple[int, int], abilitySpeedRange: tuple[int, int], missChance: float,
                 upAnimation: Animation, downAnimation: Animation, leftAnimation: Animation, rightAnimation: Animation,
                 zoneShape: list[str], AOEShape: list[str], zoneColor: tuple[int, int, int], AOEColor: tuple[int, int, int],
                 applyAttackAnimAdvancement: float = 1,
                 idleAbilityIcon: pygame.Surface = None, hoverAbilityIcon: pygame.Surface = None, clickedAbilityIcon: pygame.Surface = None):

        super().__init__(damageRange, abilitySpeedRange, missChance, upAnimation, downAnimation, leftAnimation, rightAnimation,
                         applyAttackAnimAdvancement, idleAbilityIcon, hoverAbilityIcon, clickedAbilityIcon)
        self.zoneShape = zoneShape
        self.AOEShape = AOEShape
        self.zoneColor = zoneColor
        self.AOEColor = AOEColor

    def GetPlayerPreviewShapes(self, playerPosition: tuple[int, int], mousePositon: tuple[int, int]) -> list[gridManager.GridShape]:
        return [gridManager.GridShape(self.zoneShape, self.zoneColor, playerPosition), self.GetPlayerAOEShape(playerPosition, mousePositon)]

    def GetPlayerAttackShape(self, playerPosition: tuple[int, int], mousePositon: tuple[int, int]) -> gridManager.GridShape:
        return self.GetPlayerAOEShape(playerPosition, mousePositon)

    def GetEnemyAttackShape(self, enemyPositon: tuple[int, int], playerPosition: tuple[int, int]) -> gridManager.GridShape:
        return self.GetPlayerAOEShape(enemyPositon, playerPosition)

    

    def GetPlayerAOEShape(self, position: tuple[int, int], targetPosition: tuple[int, int]) -> gridManager.GridShape:
        """Retourne la forme de l'AOE de l'attaque d'un joueur en fonction de la position du joueur et de la position de la souris"""
        
        # get closest AOE position to mouse in zone
        zonePositons = gridManager.GetShapePositions(
            self.zoneShape, position)

        closestPositonIndex = 0
        smallestDistanceNorm = 9999999
        for i in range(len(zonePositons)):
            direction = (targetPosition[0] - zonePositons[i][0],
                         targetPosition[1] - zonePositons[i][1])
            distanceNorm = math.sqrt(sum(j**2 for j in direction))
            if distanceNorm < smallestDistanceNorm:
                smallestDistanceNorm = distanceNorm
                closestPositonIndex = i
        return gridManager.GridShape(self.AOEShape, self.AOEColor, zonePositons[closestPositonIndex])


class MovementAbility(RangedAbility):
    def __init__(self, abilitySpeedRange: tuple[int, int],
                 upAnimation: Animation, downAnimation: Animation, leftAnimation: Animation, rightAnimation: Animation,
                 zoneShape: list[str], AOEShape: list[str], zoneColor: tuple[int, int, int], AOEColor: tuple[int, int, int], applyAttackAnimAdvancement: float = 1,
                 idleAbilityIcon: pygame.Surface = None, hoverAbilityIcon: pygame.Surface = None, clickedAbilityIcon: pygame.Surface = None):

        super().__init__((0, 0), abilitySpeedRange, 0, upAnimation, downAnimation, leftAnimation, rightAnimation, zoneShape,
                         AOEShape, zoneColor, AOEColor, applyAttackAnimAdvancement, idleAbilityIcon, hoverAbilityIcon, clickedAbilityIcon)

    def OnAbilityAttackApplied(self, entity, shape: gridManager.GridShape, direction: str) -> None:
        shapePositions = gridManager.GetShapePositions(
            shape.shape, shape.position + entity.gridPosition)
        newPos = shapePositions[random.randint(0, len(shapePositions)-1)]
        entity.gridPosition = newPos
