from Base.entity import Entity
from Combat.ability import Ability
import Base.gridManager as gridManager

turnsLeft: list[Entity, Ability, gridManager.GridShape, str] = []
turnShape: gridManager.GridShape = None
playingTurns: bool = False

onStartPlayingTurns: callable = []
onEndPlayingTurns: callable = []


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


'''Execute quand le joueur a fini de choisir son attaque'''


def PlayTurns(playerTurn: tuple[Entity, Ability, gridManager.GridShape, str],
              enemyTurns: list[tuple[Entity, Ability, gridManager.GridShape, str]]):
    sortedTurns = [playerTurn] + enemyTurns
    # sort by speed
    sortedTurns.sort(key=lambda entity: entity[1].GetSpeed())

    global turnsLeft, playingTurns
    playingTurns = True
    turnsLeft = sortedTurns

    for callback in onStartPlayingTurns:
        callback()

    DebugTurns()
    PlayNextTurn()


'''Execute quand l'attaque est appliquee : peut etre appele pendant l'animation a un avancement donne'''


def ApplyTurnDamage():
    print(f"Applying attack by {turnsLeft[-1][0].properties.name}")


'''Execute quand l'animation de l'entite est finie'''


def FinishedTurnAnimation():
    print("Finished animation. Next Turn")
    turnsLeft[-1][0].properties.animationManager.PlayAnimation(
        turnsLeft[-1][0].properties.idleAnimation)

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
    global turnShape

    if len(turnsLeft) == 0:
        StopPlayingTurns()
        return
    turnShape = turnsLeft[-1][2]

    turnsLeft[-1][0].properties.animationManager.PlayAnimation(
        turnsLeft[-1][1].GetAnimation(turnsLeft[-1][3]), [(ApplyTurnDamage, turnsLeft[-1][1].applyAttackAnimAdvancement), (FinishedTurnAnimation, 1)])


def AddTurnShapes():
    if not playingTurns:
        return
    if turnShape is not None:
        gridManager.AddShape(turnShape)
