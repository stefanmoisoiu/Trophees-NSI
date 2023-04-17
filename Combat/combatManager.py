from Entities.entity import Entity
from Combat.ability import Ability
import Base.gridManager as gridManager
import Effects.textPopup as textPopup

entities: list[Entity] = []
entityPositions : list[tuple[int,int]] = []
turnsLeft: list[Entity, Ability, gridManager.GridShape, str] = []
currentTurnShape: gridManager.GridShape = None
playingTurns: bool = False
__player : Entity = None

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
    
    for entity in entities:
        for shapePosition in shape.shapePositions:
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
    
    entities = enemies + [player]
    entityPositions = [x.gridPosition for x in entities]
    
    # On calcule l'ability du joueur au debut
    playerAbility = playerAbilitiesUI.currentAbility

    playerAbilityDirection = playerAbility.GetAbilityDirection(
        mouseGridPos, player.gridPosition)
    playerAbilityShape = playerAbility.GetPlayerAttackShape(
        player.gridPosition, mouseGridPos, entityPositions)
    
    enemyTurns = enemies.copy()
    
    for i in range(len(enemies)):
        enemyAbility = enemies[i].GetEnemyAbility(player.gridPosition, entityPositions)

        if enemyAbility is None:
            enemyTurns.pop(i)
        else:
            enemyTurns[i] = (enemyTurns[i], enemyAbility)
    
    PlayTurns(enemies + [player],
              (player, playerAbility, playerAbilityDirection, playerAbilityShape), enemyTurns)


def PlayTurns(entitiesInTurn: list[Entity], playerTurn: tuple[Entity, Ability,str,gridManager.GridShape],
              enemyTurns: list[tuple[Entity, Ability]]):
    '''Execute quand le joueur a fini de choisir son attaque'''

    global turnsLeft, playingTurns, entities, entityPositions, __player

    __player = playerTurn[0]

    entities = entitiesInTurn.copy()
    entityPositions = [x.gridPosition for x in entities]


    sortedTurns = [playerTurn] + enemyTurns
    # sort by speed
    sortedTurns.sort(key=lambda entity: entity[1].GetSpeed())

    playingTurns = True
    turnsLeft = sortedTurns

    for callback in onStartPlayingTurns:
        callback()

    PlayNextTurn()


def ApplyTurnDamage(abilityShape : gridManager.GridShape, abilityDir : str):
    '''Execute quand l'attaque est appliquee : peut etre appele pendant l'animation a un avancement donne'''

    DealDamage(entities, turnsLeft[-1][1], abilityShape)
    turnsLeft[-1][1].OnAbilityAttackApplied(
        turnsLeft[-1][0],abilityShape, abilityDir)


def FinishedTurnAnimation(abilityShape: gridManager.GridShape, abilityDir: str):
    '''Execute quand l'animation de l'entite est finie'''

    print("Finished animation. Next Turn")
    turnsLeft[-1][0].properties.animationManager.PlayAnimation(
        turnsLeft[-1][0].properties.idleAnimation)

    turnsLeft[-1][1].OnAbilityAnimationEnded(
        turnsLeft[-1][0], abilityShape, abilityDir)
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

    global turnsLeft, currentTurnShape,entities

    if len(turnsLeft) == 0:
        StopPlayingTurns()
        return
    
    abilityShape = None
    abilityDir = None

    if (turnsLeft[-1][0]) is __player:
        # Joueur
        abilityDir = turnsLeft[-1][2]
        abilityShape = turnsLeft[-1][3]
    else:
        #Ennemi
        abilityDir = turnsLeft[-1][1].GetAbilityDirection(
            __player.gridPosition, turnsLeft[-1][0].gridPosition)
        abilityShape = turnsLeft[-1][1].GetEnemyAttackShape(
            turnsLeft[-1][0].gridPosition, __player.gridPosition, entityPositions)

    currentTurnShape = abilityShape

    turnsLeft[-1][0].properties.animationManager.PlayAnimation(
        turnsLeft[-1][1].GetAnimation(abilityDir), [(lambda: ApplyTurnDamage(abilityShape, abilityDir), turnsLeft[-1][1].applyAttackAnimAdvancement),
                                                    (lambda: FinishedTurnAnimation(abilityShape, abilityDir), 1)])

    turnsLeft[-1][1].OnAbilityAnimationStarted(
        turnsLeft[-1][0], abilityShape, abilityDir)


def AddTurnShapes():
    '''Ajoute les shapes de l'entite suivante'''
    if not playingTurns:
        return
    if currentTurnShape is not None:
        gridManager.AddShape(currentTurnShape)


def ResetWaitingForPopupEnd():
    global waitingForPopupEnd
    waitingForPopupEnd = False
