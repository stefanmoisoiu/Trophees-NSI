from Base.entity import Entity
from Combat.ability import Ability
import Base.gridManager as gridManager
import Effects.textPopup as textPopup

entities: list[Entity] = []
turnsLeft: list[Entity, Ability, gridManager.GridShape, str] = []
turnShape: gridManager.GridShape = None
playingTurns: bool = False

onStartPlayingTurns: callable = []
onEndPlayingTurns: callable = []

damagePopupAddedHeight = 20


def DebugTurns():
    print("---Debug Turns---")
    invertedTurns = turnsLeft.copy()
    invertedTurns.reverse()
    for i in range(len(turnsLeft)):
        print(
            f"{i+1} : {turnsLeft[i][0].properties.name} is attacking with ability shape:")
        for line in turnsLeft[i][2].shape:
            print(line)
        print("-----------------")


def ShowDamagePopups(damage: int, worldStartPosition: tuple[float, float]) -> None:
    worldEndPosition = (
        worldStartPosition[0], worldStartPosition[1] - damagePopupAddedHeight)

    damage = abs(damage)
    popupText = str(damage)

    if damage > 0:
        popupProperties = textPopup.damagePopup
    elif damage < 0:
        popupProperties = textPopup.healPopup
    else:
        popupProperties = textPopup.missPopup
        popupText = "Miss"

    textPopup.activePopups.append(
        textPopup.TextPopup(popupText, worldStartPosition, worldEndPosition, popupProperties))


def DealDamage(entities: list[Entity], ability: Ability, shape: gridManager.GridShape):
    if ability.damageRange == (0, 0):
        return

    shapePositions = gridManager.GetShapePositions(shape.shape, shape.position)
    for entity in entities:
        for shapePosition in shapePositions:
            if entity.gridPosition == shapePosition:
                damageToApply = ability.GetDamage()
                # if ability.Missed():
                #    damageToApply = 0

                entity.health -= damageToApply
                print(f"{entity.properties.name} took {damageToApply} damage")

                ShowDamagePopups(
                    damageToApply, (entity.rect.centerx, entity.rect.top))


'''Execute quand le joueur a fini de choisir son attaque'''


def PlayTurns(entitiesTakingDamage: list[Entity], playerTurn: tuple[Entity, Ability, gridManager.GridShape, str],
              enemyTurns: list[tuple[Entity, Ability, gridManager.GridShape, str]]):
    global turnsLeft, playingTurns, entities
    entities = entitiesTakingDamage.copy()
    sortedTurns = [playerTurn] + enemyTurns
    # sort by speed
    sortedTurns.sort(key=lambda entity: entity[1].GetSpeed())

    playingTurns = True
    turnsLeft = sortedTurns

    for callback in onStartPlayingTurns:
        callback()

    DebugTurns()
    PlayNextTurn()


'''Execute quand l'attaque est appliquee : peut etre appele pendant l'animation a un avancement donne'''


def ApplyTurnDamage():
    print(f"Applying attack by {turnsLeft[-1][0].properties.name}")
    DealDamage(entities, turnsLeft[-1][1], turnsLeft[-1][2])
    turnsLeft[-1][1].OnAbilityAttackApplied(
        turnsLeft[-1][0], turnsLeft[-1][2], turnsLeft[-1][3])


'''Execute quand l'animation de l'entite est finie'''


def FinishedTurnAnimation():
    print("Finished animation. Next Turn")
    turnsLeft[-1][0].properties.animationManager.PlayAnimation(
        turnsLeft[-1][0].properties.idleAnimation)

    turnsLeft[-1][1].OnAbilityAnimationEnded(
        turnsLeft[-1][0], turnsLeft[-1][2], turnsLeft[-1][3])
    turnsLeft.pop()
    PlayNextTurn()


def StopPlayingTurns():
    global playingTurns, turnShape

    playingTurns = False
    turnShape = None

    for callback in onEndPlayingTurns:
        callback()


'''Joue le tour de l'entite suivante'''


def PlayNextTurn():
    global turnsLeft, turnShape

    if len(turnsLeft) == 0:
        StopPlayingTurns()
        return
    turnShape = turnsLeft[-1][2]

    turnsLeft[-1][0].properties.animationManager.PlayAnimation(
        turnsLeft[-1][1].GetAnimation(turnsLeft[-1][3]), [(ApplyTurnDamage, turnsLeft[-1][1].applyAttackAnimAdvancement), (FinishedTurnAnimation, 1)])

    turnsLeft[-1][1].OnAbilityAnimationStarted(
        turnsLeft[-1][0], turnsLeft[-1][2], turnsLeft[-1][3])


def AddTurnShapes():
    if not playingTurns:
        return
    if turnShape is not None:
        gridManager.AddShape(turnShape)


def ResetWaitingForPopupEnd():
    global waitingForPopupEnd
    waitingForPopupEnd = False
