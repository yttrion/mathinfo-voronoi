#!/usr/bin/python
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import simpledialog
from tkinter import filedialog


from itertools import combinations
import pygame

import numpy as np
import os
import sys
import time

import platform
import math
import random
import configparser


if platform.system().lower() == "windows":
    dirr = "\\"
else:
    dirr = "/"


curDir = os.path.dirname(os.path.abspath(__file__)) + dirr
configfile = curDir + "vor.cfg"
config = configparser.ConfigParser()
config.read(configfile)


def clearScr():
    os.system("clear||cls")


pygame.init()
ost = pygame.mixer.Sound("startup.wav")


global dots, H, W, centers, middles, radius

dots = []
H = config.getint("config", "height")
W = config.getint("config", "width")
centers = []
middles = []
radius = []



class AIO:

    def __init__(self):
        clearScr()
        self.root = tk.Tk()
        self.width = W
        self.height = H
        self.root.geometry(str(H)+"x"+str(W)+"+100+100")
        self.bg = "white"
        self.title = self.root.title("Voronoï")
        self.menubar = tk.Menu(self.root)
        self.root.config(menu=self.menubar)

        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Fichier", menu=self.filemenu)
        self.filemenu.add_command(label="Ouvrir", command=self.openfile)
        self.filemenu.add_command(label="Sauver", accelerator="s")
        self.filemenu.add_command(
            label="Run", accelerator="r", command=self.Delaunay)
        self.filemenu.add_command(label="Quitter", command=self.root.destroy)

        self.custommenu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Edition", menu=self.custommenu)
        self.custommenu.add_command(
            label="Création", command=self.enablecustom)
        self.custommenu.add_command(label="Aléatoire", command=self.randomize)
        self.custommenu.add_command(label="Drag & drop", accelerator="d")
        self.custommenu.add_command(label="Balayage", command=self.randomize)
        self.custommenu.add_command(label="Triangulation")

        self.helpmenu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Aide", menu=self.helpmenu)
        self.helpmenu.add_command(label="Raccourcis")
        self.helpmenu.add_command(label="A propos")

        self.can = tk.Canvas(self.root, height=self.height,
                             width=self.width, bg=self.bg)
        self.can.pack(side=tk.BOTTOM)
        self.keybind()
        self.root.mainloop()

    def motion(self, event):
        x, y = event.x, event.y

    def clicked(self, event):
        x, y = event.x, event.y
        if config.getboolean("config", "custom-plot"):
            self.create_circle(x, y, 2, "red")
            dots.append([x, y])

    def enablecustom(self):
        self.can.delete("all")
        dots.clear()
        config.set("config", "custom-plot", "1")
        self.root.bind('<Button-1>', self.clicked)

    def disbalecustom(self, event):
        config.set("config", "custom-plot", "0")

    def randomize(self):
        config.set("config", "custom-plot", "0")
        n = simpledialog.askinteger("Number of dots", self.root)
        self.can.delete("all")
        dots.clear()
        for k in range(n):
            x, y = random.randint(
                20, self.width-20), random.randint(10, self.height-10)
            self.create_circle(x, y, 2, "red")
            dots.append([x, y])

    def create_circle(self, x, y, r, color):
        # , tags=str(x)+','+str(y))
        self.can.create_oval(x-r, y-r, x+r, y+r, fill=color)

    def create_trans_circle(self, x, y, r):
        self.can.create_oval(x-r, y-r, x+r, y+r, outline="blue")

    def openfile(self, event):
        self.root.filename = filedialog.askopenfilename(initialdir=dir, title="Select file", filetypes=(
            ("Plain text files", "*.txt"), ("All files", "*.*")))

    def keybind(self):
        self.root.bind('<Motion>', self.motion)
        self.root.bind('<Escape>', self.disbalecustom)

        # VIM-like keybind
        self.root.bind('<q>', self.root.destroy)

    def Delaunay(self):

        centers.clear()
        radius.clear()
        keeped = self.triangulation()

        for j in range(len(keeped)):

            tri = keeped[j]

            xa = tri[0][0]
            ya = tri[0][1]

            xb = tri[1][0]
            yb = tri[1][1]

            xc = tri[2][0]
            yc = tri[2][1]

            xab = xb-xa
            yab = yb-ya

            xac = xc-xa
            yac = yc-ya

            xcb = xb-xc
            ycb = yb-yc

            xi = (xa+xb)//2
            yi = (ya+yb)//2

            xj = (xa+xc)//2
            yj = (ya+yc)//2

            xk = (xb+xc)//2
            yk = (yb+yc)//2

            det = xab*yac-xac*yab

            try:
                xo = ((xab*xi+yab*yi)*yac-(xac*xj+yac*yj)*yab)//det
                yo = ((xac*xj+yac*yj)*xab-(xab*xi+yab*yi)*xac)//det
            except ZeroDivisionError:
                pass

            centers.append([xo, yo])

            r = math.sqrt((xo-xa)**2 + (yo-ya)**2)
            self.create_trans_circle(xo, yo, r)

    def triangulation(self):
        listetri = list(combinations(dots, 3))
        keeptri = []

        for j in range(len(listetri)):

            flag = True
            listedist = []
            tri = listetri[j]

            xa, ya = tri[0][0], tri[0][1]

            xb, yb = tri[1][0], tri[1][1]

            xc, yc = tri[2][0], tri[2][1]

            xab, yab = xb-xa, yb-ya

            xac, yac = xc-xa, yc-ya

            xi, yi = (xa+xb)/2, (ya+yb)/2

            xj, yj = (xa+xc)/2, (ya+yc)/2

            xk, yk = (xb+xc)/2, (yb+yc)/2

            det = xab*yac-xac*yab

            try:
                xo = ((xab*xi+yab*yi)*yac-(xac*xj+yac*yj)*yab)//det
                yo = ((xac*xj+yac*yj)*xab-(xab*xi+yab*yi)*xac)//det
            except ZeroDivisionError:
                pass

            r = (xa-xo)**2 + (ya-yo)**2

            for n in range(len(dots)):
                p = dots[n]

                if p not in tri:
                    px, py = p[0], p[1]
                    dist = (px-xo)**2 + (py-yo)**2
                    listedist.append(dist)
                    for D in listedist:
                        if D <= r:
                            flag = False
                            break
            if flag == True:
                keeptri.append(tri)

        return keeptri


class startup:
    print("e")


if __name__ == "__main__":
    ost.play()
    AIO()
