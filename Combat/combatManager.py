from Entities.entity import Entity
from Combat.ability import Ability
import Base.gridManager as gridManager
import Effects.textPopup as textPopup

entities: list[Entity] = []
turnsLeft: list[Entity, Ability, gridManager.GridShape, str] = []
currentTurnShape: gridManager.GridShape = None
playingTurns: bool = False

onStartPlayingTurns: callable = []
onEndPlayingTurns: callable = []

damagePopupAddedHeight = 20


def DebugTurns():
    '''Affiche les turns en cours'''
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
    '''Affiche les popup de dommage'''
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
    '''Execute quand l'attaque est appliquee : peut etre appele pendant l'animation a un avancement donne'''
    if ability.damageRange == (0, 0):
        return

    shapePositions = gridManager.GetShapePositions(shape.shape, shape.position)
    for entity in entities:
        for shapePosition in shapePositions:
            if entity.gridPosition == shapePosition:
                print(f"\n------ {entity.properties.name} ------\n")
                damageToApply = ability.GetDamage()
                if ability.Missed():
                    print(f"{entity.properties.name} Missed its attack !")
                    damageToApply = 0

                entity.Damage(damageToApply)

                ShowDamagePopups(
                    damageToApply, (entity.rect.centerx, entity.rect.top))


def SetupAndPlayTurns(enemies: list[Entity], player: Entity, playerAbilitiesUI,mouseGridPos:tuple[int,int]):
    if playingTurns or playerAbilitiesUI.currentAbility is None or playerAbilitiesUI.ButtonHovered():
        return
    
    playerAbility = playerAbilitiesUI.currentAbility

    playerAbilityDirection = playerAbility.GetAbilityDirection(
        mouseGridPos, player.gridPosition)
    playerAbilityShape = playerAbility.GetPlayerAttackShape(
        player.gridPosition, mouseGridPos)
    
    enemiesUsingAbilities = []
    enemyInfos = []
    
    for enemy in enemies:
        
        enemyAbility = enemy.GetEnemyAbility(player.gridPosition)
        if enemyAbility is None:
            continue

        enemyAbilityDirection = enemyAbility.GetAbilityDirection(
            player.gridPosition, enemy.gridPosition)
        enemyAbilityShape = enemyAbility.GetEnemyAttackShape(
            enemy.gridPosition, player.gridPosition)
        
        enemiesUsingAbilities.append(enemy)
        enemyInfos.append((enemy, enemyAbility, enemyAbilityShape, enemyAbilityDirection))
    PlayTurns(enemiesUsingAbilities + [player],
              (player, playerAbility, playerAbilityShape, playerAbilityDirection), enemyInfos)

def PlayTurns(entitiesInTurn: list[Entity], playerTurn: tuple[Entity, Ability, gridManager.GridShape, str],
              enemyTurns: list[tuple[Entity, Ability, gridManager.GridShape, str]]):
    '''Execute quand le joueur a fini de choisir son attaque'''

    global turnsLeft, playingTurns, entities

    entities = entitiesInTurn.copy()
    sortedTurns = [playerTurn] + enemyTurns
    # sort by speed
    sortedTurns.sort(key=lambda entity: entity[1].GetSpeed())

    playingTurns = True
    turnsLeft = sortedTurns

    for callback in onStartPlayingTurns:
        callback()

    PlayNextTurn()


def ApplyTurnDamage():
    '''Execute quand l'attaque est appliquee : peut etre appele pendant l'animation a un avancement donne'''

    DealDamage(entities, turnsLeft[-1][1], turnsLeft[-1][2])
    turnsLeft[-1][1].OnAbilityAttackApplied(
        turnsLeft[-1][0], turnsLeft[-1][2], turnsLeft[-1][3])


def FinishedTurnAnimation():
    '''Execute quand l'animation de l'entite est finie'''

    print("Finished animation. Next Turn")
    turnsLeft[-1][0].properties.animationManager.PlayAnimation(
        turnsLeft[-1][0].properties.idleAnimation)

    turnsLeft[-1][1].OnAbilityAnimationEnded(
        turnsLeft[-1][0], turnsLeft[-1][2], turnsLeft[-1][3])
    turnsLeft.pop()

    PlayNextTurn()


def StopPlayingTurns():
    '''Arrete de jouer les tours et execute les callbacks'''
    global playingTurns, currentTurnShape

    playingTurns = False
    currentTurnShape = None

    for callback in onEndPlayingTurns:
        callback()


def PlayNextTurn():
    '''Joue le tour de l'entite suivante'''

    global turnsLeft, currentTurnShape

    if len(turnsLeft) == 0:
        StopPlayingTurns()
        return
    currentTurnShape = turnsLeft[-1][2]

    turnsLeft[-1][0].properties.animationManager.PlayAnimation(
        turnsLeft[-1][1].GetAnimation(turnsLeft[-1][3]), [(ApplyTurnDamage, turnsLeft[-1][1].applyAttackAnimAdvancement), (FinishedTurnAnimation, 1)])

    turnsLeft[-1][1].OnAbilityAnimationStarted(
        turnsLeft[-1][0], turnsLeft[-1][2], turnsLeft[-1][3])


def AddTurnShapes():
    '''Ajoute les shapes de l'entite suivante'''
    if not playingTurns:
        return
    if currentTurnShape is not None:
        gridManager.AddShape(currentTurnShape)


def ResetWaitingForPopupEnd():
    global waitingForPopupEnd
    waitingForPopupEnd = False
