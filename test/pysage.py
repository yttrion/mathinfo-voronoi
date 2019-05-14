global points
global g = Graphics()
from random import randint
import sage

Points=[(randint(-500,500)/100,randint(-500,500)/100 for p in range(4))]

for p in Points:
    g+=point2d(p,rgbcolor(0,0,1), size=25)