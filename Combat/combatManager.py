from Base.entity import Entity
from Combat.ability import Ability

turnsLeft: list[tuple[Entity, Ability]] = []


def PlayTurns(playerEntityAndAbility: tuple[Entity, Ability], enemiesAndAbilities: list[tuple[Entity, Ability]]):
    sortedEntities = enemiesAndAbilities + [playerEntityAndAbility]
    # sort by speed
    sortedEntities.sort(key=lambda entity: entity[1].GetSpeed(), reverse=True)

    global turnsLeft
    turnsLeft = sortedEntities
    PlayNextAbility()


def FinishedTurnAnimation():
    print("Finished animation. Next Turn")


def PlayNextAbility():
    if len(turnsLeft) == 0:
        return
    turnsLeft[-1][0].properties.animationManager.PlayAnimation(
        turnsLeft[-1][1].animation, FinishedTurnAnimation)
    turnsLeft.pop()
