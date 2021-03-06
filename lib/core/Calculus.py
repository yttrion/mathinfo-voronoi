#!/usr/bin/python
# -*- coding: utf-8 -*-

import tkinter as tk 

from tkinter import simpledialog, filedialog, messagebox

from itertools import combinations

import os
import platform
import configparser

import math
import random

import lib.gui.voronoi as vor

global keeptri, thall, keeped
keeptri, thall, keeped= [], [], []

def clearScr():
    os.system("clear||cls")

def Dist(p1, p2):
    return math.sqrt((p2[0]-p1[0])**2 + (p2[1]-p1[1])**2)


class Triangulation:

    def __init__(self, dots, offset, can, config, ntheme, tria=1, clean=0):

        global keeped


        self.can = can
        self.tria = tria
        self.dots = dots
        self.config = config
        themes = ["default","solarized","gruvbox", "onedark", "vapor"]
        self.theme = themes[ntheme]
        self.can.delete("all")



        if  ([offset,offset] not in self.dots):
            self.dots.append([-offset,offset])
            self.dots.append([offset,-offset])
            self.dots.append([-offset,-offset])
            self.dots.append([offset,offset])

        elif ([offset,offset] in self.dots) and clean==1:
            print(self.dots.index([-offset,offset]))
            self.dots = self.dots[:-4]

        self.listetri = list(combinations(self.dots, 3))
        keeptri.clear()
        thall.clear()
        clearScr()
        keeped.clear()
        keeped = self.run()

    
    def run(self):

        for j in range(len(self.listetri)):

            flag = True
            listedist = []
            tri = self.listetri[j]

            xa, ya = tri[0][0], tri[0][1]
            xb, yb = tri[1][0], tri[1][1]
            xc, yc = tri[2][0], tri[2][1]

            xab, yab = xb-xa, yb-ya
            xac, yac = xc-xa, yc-ya

            xi, yi = (xa+xb)/2, (ya+yb)/2
            xj, yj = (xa+xc)/2, (ya+yc)/2

            det = 1 if xab*yac-xac*yab==0 else xab*yac-xac*yab

            xo = ((xab*xi+yab*yi)*yac-(xac*xj+yac*yj)*yab)/det
            yo = ((xac*xj+yac*yj)*xab-(xab*xi+yab*yi)*xac)/det

            r = Dist([xa, ya],[xo, yo])

            for n in range(len(self.dots)):

                p = self.dots[n]

                if p not in tri:
                    px, py = p[0], p[1]
                    dist = Dist([px, py], [xo, yo])
                    listedist.append(dist)

                    for D in listedist:
                        if D <= r:
                            flag = False
                            break

            if flag == True:

                keeptri.append(tri)
                thall.append([xo, yo])
                
                if self.tria == 1:
                    self.can.create_line(xa, ya, xb, yb, fill=self.config.get(str(self.theme), "tri"), width=2)
                    self.can.create_line(xc, yc, xb, yb, fill=self.config.get(str(self.theme), "tri"), width=2)
                    self.can.create_line(xa, ya, xc, yc, fill=self.config.get(str(self.theme), "tri"), width=2)
                    
        for i in range(len(self.dots)):
            self.can.create_oval(self.dots[i][0]-2, self.dots[i][1]-2, self.dots[i][0]+2, self.dots[i][1]+2, fill=self.config.get(str(self.theme), "dots"), outline=self.config.get(str(self.theme), "dots"))
        return keeptri


    def motion(self, event):
        x, y = event.x, event.y



class Delaunay:
    global keeped
    def __init__(self, dots, offset, can, config, ntheme):
        self.dots = dots
        self.offset = offset
        self.can = can
        self.config = config
        themes = ["default","solarized","gruvbox", "onedark", "vapor"]
        self.theme = themes[ntheme]
        self.can.delete("all")
        for i in range(len(dots)):
            self.can.create_oval(dots[i][0]-2, dots[i][1]-2, dots[i][0]+2, dots[i][1]+2, fill=self.config.get(str(self.theme), "dots"), outline=self.config.get(str(self.theme), "dots"))

        Triangulation(self.dots, self.offset, self.can, self.config, ntheme, 0)


        for j in range(len(keeped)):

            tri = keeped[j]

            xa, ya = tri[0][0], tri[0][1]
            xb, yb = tri[1][0], tri[1][1]
            xc, yc = tri[2][0], tri[2][1]

            xab, yab = xb-xa, yb-ya
            xac, yac = xc-xa, yc-ya

            xi, yi = (xa+xb)/2, (ya+yb)/2
            xj, yj = (xa+xc)/2, (ya+yc)/2

            det = 1 if xab*yac-xac*yab==0 else xab*yac-xac*yab

            xo = ((xab*xi+yab*yi)*yac-(xac*xj+yac*yj)*yab)/det
            yo = ((xac*xj+yac*yj)*xab-(xab*xi+yab*yi)*xac)/det

            r = Dist([xo, yo], [xa, ya])
            self.create_trans_circle(xo, yo, r)
            self.create_circle(xo, yo, 4, self.config.get(str(self.theme), "cent"))        

    def create_circle(self, x, y, r, color):
        self.can.create_oval(x-r, y-r, x+r, y+r, fill=color, outline=color, tags=str(x)+","+str(y))

    def create_trans_circle(self, x, y, r):
        self.can.create_oval(x-r, y-r, x+r, y+r, outline=self.config.get(str(self.theme), "del"))



class Voronoi:
    global keeped
    def __init__(self, dots, offset, can, config, ntheme):
        self.dots = dots
        self.offset = offset
        self.config = config
        themes = ["default","solarized","gruvbox", "onedark", "vapor"]
        self.theme = themes[ntheme]
        self.can = can
        self.can.delete("all")

        for i in range(len(dots)):
            self.can.create_oval(dots[i][0]-2, dots[i][1]-2, dots[i][0]+2, dots[i][1]+2, fill=self.config.get(str(self.theme), "dots"), outline=self.config.get(str(self.theme), "dots"))
        
        tag=0

        Triangulation(self.dots, self.offset, self.can,self.config, ntheme, 0)

        for i in range(len(keeped)):
    
            A = [keeped[i][0][0], keeped[i][0][1]]
            B = [keeped[i][1][0], keeped[i][1][1]]
            C = [keeped[i][2][0], keeped[i][2][1]]

            for j in range(len(keeped)):

                    D = [keeped[j][0][0], keeped[j][0][1]]
                    E = [keeped[j][1][0], keeped[j][1][1]]
                    F = [keeped[j][2][0], keeped[j][2][1]]

                    TEST = [D, E, F]

                    if i != j :
                    

                        # Méthode de bourrin triangles adjacents
                        if   (A in TEST) and (B in TEST):

                            self.can.create_line(thall[i][0], thall[i][1], thall[j][0], thall[j][1], fill=self.config.get(str(self.theme), "vor"), width=2)
                            tag +=1

                        elif (C in TEST) and (A in TEST):

                            self.can.create_line(thall[i][0], thall[i][1], thall[j][0], thall[j][1], fill=self.config.get(str(self.theme), "vor"), width=2)
                            tag +=1

                        elif (C in TEST) and (B in TEST):

                            self.can.create_line(thall[i][0], thall[i][1], thall[j][0], thall[j][1], fill=self.config.get(str(self.theme), "vor"), width=2)
                            tag +=1       