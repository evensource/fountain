from pygame.mixer import *

def loadmusic(filename):
    music.load(filename) 

def playmusic(times):
    music.play(times)

def stopmusic():
    music.stop()

