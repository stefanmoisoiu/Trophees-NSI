import pygame
import Effects.textPopup as textPopup
import Base.gridManager as gridManager
import Combat.combatManager as combatManager

import Base.events as events

import Entities.entity as entity
import Entities.enemies as enemies
import Entities.playerClasses as playerClasses

import Sound.audio as audio
audio.PlayMusic("Sound/Music/botw.mp3")

# region Window Setup
pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Jeu de role")

framerate: int = 60
clock = pygame.time.Clock()
# endregion

player = entity.CreatePlayer(
    playerClasses.playerProperties,(4,4))

events.onLeftClick.append(
    lambda: combatManager.SetupAndPlayTurns(mouseGridPos))


def EnemyDied(enemy):
    global enemyList
    for i in range(len(enemyList)):
        if enemyList[i][0] == enemy:
            enemyList.pop(i)
            combatManager.TryRemoveEnemyFromTurn(enemy)
            return


goblin1 = entity.CreateEnemy(enemies.goblinProperties, (3, 1), EnemyDied)
goblin2 = entity.CreateEnemy(enemies.goblinProperties, (5, 7), EnemyDied)
goblin3 = entity.CreateEnemy(enemies.goblinProperties, (1, 2), EnemyDied)
goblin4 = entity.CreateEnemy(enemies.goblinProperties, (7, 4), EnemyDied)
mageTest = entity.CreateEnemy(enemies.mageTestProperties, (8, 5), EnemyDied)

# Tuple de Entity, Healthbar
enemyList = [mageTest, goblin1, goblin2, goblin3, goblin4]

# region Game Loop
def gameLoop(running: bool):
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
        
        for enemy in enemyList:
            enemy[0].Display(screen)
            enemy[1].Display(screen, enemy[0].rect.center)

        player[0].Display(screen)
        player[1].Display(screen, player[0].rect.center)
        player[2].Display(screen)
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
