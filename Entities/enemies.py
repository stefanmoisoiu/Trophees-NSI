import pygame
from Base.animation import Animation
from Combat.ability import MeleeAbility, MovementAbility
from Entities.entity import EntityProperties

# region Goblin
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
    "Sprites/Entities/Enemy/goblin_attack_right.png"), loop=False, length=.2, horizontalFrames=7, verticalFrames=1, flip=True, scale=2, topleft=(.333, .333))
__golbinAttackAbility = MeleeAbility(damageRange=(3, 6), abilitySpeedRange=(0, 6), missChance=.1,
                                     upAnimation=__goblinAttackRightAnimation, downAnimation=__goblinAttackRightAnimation, leftAnimation=__goblinAttackLeftAnimation, rightAnimation=__goblinAttackRightAnimation, applyAttackAnimAdvancement=.7,
                                     shapeUp=__goblinMeleeUpShape, shapeDown=__goblinMeleeDownShape, shapeLeft=__goblinMeleeLeftShape, shapeRight=__goblinMeleeRightShape, shapeColor=(140, 28, 28))
__goblinMoveZoneShape = [" F ",
                         "FCF",
                         " F "]

__goblinMoveRightAnimation = Animation(pygame.image.load(
    "Sprites/Entities/Enemy/goblin_attack_right.png"), loop=False, length=.2, horizontalFrames=7, verticalFrames=1, scale=2, topleft=(.333, .333))
__goblinMoveLeftAnimation = Animation(pygame.image.load(
    "Sprites/Entities/Enemy/goblin_attack_right.png"), loop=False, length=.2, horizontalFrames=7, verticalFrames=1, flip=True, scale=2, topleft=(.333, .333))
__golbinMoveAbility = MovementAbility(abilitySpeedRange=(0, 6),
                                      upAnimation=__goblinMoveRightAnimation, downAnimation=__goblinMoveRightAnimation, leftAnimation=__goblinMoveLeftAnimation, rightAnimation=__goblinMoveLeftAnimation,
                                      zoneShape=__goblinMoveZoneShape, zoneColor=(0, 0, 100), targetColor=(0, 0, 255), applyAttackAnimAdvancement=.7)
goblinProperties = EntityProperties(
    "Goblin", "A goblin", 5, [__golbinAttackAbility, __golbinMoveAbility], __goblinIdleAnimation)
#endregion