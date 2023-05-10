import pygame

onQuit: list[callable] = []
quitting : bool = False
onLeftClick: list[callable] = []
whileLeftClick: list[callable] = []


def CallCallbacks(callbacks: list[callable]):
    """Fonction qui execute les callbacks"""
    for callback in callbacks:
        callback()


def CheckEvents(events: list[pygame.event.Event]):
    global quitting
    '''Fonction qui verifie les evenements'''
    for event in events:
        if event.type == pygame.QUIT:
            quitting = True
            CallCallbacks(onQuit)
        if event.type == pygame.MOUSEBUTTONDOWN:
            CallCallbacks(onLeftClick)
    
    if pygame.mouse.get_pressed()[0]:
        CallCallbacks(whileLeftClick)
