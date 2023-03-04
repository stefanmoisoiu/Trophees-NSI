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
    if combatManager.playingTurns or playerAbilitiesUI.currentAbility is None or playerAbilitiesUI.ButtonHovered():
        return
    playerAbility = playerAbilitiesUI.currentAbility

    playerAbilityDirection = playerAbility.GetAbilityDirection(
        mouseGridPos, player.position)
    playerAbilityShape = playerAbility.GetPlayerAttackShape(
        player.position, mouseGridPos)

    golbinAbilityDirection = goblin.properties.abilities[0].GetAbilityDirection(
        player.position, goblin.position)
    golbinAbilityShape = goblin.properties.abilities[0].GetEnemyAttackShape(
        goblin.position, player.position)
    combatManager.PlayTurns(
        (player, playerAbility, playerAbilityShape, playerAbilityDirection), [(goblin, goblin.properties.abilities[0], golbinAbilityShape, golbinAbilityDirection)])

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
    "Sprites/Entities/Player/player_idle.png"), loop=True, length=.25, horizontalFrames=4, verticalFrames=1, scale=2, topleft=(.175, .175))
__playerTestAnimation = Animation(pygame.image.load(
    "Sprites/Entities/Player/player test sprite.png"), loop=False, length=1, horizontalFrames=4, verticalFrames=1, scale=2)

__playerMeleeUpAnimation = Animation(pygame.image.load(
    "Sprites/Entities/Player/player_attack_up.png"), loop=False, length=.25, horizontalFrames=4, verticalFrames=1, scale=2, topleft=(.175, .175))
__playerMeleeDownAnimation = Animation(pygame.image.load(
    "Sprites/Entities/Player/player_attack_down.png"), loop=False, length=.25, horizontalFrames=4, verticalFrames=1, scale=2, topleft=(.175, .175))
__playerMeleeLeftAnimation = Animation(pygame.image.load(
    "Sprites/Entities/Player/player_attack_left.png"), loop=False, length=.25, horizontalFrames=5, verticalFrames=1, scale=2, topleft=(.175, .175))
__playerMeleeRightAnimation = Animation(pygame.image.load(
    "Sprites/Entities/Player/player_attack_right.png"), loop=False, length=.25, horizontalFrames=5, verticalFrames=1, scale=2, topleft=(.175, .175))

__playerMeleeUpShape = ["F",
                        "F",
                        "C"]
__playerMeleeDownShape = ["C",
                          "F",
                          "F"]
__playerMeleeLeftShape = ["FFC"]
__playerMeleeRightShape = ["CFF"]

__playerMeleeTestAbility = MeleeAbility(damageRange=(3, 0), abilitySpeedRange=(3, 7),
                                        upAnimation=__playerMeleeUpAnimation, downAnimation=__playerMeleeDownAnimation, leftAnimation=__playerMeleeLeftAnimation, rightAnimation=__playerMeleeRightAnimation,
                                        shapeUp=__playerMeleeUpShape, shapeDown=__playerMeleeDownShape, shapeLeft=__playerMeleeLeftShape, shapeRight=__playerMeleeRightShape, shapeColor=(255, 0, 0), applyAttackAnimAdvancement=.5,
                                        idleAbilityIcon=swordAttackIdleImage, hoverAbilityIcon=swordAttackHoverImage, clickedAbilityIcon=swordAttackClickImage)

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
__playerRangedTestAbility = RangedAbility(damageRange=(3, 0), abilitySpeedRange=(1, 6),
                                          upAnimation=__playerTestAnimation, downAnimation=__playerTestAnimation, leftAnimation=__playerTestAnimation, rightAnimation=__playerTestAnimation,
                                          zoneShape=__playerRangedZoneShape, AOEShape=__playerRangedAOEShape, zoneColor=(100, 0, 0), AOEColor=(255, 0, 0), applyAttackAnimAdvancement=.5,
                                          idleAbilityIcon=rangedAttackIdleImage, hoverAbilityIcon=rangedAttackHoverImage, clickedAbilityIcon=rangedAttackClickImage)

__playerProperties = EntityProperties(
    "Player", "The player", [__playerMeleeTestAbility, __playerRangedTestAbility], __playerIdleAnimation)
player: Entity = Entity(__playerProperties, position=(4, 4))

playerAbilitiesUI = PlayerAbilitiesUI(player)
playerAbilitiesUI.GenerateAbilityButtons()
# endregion

# region Enemy Setup : pareil que pour le joueur, a deplacer dans un fichier de configuration
__goblinIdleAnimation = Animation(pygame.image.load(
    "Sprites/Entities/Enemy/goblin_idle.png"), loop=True, length=.3, horizontalFrames=4, verticalFrames=1, scale=2, topleft=(.333, .333))

__goblinMeleeUpShape = [" F ",
                        " C ",
                        "   "]
__goblinMeleeDownShape = ["   ",
                          " C ",
                          " F "]
__goblinMeleeLeftShape = ["   ",
                          "FC ",
                          "   "]
__goblinMeleeRightShape = ["   ",
                           " CF",
                           "   "]

__goblinAttackRightAnimation = Animation(pygame.image.load(
    "Sprites/Entities/Enemy/goblin_attack_right.png"), loop=False, length=.2, horizontalFrames=7, verticalFrames=1, scale=2, topleft=(.333, .333))
__goblinAttackLeftAnimation = Animation(pygame.image.load(
    "Sprites/Entities/Enemy/goblin_attack_left.png"), loop=False, length=.2, horizontalFrames=7, verticalFrames=1, scale=2, topleft=(.333, .333))
__golbinAttackAbility = MeleeAbility(damageRange=(3, 6), abilitySpeedRange=(0, 6),
                                     upAnimation=__goblinAttackRightAnimation, downAnimation=__goblinAttackRightAnimation, leftAnimation=__goblinAttackLeftAnimation, rightAnimation=__goblinAttackRightAnimation, applyAttackAnimAdvancement=1,
                                     shapeUp=__goblinMeleeUpShape, shapeDown=__goblinMeleeDownShape, shapeLeft=__goblinMeleeLeftShape, shapeRight=__goblinMeleeRightShape, shapeColor=(255, 0, 0))
__goblinProperties = EntityProperties(
    "Goblin", "A goblin", [__golbinAttackAbility], __goblinIdleAnimation)
goblin: Entity = Entity(__goblinProperties, position=(6, 5))
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

# region Entities
    goblin.Update(deltaTime)
    player.Update(deltaTime)
    playerAbilitiesUI.Update(mouseGridPos)

    combatManager.AddTurnShapes()
    gridManager.DrawCells(screen)

    goblin.Display(screen)
    player.Display(screen)
    playerAbilitiesUI.Display(screen)
# endregion
    pygame.display.flip()
# endregion
