import pygame
from Base.animation import Animation
from Combat.ability import MeleeAbility, MovementAbility, RangedAbility
from Entities.entity import EntityProperties
import Sound.sounds as sounds


__swordAttackIdleImage = pygame.image.load(
    "Sprites/Abilities/Player/sword_icon.png")
__swordAttackHoverImage = pygame.image.load(
    "Sprites/Abilities/Player/sword_icon_hover.png")
__swordAttackClickImage = pygame.image.load(
    "Sprites/Abilities/Player/sword_icon_click.png")


__playerIdleAnimation = Animation(pygame.image.load(
    "Sprites/Entities/Player/player_idle.png"), loop=True, length=.25, horizontalFrames=4, verticalFrames=1, scale=2, topleft=(.175, .175))
__playerTestAnimation = Animation(pygame.image.load(
    "Sprites/Entities/Player/player test sprite.png"), loop=False, length=1, horizontalFrames=4, verticalFrames=1, scale=2)

__playerMeleeUpAnimation = Animation(pygame.image.load(
    "Sprites/Entities/Player/player_attack_up.png"), loop=False, length=.25, horizontalFrames=4, verticalFrames=1, scale=2, topleft=(.175, .175))
__playerMeleeDownAnimation = Animation(pygame.image.load(
    "Sprites/Entities/Player/player_attack_down.png"), loop=False, length=.25, horizontalFrames=4, verticalFrames=1, scale=2, topleft=(.175, .175))
__playerMeleeRightAnimation = Animation(pygame.image.load(
    "Sprites/Entities/Player/player_attack_right.png"), loop=False, length=.25, horizontalFrames=5, verticalFrames=1, scale=2, topleft=(.175, .175))
__playerMeleeLeftAnimation = Animation(pygame.image.load(
    "Sprites/Entities/Player/player_attack_right.png"), loop=False, length=.25, horizontalFrames=5, verticalFrames=1, flip=True, scale=2, topleft=(.175, .175))

__playerMeleeUpShape = ["F",
                        "F",
                        "C"]
__playerMeleeDownShape = ["C",
                          "F",
                          "F"]
__playerMeleeLeftShape = ["FFC"]
__playerMeleeRightShape = ["CFF"]

__playerMeleeTestAbility = MeleeAbility(damageRange=(1, 3), abilitySpeedRange=(3, 7), missChance=.1,
                                        upAnimation=__playerMeleeUpAnimation, downAnimation=__playerMeleeDownAnimation, leftAnimation=__playerMeleeLeftAnimation, rightAnimation=__playerMeleeRightAnimation,
                                        shapeUp=__playerMeleeUpShape, shapeDown=__playerMeleeDownShape, shapeLeft=__playerMeleeLeftShape, shapeRight=__playerMeleeRightShape, shapeColor=(140, 28, 28), applyAttackAnimAdvancement=.5,
                                        idleAbilityIcon=__swordAttackIdleImage, hoverAbilityIcon=__swordAttackHoverImage, clickedAbilityIcon=__swordAttackClickImage, abilityAppliedSounds=sounds.sword)

__rangedAttackIdleImage = pygame.image.load(
    "Sprites/Abilities/Player/ranged_icon.png")
__rangedAttackHoverImage = pygame.image.load(
    "Sprites/Abilities/Player/ranged_icon_hover.png")
__rangedAttackClickImage = pygame.image.load(
    "Sprites/Abilities/Player/ranged_icon_click.png")

__sideStepAttackIdleImage = pygame.image.load(
    "Sprites/Abilities/Player/sidestep_icon.png")
__sideStepAttackHoverImage = pygame.image.load(
    "Sprites/Abilities/Player/sidestep_icon_hover.png")
__sideStepAttackClickImage = pygame.image.load(
    "Sprites/Abilities/Player/sidestep_icon_click.png")

__playerSideStepZoneShape = [" F ",
                             "FCF",
                             " F "]
__playerSideStepTestAbility = MovementAbility(abilitySpeedRange=(8, 15),
                                              upAnimation=__playerMeleeRightAnimation, downAnimation=__playerMeleeRightAnimation, rightAnimation=__playerMeleeRightAnimation, leftAnimation=__playerMeleeRightAnimation,
                                              zoneShape=__playerSideStepZoneShape, zoneColor=(0, 0, 100), targetColor=(0, 0, 255), applyAttackAnimAdvancement=.5,
                                              idleAbilityIcon=__sideStepAttackIdleImage, hoverAbilityIcon=__sideStepAttackHoverImage, clickedAbilityIcon=__sideStepAttackClickImage)


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
__playerRangedTestAbility = RangedAbility(damageRange=(1, 3), abilitySpeedRange=(1, 6), missChance=.1,
                                          upAnimation=__playerTestAnimation, downAnimation=__playerTestAnimation, leftAnimation=__playerTestAnimation, rightAnimation=__playerTestAnimation,
                                          zoneShape=__playerRangedZoneShape, AOEShape=__playerRangedAOEShape, zoneColor=(100, 0, 0), AOEColor=(140, 28, 28), applyAttackAnimAdvancement=.5,
                                          idleAbilityIcon=__rangedAttackIdleImage, hoverAbilityIcon=__rangedAttackHoverImage, clickedAbilityIcon=__rangedAttackClickImage, abilityAppliedSounds=sounds.fireball)

playerProperties = EntityProperties(
    "Player", "The player", 15, [__playerMeleeTestAbility, __playerSideStepTestAbility, __playerRangedTestAbility], __playerIdleAnimation)
