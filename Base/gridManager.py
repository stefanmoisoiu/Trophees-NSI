import math
import pygame

gridOutlineSprite = pygame.image.load("Sprites/Grid/Grid Outline.png")
gridCellSprite = pygame.image.load("Sprites/Grid/Grid Cell.png")
gridPixelSize = 32

cellsToAdd: list[tuple[tuple[int, int], tuple[int, int, int]]] = []

'''Retourne la position transformee en coordonnees de la grille'''


def GetGridPosition(position: tuple[int, int]) -> tuple[int, int]:
    return (math.floor(position[0] / gridPixelSize), math.floor(position[1] / gridPixelSize))


'''Retourne la position transformee en coordonnees du monde'''


def GetWorldPosition(position: tuple[int, int]) -> tuple[int, int]:
    return (position[0] * gridPixelSize, position[1] * gridPixelSize)


'''Affiche la grille des cellules sur l'ecran'''


def DrawGridOutline(screen: pygame.Surface):
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
    cellPositions: list[tuple[int, int]] = []
    anchorPos: tuple[int, int] = (0, 0)
    for j in range(len(shape)):
        for i in range(len(shape[j])):
            if shape[i][j] in ["F", "O"]:
                cellPositions.append((j, i))
            if shape[i][j] in ["C", "O"]:
                anchorPos = (j, i)

    for i in range(len(cellPositions)):
        cellPositions[i] = (cellPositions[i][0] - anchorPos[0] + gridOffset[0],
                            cellPositions[i][1] - anchorPos[1] + gridOffset[1])
    return cellPositions


'''Ajoute une forme a la liste des cellules a ajouter. La forme est une liste de strings, chaque string represente une ligne de la forme. Chaque caractere de la string represente un pixel de la forme. Les caracteres possibles sont: F = filled grid cell, C = center of the shape, O = filled center of the shape.'''


def AddShape(shape: list[str], color: tuple[int, int, int], gridOffset: tuple[int, int] = (0, 0)):
    global cellsToAdd
    # example shape:
    # shape = ["FFF",
    #          "FCF",
    #          "FFF"]

    cellPositions: list[tuple[int, int]] = GetShapePositions(shape, gridOffset)

    for cellPosition in cellPositions:
        cellsToAdd.append((cellPosition, color))


'''Affiche les cellules a ajouter sur l'ecran'''


def DrawCells(screen: pygame.Surface):
    for cell in cellsToAdd:
        spriteToCreate = gridCellSprite.copy()
        spriteToCreate.fill(cell[1],
                            None, pygame.BLEND_RGBA_MULT)

        screen.blit(spriteToCreate, GetWorldPosition(cell[0]))
    cellsToAdd.clear()
