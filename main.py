import Effects.textPopup as textPopup
from Combat.playerAbilitiesUI import PlayerAbilitiesUI
import pygame
import Base.gridManager as gridManager
import Combat.combatManager as combatManager
import Base.events as events
from Entities.entity import Entity
import Combat.healthbar as healthbar
import Entities.enemies as enemies
import Entities.playerClasses as playerClasses
# IMPORTANT, SUPPRIMER LES IMPORTS INUTILES APRES AVOIR CREE LES FICHIERS CORRESPONDANTS


# region Window Setup
pygame.init()

screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
pygame.display.set_caption("Jeu de role")

framerate: int = 60
clock = pygame.time.Clock()
# endregion

player: Entity = Entity(playerClasses.playerProperties, gridPosition=(4, 4))
playerHealthbar = healthbar.CreateEntityHealthbar(player)

playerAbilitiesUI = PlayerAbilitiesUI(player, 1)
playerAbilitiesUI.GenerateAbilityButtons()


goblin = Entity(enemies.goblinProperties, gridPosition=(8, 4))
goblinHealthbar = healthbar.CreateEntityHealthbar(goblin)

mageTest = Entity(enemies.mageTestProperties, gridPosition=(6, 3))
mageTestHealthbar = healthbar.CreateEntityHealthbar(mageTest)

enemyList = [mageTest,goblin]

# region Game Loop
running: bool = True


def QuitGame():
    global running
    running = False
    print("Quit game")


events.onQuit.append(QuitGame)

# A changer plus tard
events.onLeftClick.append(lambda: combatManager.SetupAndPlayTurns(
    enemyList, player, playerAbilitiesUI, mouseGridPos))

while running:
    # region Setup:Events,variables,etc...
    deltaTime = clock.tick(framerate) / 1000
    mouseGridPos = gridManager.GetGridPosition(pygame.mouse.get_pos())

    screen.fill((0, 0, 0))
    gridManager.DrawGridOutline(screen)

    events.CheckEvents(pygame.event.get())
    # endregion

# region Entities
    for enemy in enemyList:
        enemy.Update(deltaTime)
    
    player.Update(deltaTime)
    for popup in textPopup.activePopups:
        if not popup.alive:
            textPopup.activePopups.remove(popup)
        else:
            popup.Update(deltaTime)
    playerAbilitiesUI.Update(mouseGridPos)

    combatManager.AddTurnShapes()
    gridManager.DrawCells(screen)

    for enemy in enemyList:
        enemy.Display(screen)

    player.Display(screen)
    playerAbilitiesUI.Display(screen)

    playerHealthbar.Display(screen, player.rect.center)
    goblinHealthbar.Display(screen, goblin.rect.center)
    mageTestHealthbar.Display(screen, mageTest.rect.center)

    for popup in textPopup.activePopups:
        popup.Display(screen)
# endregion
    pygame.display.flip()
# endregion
