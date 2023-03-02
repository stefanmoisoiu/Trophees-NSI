from Combat.playerAbilitiesUI import PlayerAbilitiesUI
from UI.button import Button
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


# temporaire, a remplacer dans combatManager
def PlayCombatTurnsSetup():
    if playerAbilitiesUI.currentAbility is None or playerAbilitiesUI.ButtonHovered():
        return
    playerAbility = playerAbilitiesUI.currentAbility

    playerAbilityShape = playerAbility.GetPlayerAttackShape(
        player.position, mouseGridPos)
    golbinAbilityShape = goblin.properties.abilities[0].GetEnemyAttackShape(
        goblin.position, player.position)
    combatManager.PlayTurns(
        (player, playerAbility, playerAbilityShape), [(goblin, goblin.properties.abilities[0], golbinAbilityShape)])

# region Player Setup : A DEPLACER DANS UN FICHIER DE CONFIGURATION AVEC LES DIFFERENTES CLASSES DU JOUEUR + LES ARMES ET LES ITEMS QU'ON PEUT OBTENIR


# region Melee Buttons
swordAttackIdleImage = pygame.image.load(
    "Sprites/Abilities/Player/Sword/sword_icon.png")
swordAttackHoverImage = pygame.image.load(
    "Sprites/Abilities/Player/Sword/sword_icon_hover.png")
swordAttackClickImage = pygame.image.load(
    "Sprites/Abilities/Player/Sword/sword_icon_click.png")
# endregion

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
    __playerTestAnimation, (3, 0), (3, 7), __playerMeleeUpShape, __playerMeleeDownShape, __playerMeleeLeftShape, __playerMeleeRightShape, (255, 0, 0), .5, swordAttackIdleImage, swordAttackHoverImage, swordAttackClickImage)

# region Ranged Buttons
rangedAttackIdleImage = pygame.image.load(
    "Sprites/Abilities/Player/Sword/ranged_icon.png")
rangedAttackHoverImage = pygame.image.load(
    "Sprites/Abilities/Player/Sword/ranged_icon_hover.png")
rangedAttackClickImage = pygame.image.load(
    "Sprites/Abilities/Player/Sword/ranged_icon_click.png")
# endregion


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
    __playerTestAnimation, (3, 0), (1, 6), __playerRangedZoneShape, __playerRangedAOEShape, (100, 0, 0), (255, 0, 0), .5, rangedAttackIdleImage, rangedAttackHoverImage, rangedAttackClickImage)

__playerProperties = EntityProperties(
    "Player", "The player", [__playerMeleeTestAbility, __playerRangedTestAbility], __playerIdleAnimation)
player: Entity = Entity(__playerProperties, position=(8, 8))

playerAbilitiesUI = PlayerAbilitiesUI(player)
playerAbilitiesUI.GenerateAbilityButtons(screen)
# endregion

# region Enemy Setup : pareil que pour le joueur, a deplacer dans un fichier de configuration
__goblinIdleAnimation = Animation(pygame.image.load(
    "Sprites/Entities/Enemy/goblin_idle.png"), loop=True, length=.3, horizontalFrames=4, verticalFrames=1)

__goblinMeleeUpShape = [" F ",
                        " F ",
                        " C "]
__goblinMeleeDownShape = [" C ",
                          " F ",
                          " F "]
__goblinMeleeLeftShape = ["   ",
                          "FFC",
                          "   "]
__goblinMeleeRightShape = ["   ",
                           "CFF",
                           "   "]

__goblinAttackRightAnimation = Animation(pygame.image.load(
    "Sprites/Entities/Enemy/goblin_attack_right.png"), loop=False, length=.4, horizontalFrames=5, verticalFrames=1)
__golbinAttackAbility = MeleeAbility(
    __goblinAttackRightAnimation, (3, 6), (0, 6), __goblinMeleeUpShape, __goblinMeleeDownShape, __goblinMeleeLeftShape, __goblinMeleeRightShape, (255, 0, 0), 1)
__goblinProperties = EntityProperties(
    "Goblin", "A goblin", [__golbinAttackAbility], __goblinIdleAnimation)
goblin: Entity = Entity(__goblinProperties, position=(14, 14))
# endregion

# region Game Loop
running: bool = True


def QuitGame():
    global running
    running = False
    print("Quit game")


events.onQuit.append(QuitGame)
events.onLeftClick.append(PlayCombatTurnsSetup)

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
        playerAbilitiesUI.AddPreviewAbilityShape(mouseGridPos)
    combatManager.AddTurnShapes()

    gridManager.DrawCells(screen)
# endregion
# region Entities
    goblin.Update(deltaTime)
    goblin.Display(screen)

    player.Update(deltaTime)
    player.Display(screen)

    playerAbilitiesUI.Update()
    playerAbilitiesUI.Display(screen)
# endregion
    pygame.display.flip()
# endregion
