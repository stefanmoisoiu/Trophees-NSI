import math
import pygame

gridPixelSize = 64
gridOutlineSprite = pygame.transform.scale(
    pygame.image.load("Sprites/Grid/Grid Outline.png"),
    (gridPixelSize, gridPixelSize))

gridCellSprite = pygame.transform.scale(pygame.image.load(
    "Sprites/Grid/Grid Cell.png"), (gridPixelSize, gridPixelSize))

cellsToAdd: list[tuple[tuple[int, int], tuple[int, int, int]]] = []


class GridShape:
    '''Classe qui permet de gérer les formes de la grille'''
    def __init__(self, shapePositions : tuple[int,int], color: tuple[int, int, int]) -> None:
        self.shapePositions = shapePositions
        self.color = color



def GetGridPosition(position: tuple[int, int]) -> tuple[int, int]:
    '''Retourne la position transformee en coordonnees de la grille'''
    return (math.floor(position[0] / gridPixelSize), math.floor(position[1] / gridPixelSize))


def GetGridDirection(direction: tuple[int, int]) -> str:
    '''Retourne la direction transformee en direction de la grille'''
    if direction[0] >= 0:
        if direction[1] >= direction[0]:
            return "UP"
        elif direction[1] <= -direction[0]:
            return "DOWN"
        else:
            return "RIGHT"
    else:
        if direction[1] >= -direction[0]:
            return "UP"
        elif direction[1] <= direction[0]:
            return "DOWN"
        else:
            return "LEFT"





def GetWorldPosition(position: tuple[float, float]) -> tuple[float, float]:
    '''Retourne la position transformee en coordonnees du monde'''
    return (position[0] * gridPixelSize, position[1] * gridPixelSize)

def DrawGridOutline(screen: pygame.Surface):
    '''Affiche la grille des cellules sur l'ecran'''
    # get screen in grid coordinates
    topleft = (math.floor(screen.get_rect().left / gridPixelSize),
               math.floor(screen.get_rect().top / gridPixelSize))
    size = (math.ceil(screen.get_width() / gridPixelSize),
            math.ceil(screen.get_height() / gridPixelSize))

    # draw grid outline
    for i in range(size[0]):
        for j in range(size[1]):
            screen.blit(gridOutlineSprite,
                        ((topleft[0] + i) * gridPixelSize, (topleft[1] + j) * gridPixelSize))


def GetShapePositions(shape: list[str], gridOffset: tuple[int, int] = (0, 0)) -> list[tuple[int, int]]:
    '''Retourne la position des cellules de la grille'''
    cellPositions: list[tuple[int, int]] = []
    anchorPos: tuple[int, int] = (0, 0)
    for y in range(len(shape)):
        for x in range(len(shape[y])):
            if shape[y][x] in ["F", "O"]:
                cellPositions.append((x, y))
            if shape[y][x] in ["C", "O"]:
                anchorPos = (x, y)

    for i in range(len(cellPositions)):
        cellPositions[i] = (cellPositions[i][0] - anchorPos[0] + gridOffset[0],
                            cellPositions[i][1] - anchorPos[1] + gridOffset[1])
    return cellPositions





def AddShape(shape: GridShape):
    '''Ajoute une forme a la liste des cellules a ajouter. La forme est une liste de strings, chaque string represente une ligne de la forme.
    Chaque caractere de la string represente un pixel de la forme.
    Les caracteres possibles sont: F = rempli, C = centre, O = centre rempli'''

    for cellPosition in shape.shapePositions:
        cellsToAdd.append((cellPosition, shape.color))




def DrawCells(screen: pygame.Surface):
    '''Affiche les cellules a ajouter sur l'ecran'''
    
    for cell in cellsToAdd:
        spriteToCreate = gridCellSprite.copy()
        spriteToCreate.fill(cell[1],
                            None, pygame.BLEND_RGBA_MULT)

        screen.blit(spriteToCreate, GetWorldPosition(cell[0]))
    cellsToAdd.clear()
