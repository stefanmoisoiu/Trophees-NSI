import math
import random
from Base.animation import Animation
import Base.gridManager as gridManager

'''Classe qui permet de gérer une attaque d'une entite. ex: attaque au corps a corps, attaque a distance, etc...'''


class Ability:
    def __init__(self, animation: Animation, damageRange: tuple[int, int]):
        # Damage range: =0,0 no damage, >0,0 damage, <0,0 heal
        self.damageRange = damageRange
        self.animation = animation

    '''Retourne les degats de l'attaque en fonction de la range de degats aleatoirement'''

    def GetDamage(self) -> int:
        return random.randint(self.damageRange[0], self.damageRange[1])

    '''Retourne la forme de l'attaque d'un ennemi en fonction de la position du joueur et de la position de l'entite qui attaque'''

    def GetEnemyShape(self, playerPosition: tuple[int, int], myPositon: tuple[int, int]) -> list[str]:
        print("To be implemented in child class")

    '''Retourne les formes de la previsualisation de l'attaque d'un joueur en fonction de la position du joueur et de la position de la souris'''

    # list[tuple[shape, color, position]]
    def GetPlayerPreviewShapes(self, playerPosition: tuple[int, int], mousePositon: tuple[int, int]) -> list[tuple[list[str], tuple[int, int, int], tuple[int, int]]]:
        print("To be implemented in child class")

    '''Retourne la forme de l'attaque d'un joueur en fonction de la position du joueur et de la position de la souris'''

    def GetPlayerAttackShape(self, playerPosition: tuple[int, int], mousePositon: tuple[int, int]) -> tuple[list[str], tuple[int, int, int], tuple[int, int]]:
        print("To be implemented in child class")


'''Classe qui permet de gérer une attaque au corps a corps: il y a 4 directions possibles'''


class MeleeAbility(Ability):
    def __init__(self, animation: Animation, damageRange: tuple[int, int], shapeUp: list[str], shapeDown: list[str], shapeLeft: list[str], shapeRight: list[str], previewColor: tuple[int, int, int]):
        super().__init__(animation, damageRange)
        self.shapeUp = shapeUp
        self.shapeDown = shapeDown
        self.shapeLeft = shapeLeft
        self.shapeRight = shapeRight
        self.previewColor = previewColor

    def GetPlayerPreviewShapes(self, playerPosition: tuple[int, int], mousePositon: tuple[int, int]) -> list[tuple[list[str], tuple[int, int, int], tuple[int, int]]]:
        return [self.GetPlayerMeleeAttackShape(playerPosition, mousePositon)]

    def GetPlayerAttackShape(self, playerPosition: tuple[int, int], mousePositon: tuple[int, int]) -> tuple[list[str], tuple[int, int, int], tuple[int, int]]:
        return self.GetPlayerMeleeAttackShape(playerPosition, mousePositon)

    def GetPlayerMeleeAttackShape(self, playerPosition: tuple[int, int], mouseGridPositon: tuple[int, int]) -> tuple[list[str], tuple[int, int, int]]:
        direction = [mouseGridPositon[0] - playerPosition[0],
                     -(mouseGridPositon[1] - playerPosition[1])]

        if direction[0] >= 0:
            if direction[1] >= direction[0]:
                return (self.shapeUp, self.previewColor, playerPosition)
            elif direction[1] <= -direction[0]:
                return (self.shapeDown, self.previewColor, playerPosition)
            else:
                return (self.shapeRight, self.previewColor, playerPosition)
        else:
            if direction[1] >= -direction[0]:
                return (self.shapeUp, self.previewColor, playerPosition)
            elif direction[1] <= direction[0]:
                return (self.shapeDown, self.previewColor, playerPosition)
            else:
                return (self.shapeLeft, self.previewColor, playerPosition)


'''Classe qui permet de gérer une attaque a distance: il y a la zone ou l'entite peut attaquer et l'AOE (Area of effect) de l'attaque'''


class RangedAbility(Ability):
    def __init__(self, animation: Animation, damageRange: tuple[int, int], zoneShape: list[str], AOEShape: list[str], zoneColor: tuple[int, int, int], AOEColor: tuple[int, int, int]):
        super().__init__(animation, damageRange)
        self.zoneShape = zoneShape
        self.AOEShape = AOEShape
        self.zoneColor = zoneColor
        self.AOEColor = AOEColor

    def GetPlayerPreviewShapes(self, playerPosition: tuple[int, int], mousePositon: tuple[int, int]) -> list[tuple[list[str], tuple[int, int, int], tuple[int, int]]]:
        return [(self.zoneShape, self.zoneColor, playerPosition), self.GetPlayerAOEShape(playerPosition, mousePositon)]

    def GetPlayerAttackShape(self, playerPosition: tuple[int, int], mousePositon: tuple[int, int]) -> tuple[list[str], tuple[int, int, int], tuple[int, int]]:
        return self.GetPlayerAOEShape(playerPosition, mousePositon)

    def GetPlayerAOEShape(self, playerPosition: tuple[int, int], mouseGridPositon: tuple[int, int]) -> tuple[list[str], tuple[int, int, int], tuple[int, int]]:
        # get closest AOE position to mouse in zone
        zonePositons = gridManager.GetShapePositions(
            self.zoneShape, playerPosition)

        closestPositonIndex = 0
        smallestDistanceNorm = 9999999
        for i in range(len(zonePositons)):
            direction = (mouseGridPositon[0] - zonePositons[i][0],
                         mouseGridPositon[1] - zonePositons[i][1])
            distanceNorm = math.sqrt(sum(j**2 for j in direction))
            if distanceNorm < smallestDistanceNorm:
                smallestDistanceNorm = distanceNorm
                closestPositonIndex = i
        return (self.AOEShape, self.AOEColor, zonePositons[closestPositonIndex])
