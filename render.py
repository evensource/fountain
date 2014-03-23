# -*- coding: utf-8 -*-
#基础函数
from OpenGL.GL import *
from OpenGL.GLU import *
import PIL.Image as Image

global textureK
global textureDic
textureK = 0
textureDic = {}

def oglInit(w, h):
    glEnable(GL_BLEND)
    glEnable(GL_MULTISAMPLE)
    glEnable(GL_LINE_SMOOTH)
    glEnable(GL_POLYGON_SMOOTH)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
    glHint(GL_POLYGON_SMOOTH_HINT, GL_NICEST)
    glShadeModel(GL_SMOOTH)
    glViewport(0, 0, w, h)
    glClearColor(0.0, 0.0, 1.0, 1.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    #glOrtho(-w, w*2, -h, h*2, -3000, 3000)
    glOrtho(0, w, 0, h, -3000, 3000)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

class imageObj:
    def __init__(self, filename = None, string = None, w = None, h = None):
        global textureK
        global textureDic
        if filename != None:
            pic = Image.open(filename)
            self.oriSize = pic.size[:]
            self.pics = pic.tostring("raw", "RGBA", 0, -1)
        else:
            self.pics = string
            self.oriSize = (w, h)
        self.textureID = textureK
        textureDic[filename] = textureK
        glBindTexture(GL_TEXTURE_2D, textureK)
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_REPLACE)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self.oriSize[0], self.oriSize[1], 0, GL_RGBA, GL_UNSIGNED_BYTE, self.pics)
        textureK += 1
        self.w2 = self.oriSize[0] / 2
        self.h2 = self.oriSize[1] / 2

    def bindTex(self, mode = GL_REPLACE):
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, mode)
        glBindTexture(GL_TEXTURE_2D, self.textureID)

    def drawQuad(self, horN = 1.0, verN = 1.0, horI = 0, verI = 0):
        w2 = self.w2 / horN
        h2 = self.h2 / verN
        tl = horI / horN
        tr = tl + (1.0 / horN)
        tb = verI / verN
        tt = tb + (1.0 / verN)
        glBegin(GL_QUADS)
        glTexCoord2f(tl, tb)
        glVertex2f(-w2, -h2)
        glTexCoord2f(tr, tb)
        glVertex2f(w2, -h2)
        glTexCoord2f(tr, tt)
        glVertex2f(w2, h2)
        glTexCoord2f(tl, tt)
        glVertex2f(-w2, h2)
        glEnd()

class baseObj:
    def set_Center(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def set_LeftBottom(self, x, y, z = 0):
        self.x = x + self.image.w2
        self.y = y + self.image.h2
        self.z = z

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y

    def move(self, x, y, z):
        self.x += x
        self.y += y

    def rotate(self, x, y, z):
        self.xAg += x
        self.yAg += y
        self.zAg += z

class drawObj(baseObj):
    def __init__(self, image, horN = 1.0, verN = 1.0):
        self.image = image
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0
        self.xAg = 0.0
        self.yAg = 0.0
        self.zAg = 0.0
        self.horN = horN
        self.verN = verN

    def draw(self, horI = 0, verI = 0):
        glEnable(GL_TEXTURE_2D)
        self.image.bindTex()
        glPushMatrix()
        glTranslatef(self.x, self.y, self.z)
        glRotatef(self.xAg, 1.0, 0.0, 0.0)
        glRotatef(self.yAg, 0.0, 1.0, 0.0)
        glRotatef(self.zAg, 0.0, 0.0, 1.0)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        self.image.drawQuad(self.horN, self.verN, horI, verI)
        glPopMatrix()
        glDisable(GL_TEXTURE_2D)

class drawMaskObj(drawObj):
    def __init__(self, image, mask, horN = 1.0, verN = 1.0):
        drawObj.__init__(self, image)
        self.mask = mask
        self.horN = horN
        self.verN = verN

    def draw(self, horI = 0, verI = 0):
        glEnable(GL_TEXTURE_2D)
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_REPLACE)
        glPushMatrix()
        glTranslatef(self.x, self.y, self.z)
        glRotatef(self.xAg, 1.0, 0.0, 0.0)
        glRotatef(self.yAg, 0.0, 1.0, 0.0)
        glRotatef(self.zAg, 0.0, 0.0, 1.0)
        self.drawMask(horI, verI)
        self.drawImage(horI, verI)
        glPopMatrix()
        glDisable(GL_TEXTURE_2D)

    def drawMask(self, horI = 0, verI = 0):
        glBindTexture(GL_TEXTURE_2D, self.mask.textureID)
        glBlendFunc(GL_DST_COLOR, GL_ZERO)
        self.mask.drawQuad(self.horN, self.verN, horI, verI)
        
    def drawImage(self, horI = 0, verI = 0):
        glDisable(GL_DEPTH_TEST)
        glBindTexture(GL_TEXTURE_2D, self.image.textureID)
        glBlendFunc(GL_ONE, GL_ONE)
        self.image.drawQuad(self.horN, self.verN, horI, verI)
        glEnable(GL_DEPTH_TEST)

class animeObj(baseObj):
    def __init__(self, animeData, x = 0, y = 0, z = 0, ppf = 1):
        self.frames = []
        for pic in animeData:
            self.frames.append(imageObj(None, *pic))
        self.x, self.y, self.z = x, y, z
        self.framen = len(self.frames)
        self.ppf = ppf
        self.n = 0
        self.mn = 0

    def draw(self):
        if self.n < self.framen:
            glEnable(GL_TEXTURE_2D)
            glPushMatrix()
            glTranslatef(self.x, self.y, self.z)
            self.frames[self.n].bindTex()
            self.frames[self.n].drawQuad()
            glPopMatrix()
            glDisable(GL_TEXTURE_2D)
            self.mn += 1
            self.mn %= self.ppf
            if self.mn == 0:
                self.n += 1
    
    def get_busy(self):
        return not self.n == self.framen
        
def renderBegin():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    glLoadIdentity()
    #glOrtho(0, 300, 0, 533, -3000, 3000)
    glPushMatrix()

def renderEnd():
    glPopMatrix()

