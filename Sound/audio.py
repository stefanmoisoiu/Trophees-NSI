import random
import pygame

pygame.mixer.pre_init()

__fadeDuration = .75
__volume = 1

def PlaySound(sound : pygame.mixer.Sound):
    sound.set_volume(__volume)
    sound.play()

def PlayFromSoundList(soundList: list[pygame.mixer.Sound]):
    if soundList is None or len(soundList) == 0:
        return
    PlaySound(random.choice(soundList))


def PlayMusic(musicPath : str):
    if musicPath is None or musicPath == "":
        return

    if pygame.mixer.music.get_busy():
        pygame.mixer.music.fadeout(int(__fadeDuration * 1000))
    
    pygame.mixer.music.load(musicPath)
    pygame.mixer.music.play(-1)

def StopPlayingMusic():

    if not pygame.mixer.music.get_busy():
        return
    
    pygame.mixer.music.fadeout(int(__fadeDuration * 1000))

def SetAudioVolume(volume : float):
    global __volume
    __volume = volume

    pygame.mixer.music.set_volume(volume)
