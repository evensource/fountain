# -*- coding: utf-8 -*-
import os
import pickle
import PIL.Image as Image

def compress(pac):
    n = 0
    pc = ''
    cs = []
    s = pac[0]
    for i in xrange(0, len(s) - 1, 4):
        c = s[i:i + 4]
        if c != pc:
            if n != 0:
                #cs += pc + ' ' + str(n)
                cs.append((pc, n))
            n = 1
            pc = c
        else:
            n += 1
    #cs += pc + ' ' + str(n)
    cs.append((pc, n))
    re = pac[:]
    re[0] = cs
    return re

def decompress(pac):
    cs = pac[0]
    s = ''
    for c, n in cs:
        s += c * n
    re = pac[:]
    re[0] = s
    return re

def pic2stringPac(filename):
    pic = Image.open(filename)
    s = pic.tostring("raw", "RGBA", 0, -1)
    w = pic.size[0]
    h = pic.size[1]
    return [s, w, h]

def dump(filename, data):
    f = open(filename, 'wb')
    pickle.dump(data ,filename)
    f.close()

def load(filename):
    f = open(filename, 'rb')
    a = pickle.load(f)
    f.close()
    return a

def dumpcpic(filename, picfile):
    f = open(filename, 'wb')
    sp = pic2stringPac(picfile)
    csp = compress(sp)
    #csp = sp
    pickle.dump(csp, f)
    f.close()

def loadcpic(filename):
    f = open(filename, 'rb')
    csp = pickle.load(f)
    sp = decompress(csp)
    #sp = csp
    return sp
    f.close()

def dumpcAnime(path, name, typename = '.png'):
    i = 1
    animetypename = '.ani'
    anime = []
    while True:
        fn = path + name + str("%04d" % i) + typename
        if not os.path.exists(fn):
            break
        sp = pic2stringPac(fn)
        csp = compress(sp)
        anime.append(csp)
        i += 1
    fn = path + name + animetypename
    f = open(fn, 'wb')
    pickle.dump(anime, f)
    f.close()

def loadcAnime(filename):
    f = open(filename, 'rb') 
    cpanime = pickle.load(f)
    f.close()
    anime = []
    for pic in cpanime:
        anime.append(decompress(pic))
    return anime
