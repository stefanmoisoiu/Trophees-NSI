from Base.entity import Entity
from Combat.ability import Ability

turnsLeft: list[tuple[Entity, Ability,
                      tuple[list[str], tuple[int, int, int], tuple[int, int]]]] = []
turnShape: tuple[list[str], tuple[int, int, int], tuple[int, int]] = None
playingTurns: bool = False


def PlayTurns(playerTurn: tuple[Entity, Ability, tuple[list[str], tuple[int, int, int], tuple[int, int]]],
              enemyTurns: list[tuple[Entity, Ability, tuple[list[str], tuple[int, int, int], tuple[int, int]]]]):
    sortedTurns = [playerTurn] + enemyTurns
    # sort by speed
    sortedTurns.sort(key=lambda entity: entity[1].GetSpeed())

    global turnsLeft, playingTurns
    playingTurns = True
    turnsLeft = sortedTurns
    PlayNextTurn()


def ApplyTurnDamage():
    print(f"Applying attack by {turnsLeft[-1][0].properties.name}")


def FinishedTurnAnimation():
    print("Finished animation. Next Turn")
    turnsLeft[-1][0].properties.animationManager.PlayAnimation(
        turnsLeft[-1][0].properties.idleAnimation)

    turnsLeft.pop()
    PlayNextTurn()


def PlayNextTurn():
    global turnShape

    if len(turnsLeft) == 0:
        turnShape = None
        global playingTurns
        playingTurns = False
        return
    turnShape = turnsLeft[-1][2]

    turnsLeft[-1][0].properties.animationManager.PlayAnimation(
        turnsLeft[-1][1].animation, [(ApplyTurnDamage, turnsLeft[-1][1].applyAttackAnimAdvancement), (FinishedTurnAnimation, 1)])
