from drawBot import newPage, width, height, oval
from math import pi, sin

canvas = 800, 800

ampX = canvas[0]/2
ampY = canvas[1]/2
angFreqX = 1
angPhaseX = pi / 4
angFreqY = 4
angPhaseY = pi / 1

length = 1000

newPage(*canvas)
for index in range(length):
    t = index * pi * 2 / length
    x = width() / 2 + ampX * sin(angFreqX * t + angPhaseX)
    y = height() / 2 + ampY * sin(angFreqY * t + angPhaseY)
    oval(x-1, y-1, 2, 2)