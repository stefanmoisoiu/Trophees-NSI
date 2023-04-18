import pygame
import Effects.textPopup as textPopup
import Base.gridManager as gridManager
import Combat.combatManager as combatManager

import Base.events as events

import Entities.entity as entity
import Entities.enemies as enemies
import Entities.playerClasses as playerClasses


# region Window Setup
pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Jeu de role")

framerate: int = 60
clock = pygame.time.Clock()
# endregion

player = entity.CreatePlayer(
    playerClasses.playerProperties,(4,4))

events.onLeftClick.append(lambda: combatManager.SetupAndPlayTurns(mouseGridPos))

goblin = entity.CreateEnemy(enemies.goblinProperties,(3,5))
mageTest = entity.CreateEnemy(enemies.mageTestProperties, (8, 5))

# Tuple de Entity, Healthbar
enemyList = [mageTest,goblin]


# region Game Loop
# running: bool = True 


def gameLoop():
    running = True
    '''Boucle du jeu'''
    while running:
        entity.SetEntities([x[0] for x in enemyList] + [player[0]])
        entity.SetEnemies(enemyList)
        entity.SetPlayer(player)

        # region Setup:Events,variables,etc...
        global mouseGridPos
        deltaTime = clock.tick(framerate) / 1000
        mouseGridPos = gridManager.GetGridPosition(pygame.mouse.get_pos())

        screen.fill((0, 0, 0))
        gridManager.DrawGridOutline(screen)

        events.CheckEvents(pygame.event.get())
        if events.quitting:
            running = False
        
        # endregion

    # region Entities
        for enemy in enemyList:
            enemy[0].Update(deltaTime)
        
        player[0].Update(deltaTime)
        player[2].Update(mouseGridPos, [x[0].gridPosition for x in enemyList])
        
        combatManager.AddTurnShapes()
        gridManager.DrawCells(screen)

        player[0].Display(screen)
        player[1].Display(screen, player[0].rect.center)
        player[2].Display(screen)
        
        for enemy in enemyList:
            enemy[0].Display(screen)
            enemy[1].Display(screen, enemy[0].rect.center)
    # endregion

        for popup in textPopup.activePopups:
            if not popup.alive:
                textPopup.activePopups.remove(popup)
            else:
                popup.Update(deltaTime)
        
        for popup in textPopup.activePopups:
            popup.Display(screen)
        

        pygame.display.flip()
    # endregion
loop = gameLoop()