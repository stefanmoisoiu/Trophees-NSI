import pygame

onQuit: list[callable] = []
onLeftClick: list[callable] = []


def CallCallbacks(callbacks: list[callable]):
    for callback in callbacks:
        callback()


def CheckEvents(events: list[pygame.event.Event]):
    for event in events:
        if event.type == pygame.QUIT:
            CallCallbacks(onQuit)
        if event.type == pygame.MOUSEBUTTONDOWN:
            CallCallbacks(onLeftClick)
