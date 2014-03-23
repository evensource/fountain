# -*- coding: utf-8 -*-

import numpy as np

def coorSub(a, b):
    ans = (a[0] - b[0], a[1] - b[1])
    return ans

def coorPlus(a, b):
    ans = (a[0] + b[0], a[1] + b[1])
    return ans

def coorMCPlus(a, b):
    ans = (a[0] + b[0], a[1] - b[1])
    return ans

def coorAngle(a, b):
    vec = coorSub(b, a)
    if vec[0] == 0:
       if vec[1] <= 0:
           return 0
       else:
           return 180
    tan = float(vec[1]) / float(vec[0])
    ans = (-np.arctan(tan) / np.pi * 180 - 90) % 180
    if vec[0] > 0:
        ans += 180
    return ans

def vecLen(a):
    return np.sqrt(a[0]**2 + a[1]**2)

def TLorTR(a, b):
    l = (b - a) % 360
    r = (a - b) % 360
    if l < r:
        return 1
    else:
        return -1

def vecTurn(vec, angle):
    theta = angle * np.pi / 180.0
    sintt = np.sin(theta)
    costt = np.cos(theta)
    ans = [0, 0]
    ans[0] = vec[0] * costt - vec[1] * sintt
    ans[1] = vec[0] * sintt + vec[1] * costt
    return ans
