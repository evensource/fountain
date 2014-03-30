# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import sys

class game:
    
    def __init__(self, title, winSize = (800, 600), renderFps = 60, ogl = True, fs = True):
        pygame.init()
        self.calcClock = pygame.time.Clock()
        self.renderClock = pygame.time.Clock()
        pygame.display.set_caption(title)
        winState = DOUBLEBUF | HWSURFACE
        if ogl == True:
            winState |= OPENGL
        if fs == True:
            winState |= FULLSCREEN
        self.winSurf= pygame.display.set_mode(winSize, winState)
        self.rect = self.winSurf.get_rect()
        self.winSize = self.rect.size
        self.cx = 0
        self.cy = 0
        self.startCPos = (0, 0)
        self.startPos = (0, 0)
        self.grabornot = True
        #self.calcFps = calcFps
        self.renderFps = renderFps
        ##pygame.key.set_repeat(1, 1)

    def eventSolve(self):
        self.mousePos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE or event.key == K_q:
                    pygame.quit()
                    sys.exit()

    def renderEnd(self):
        pygame.display.flip()
        self.renderClock.tick(self.renderFps)

    #def calcEnd(self):
    #    self.calcClock.tick(self.calcFps)

