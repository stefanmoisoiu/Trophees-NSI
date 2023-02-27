import pygame
import Base.gridManager as gridManager
import Combat.combatManager as combatManager
from Base.animation import Animation
from Base.entity import Entity, EntityProperties
from Combat.ability import Ability, MeleeAbility, RangedAbility

# region Setup
pygame.init()

screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
pygame.display.set_caption("Jeu de role")

framerate: int = 60
clock = pygame.time.Clock()
# endregion

# region Player Setup
__playerIdleAnimation = Animation(pygame.image.load(
    "Sprites/Entities/Player/player test sprite.png"), length=.25, horizontalFrames=4, verticalFrames=1)
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
    __playerTestAnimation, (3, 0), (3, 7), __playerMeleeUpShape, __playerMeleeDownShape, __playerMeleeLeftShape, __playerMeleeRightShape, (255, 0, 0))

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
    __playerTestAnimation, (3, 0), (3, 7), __playerRangedZoneShape, __playerRangedAOEShape, (100, 0, 0), (255, 0, 0))

__playerProperties = EntityProperties(
    "Player", "The player", [__playerMeleeTestAbility, __playerRangedTestAbility])
player: Entity = Entity(__playerProperties, position=(8, 8))
player.properties.animationManager.PlayAnimation(__playerIdleAnimation)
# endregion


# region Game Loop
# sourcery skip: merge-list-append
running: bool = True
while running:
    deltaTime = clock.tick(framerate) / 1000

    mouseGridPos = gridManager.GetGridPosition(pygame.mouse.get_pos())

    screen.fill((0, 0, 0))
    gridManager.DrawGridOutline(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            combatManager.PlayTurns(
                (player, player.properties.abilities[1]), [])
            # player.attackShape = player.properties.abilities[1].GetPlayerAttackShape(
            #     player.position, mouseGridPos)

    for attackPreviewShape in player.properties.abilities[1].GetPlayerPreviewShapes(
            player.position, mouseGridPos):
        gridManager.AddShape(
            attackPreviewShape[0], attackPreviewShape[1], attackPreviewShape[2])

    gridManager.DrawCells(screen)

    player.Update(deltaTime)
    player.Display(screen)

    pygame.display.flip()
# endregion
