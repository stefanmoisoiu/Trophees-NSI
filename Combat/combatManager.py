from Entities.entity import Entity
from Combat.ability import Ability
import Base.gridManager as gridManager
import Effects.textPopup as textPopup
import Entities.entity as entity

turnsLeft = []
currentTurnShape: gridManager.GridShape = None
playingTurns: bool = False

__entitiesInTurn: list[Entity]

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


def SetupAndPlayTurns(mouseGridPos:tuple[int,int]):
    player = entity.GetPlayer()

    if playingTurns or player[2].currentAbility is None or player[2].ButtonHovered():
        return
    
    entityPositions = [x.gridPosition for x in entity.GetEntities()]
    
    # On calcule l'ability du joueur au debut

    playerAbilityDirection = player[2].currentAbility.GetAbilityDirection(
        mouseGridPos, player[0].gridPosition)
    
    playerAbilityShape = player[2].currentAbility.GetPlayerAttackShape(
        player[0].gridPosition, mouseGridPos, entityPositions)
    
    enemyTurns = [x[0] for x in entity.GetEnemies()]
    
    for i in range(len(enemyTurns)):
        enemyAbility = enemyTurns[i].GetEnemyAbility(
            player[0].gridPosition, entityPositions)

        if enemyAbility is None:
            enemyTurns.pop(i)
        else:
            enemyTurns[i] = (enemyTurns[i], enemyAbility,False)
    
    PlayTurns((player[0], player[2].currentAbility, True,
              playerAbilityDirection, playerAbilityShape), enemyTurns)


def PlayTurns(playerTurn: tuple[Entity, Ability,bool,str,gridManager.GridShape],
              enemyTurns: list[tuple[Entity,bool, Ability]]):
    '''Execute quand le joueur a fini de choisir son attaque'''

    global turnsLeft, playingTurns, __entitiesInTurn

    sortedTurns = [playerTurn] + enemyTurns
    # sort by speed
    sortedTurns.sort(key=lambda x: x[1].GetSpeed())

    playingTurns = True
    turnsLeft = sortedTurns
    __entitiesInTurn = [x[0] for x in sortedTurns]

    for callback in onStartPlayingTurns:
        callback()

    PlayNextTurn()


def ApplyTurnDamage(abilityShape : gridManager.GridShape, abilityDir : str):
    '''Execute quand l'attaque est appliquee : peut etre appele pendant l'animation a un avancement donne'''

    DealDamage(__entitiesInTurn, turnsLeft[-1][1], abilityShape)
    turnsLeft[-1][1].OnAbilityAttackApplied(
        turnsLeft[-1][0],abilityShape, abilityDir)


def FinishedTurnAnimation(abilityShape: gridManager.GridShape, abilityDir: str):
    '''Execute quand l'animation de l'entite est finie'''

    print("Finished animation. Next Turn")
    turnsLeft[-1][0].properties.animationManager.PlayAnimation(
        turnsLeft[-1][0].properties.idleAnimation)

    turnsLeft[-1][1].OnAbilityAnimationEnded(
        turnsLeft[-1][0], abilityShape, abilityDir)
    
    __entitiesInTurn[len(turnsLeft) - 1] = turnsLeft[-1][0]
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
    
    abilityShape = None
    abilityDir = None

    player = entity.GetPlayer()

    if turnsLeft[-1][2] == True:
        # Joueur
        abilityDir = turnsLeft[-1][3]
        abilityShape = turnsLeft[-1][4]
        print("AAAA")
    else:
        #Ennemi
        abilityDir = turnsLeft[-1][1].GetAbilityDirection(
            player[0].gridPosition, turnsLeft[-1][0].gridPosition)
        
        abilityShape = turnsLeft[-1][1].GetEnemyAttackShape(
            turnsLeft[-1][0].gridPosition, player[0].gridPosition, [x.gridPosition for x in entity.GetEntities()])

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
