from Base.entity import Entity


def PlayTurns(enemies: list[Entity]):
    for enemy in enemies:
        enemy.PlayTurn()
