import pygame
import Base.gridManager as gridManager
import Combat.combatManager as combatManager
import Base.events as events
from Base.animation import Animation
from Base.entity import Entity, EntityProperties
from Combat.ability import Ability, MeleeAbility, RangedAbility

# region Window Setup
pygame.init()

screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
pygame.display.set_caption("Jeu de role")

framerate: int = 60
clock = pygame.time.Clock()
# endregion

# region Player Setup : A DEPLACER DANS UN FICHIER DE CONFIGURATION AVEC LES DIFFERENTES CLASSES DU JOUEUR + LES ARMES ET LES ITEMS QU'ON PEUT OBTENIR
__playerIdleAnimation = Animation(pygame.image.load(
    "Sprites/Entities/Player/player test sprite.png"), loop=True, length=.25, horizontalFrames=4, verticalFrames=1)
__playerTestAnimation = Animation(pygame.image.load(
    "Sprites/Entities/Player/player test sprite.png"), loop=False, length=1, horizontalFrames=4, verticalFrames=1)


__playerMeleeUpShape = [" F ",
                        " F ",
                        " C "]
__playerMeleeDownShape = [" C ",
                          " F ",
                          " F "]
__playerMeleeLeftShape = ["   ",
                          "FFC",
                          "   "]
__playerMeleeRightShape = ["   ",
                           "CFF",
                           "   "]

__playerMeleeTestAbility = MeleeAbility(
    __playerTestAnimation, (3, 0), (3, 7), __playerMeleeUpShape, __playerMeleeDownShape, __playerMeleeLeftShape, __playerMeleeRightShape, (255, 0, 0), .5)

__playerRangedZoneShape = ["  FFF  ",
                           " FFFFF ",
                           "FFFFFFF",
                           "FFFCFFF",
                           "FFFFFFF",
                           " FFFFF ",
                           "  FFF  "]
__playerRangedAOEShape = [" F ",
                          "FOF",
                          " F "]
__playerRangedTestAbility = RangedAbility(
    __playerTestAnimation, (3, 0), (3, 7), __playerRangedZoneShape, __playerRangedAOEShape, (100, 0, 0), (255, 0, 0), .5)

__playerProperties = EntityProperties(
    "Player", "The player", [__playerMeleeTestAbility, __playerRangedTestAbility], __playerIdleAnimation)
player: Entity = Entity(__playerProperties, position=(8, 8))
# endregion

# region Game Loop
running: bool = True


def QuitGame():
    global running
    running = False
    print("Quit game")


def PlayTurnsSetup():
    playerAbilityShape = player.properties.abilities[1].GetPlayerAttackShape(
        player.position, mouseGridPos)
    combatManager.PlayTurns(
        (player, player.properties.abilities[1], playerAbilityShape), [])


events.onQuit.append(QuitGame)
events.onLeftClick.append(PlayTurnsSetup)

while running:
    # region Setup:Events,variables,etc...
    deltaTime = clock.tick(framerate) / 1000
    mouseGridPos = gridManager.GetGridPosition(pygame.mouse.get_pos())

    screen.fill((0, 0, 0))
    gridManager.DrawGridOutline(screen)

    events.CheckEvents(pygame.event.get())
    # endregion

# region Shapes
    if not combatManager.playingTurns:
        for attackPreviewShape in player.properties.abilities[1].GetPlayerPreviewShapes(
                player.position, mouseGridPos):
            gridManager.AddShape(
                attackPreviewShape[0], attackPreviewShape[1], attackPreviewShape[2])

    if combatManager.turnShape != None:
        gridManager.AddShape(
            combatManager.turnShape[0], combatManager.turnShape[1], combatManager.turnShape[2])

    gridManager.DrawCells(screen)
# endregion
# region Entities
    player.Update(deltaTime)
    player.Display(screen)
# endregion
    pygame.display.flip()
# endregion
