import pygame
from Base.entity import Entity
from Combat.ability import Ability
from UI.button import Button
import Base.gridManager as gridManager
import Combat.combatManager as combatManager


class PlayerAbilitiesUI:
    def __init__(self, playerEntity: Entity):
        self.playerEntity = playerEntity
        self.currentAbility: Ability = None
        self.buttons: list[Button] = []
        self.showButtons: bool = True

        self.bottomMargin: int = 10
        self.leftRightMargin: int = 100

        combatManager.onStartPlayingTurns.append(self.OnStartPlayingTurns)
        combatManager.onEndPlayingTurns.append(self.OnStopPlayingTurns)

    def OnStartPlayingTurns(self):
        self.showButtons = False

    def OnStopPlayingTurns(self):
        self.showButtons = True

    def OnAbilitiesChange(self):
        currentAbilityInNewList: bool = self.currentAbility in self.playerEntity.properties.abilities
        if not currentAbilityInNewList:
            self.currentAbility = None

    def OnAbilityButtonClick(self, ability: Ability):
        print("Ability button clicked.")
        self.currentAbility = ability

    def UpdateButtonsPosition(self, screen: pygame.Surface):

        availableWidth = screen.get_width() - (self.leftRightMargin * 2)
        if len(self.buttons) > 1:
            xDistance = availableWidth / (len(self.buttons)-1)
        else:
            xDistance = availableWidth

        for i in range(len(self.buttons)):
            buttonSize = self.playerEntity.properties.abilities[i].idleAbilityIcon.get_size(
            )
            self.buttons[i].position = (i * xDistance + self.leftRightMargin -
                                        buttonSize[0] / 2, screen.get_height() - self.bottomMargin - buttonSize[1])

    def GenerateAbilityButtons(self):
        self.buttons.clear()

        for i in range(len(self.playerEntity.properties.abilities)):
            print(
                f"AAAAAAAAAAA {self.playerEntity.properties.abilities[i].idleAbilityIcon}")
            self.buttons.append(Button(
                self.playerEntity.properties.abilities[i].idleAbilityIcon,
                self.playerEntity.properties.abilities[i].hoverAbilityIcon,
                self.playerEntity.properties.abilities[i].clickedAbilityIcon,
                (0, 0),
                self.OnAbilityButtonClick, self.playerEntity.properties.abilities[i]))

    def ButtonHovered(self):
        if self.showButtons:
            for button in self.buttons:
                if button.MouseHovered():
                    return True
        return False

    def Display(self, screen: pygame.Surface):
        if self.showButtons:
            for i in range(len(self.buttons)):
                self.UpdateButtonsPosition(screen)
                self.buttons[i].Display(screen)

    def Update(self, mouseGridPos: tuple[int, int]):
        if self.showButtons:
            for button in self.buttons:
                button.Update()

        if not combatManager.playingTurns:
            self.AddPreviewAbilityShape(mouseGridPos)

    def AddPreviewAbilityShape(self, mouseGridPos: tuple[int, int]):
        if self.currentAbility is None:
            return
        for attackPreviewShape in self.currentAbility.GetPlayerPreviewShapes(
                self.playerEntity.position, mouseGridPos):
            gridManager.AddShape(attackPreviewShape)
