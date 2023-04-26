import pygame
import Base.events as events
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
framerate = 60

class Slider:
    def __init__(self, position: tuple[int, int], bg: pygame.Surface, handle: pygame.Surface, valueRange: float = (0, 1), direction: str = "Down", onValueChange : list[callable] = None) -> None:
        self.__position = position
        self.__bg = bg
        self.__bgRect = bg.get_rect()
        self.__bgRect.topleft = position
        self.__handle = handle
        self.__handleRect = handle.get_rect()
        self.__onValueChange = onValueChange

        if direction == "Up":
            self.__handleRect.center = self.__bgRect.midbottom
        elif direction == "Down":
            self.__handleRect.center = self.__bgRect.midtop
        elif direction == "Left":
            self.__handleRect.center = self.__bgRect.midright
        elif direction == "Right":
            self.__handleRect.center = self.__bgRect.midleft
        
        self.__valueRange = valueRange
        self.value = valueRange[0]
        self.__direction = direction

        events.whileLeftClick.append(self.Drag)

    def Drag(self):
        mousePos = pygame.mouse.get_pos()

        if not self.__bgRect.collidepoint(mousePos[0], mousePos[1]):
            return

        if self.__direction == "Up":
            self.__handleRect.center = (self.__handleRect.centerx, mousePos[1])
            percent = -(mousePos[1] - self.__bgRect.bottom) / self.__bgRect.height
        elif self.__direction == "Down":
            self.__handleRect.center = (self.__handleRect.centerx, mousePos[1])
            percent = (mousePos[1] - self.__bgRect.top) / self.__bgRect.height
        elif self.__direction == "Left":
            self.__handleRect.center = (mousePos[0], self.__handleRect.centery)
            percent = -(mousePos[0] - self.__bgRect.right) / self.__bgRect.width
        elif self.__direction == "Right":
            self.__handleRect.center = ( mousePos[0], self.__handleRect.centery)
            percent = (mousePos[0] - self.__bgRect.left) / self.__bgRect.width
        
        self.value = (
            self.__valueRange[1] - self.__valueRange[0]) * percent + self.__valueRange[0]
        
        if self.__onValueChange is not None:
            for callable in self.__onValueChange:
                callable(self.value)

    def Display(self, screen: pygame.Surface):
        screen.blit(self.__bg, self.__position)
        screen.blit(self.__handle, self.__handleRect)


sliderbg = pygame.image.load("Sprites/slider test.png")
sliderhandle = pygame.image.load("Sprites/sliderhandle.png")
slider = Slider((300, 300), sliderbg, sliderhandle)

def gameLoop():
    running = True
    '''Boucle du jeu'''
    while running:
        deltaTime = clock.tick(framerate) / 1000

        screen.fill((0, 0, 0))
        slider.Display(screen)

        events.CheckEvents(pygame.event.get())
        if events.quitting:
            running = False

        pygame.display.flip()

gameLoop()