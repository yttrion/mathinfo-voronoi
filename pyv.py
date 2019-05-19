#!/usr/bin/python
# -*- coding: utf-8 -*-

import tkinter as tk

from tkinter import simpledialog, filedialog, messagebox
from itertools import combinations

import numpy as np

import os
import sys
import time
import pygame

import platform
import math
import random
import configparser

# Selection au cas où le script est lancé dans un système UNIX
if platform.system().lower() == "windows":
    dirr = "\\"
else:
    dirr = "/"

curDir = os.path.dirname(os.path.abspath(__file__)) + dirr
configfile = curDir + "src" + dirr + "vor.cfg"
config = configparser.ConfigParser()
config.read(configfile)


def clearScr():
    os.system("clear||cls")


pygame.init()
ost = pygame.mixer.Sound(curDir + "src" + dirr + "startup.wav")

global dots, H, W, keeptri, version, thall

dots, keeptri, thall = [], [], []
H, W = config.getint("config", "height"), config.getint("config", "width")
version = config.get("config", "version")


class AIO:

    def __init__(self):
        clearScr()

        self.root = tk.Tk()
        self.width = W
        self.height = H
        self.size = 2

        self.root.geometry(str(H)+"x"+str(W)+"+100+100")

        self.bg = "grey"
        self.title = self.root.title("Voronoï")
        self.menubar = tk.Menu(self.root)
        self.root.config(menu=self.menubar)

        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Fichier", menu=self.filemenu)
        self.filemenu.add_command(label="Ouvrir", command=self.openfile)
        self.filemenu.add_command(label="Sauver")
        self.filemenu.add_command(label="Run")
        self.filemenu.add_command(label="Quitter", command=self.root.destroy)

        self.custommenu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Edition", menu=self.custommenu)
        self.custommenu.add_command(
            label="Création", command=self.enablecustom)
        self.custommenu.add_command(label="Aléatoire", command=self.randomize)
        self.custommenu.add_command(label="Balayage")
        self.custommenu.add_command(label="Delaunay", command=self.Delaunay)
        self.custommenu.add_command(
            label="Triangulation", command=self.Triangles)

        self.helpmenu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Aide", menu=self.helpmenu)
        self.helpmenu.add_command(label="A propos", command=self.aprops)
        self.helpmenu.add_command(label="Enfer du CPU", command=self.cpuhell)

        self.can = tk.Canvas(self.root, height=self.height,
                             width=self.width, bg=self.bg)
        self.can.pack(side=tk.BOTTOM)
        self.keybind()
        self.root.mainloop()

    def motion(self, event):
        x, y = event.x, event.y

    def display(self, x, y):
        self.can.create_rectangle(x, y, x+self.size, y+self.size, fill="black")

    def clicked(self, event):
        x, y = event.x, event.y
        if config.getboolean("config", "custom-plot"):
            self.create_circle(x, y, 2, "black")
            col = '#%02x%02x%02x' % self.colourize()
            dots.append([x, y, col])

    def enablecustom(self):
        self.can.delete("all")
        dots.clear()
        config.set("config", "custom-plot", "1")
        self.root.bind('<Button-1>', self.clicked)

    def disbalecustom(self, event):
        config.set("config", "custom-plot", "0")

    def randomize(self):
        config.set("config", "custom-plot", "0")
        n = simpledialog.askinteger("Number of dots", self.root, minvalue = 3, maxvalue = 15)
        self.can.delete("all")
        dots.clear()
        if n > 15:
            n=15
        for k in range(n):
            x, y = random.randint(
                20, self.width-20), random.randint(10, self.height-10)
            self.create_circle(x, y, 2, "black")
            col = '#%02x%02x%02x' % self.colourize()
            dots.append([x, y, col])

    def colourize(self):
        a = random.randint(0, 255)
        b = random.randint(0, 255)
        c = random.randint(0, 255)
        return (a, b, c)

    def Dist(self, p1, p2):
        return int(math.sqrt((p2[0]-p1[0])**2 + (p2[1]-p1[1])**2))

    def create_circle(self, x, y, r, color):
        self.can.create_oval(x-r, y-r, x+r, y+r,
                             fill=color, tags=str(x)+","+str(y))

    def create_trans_circle(self, x, y, r):
        self.can.create_oval(x-r, y-r, x+r, y+r, outline="blue")

    def openfile(self):
        self.root.filename = filedialog.askopenfilename(initialdir=dir, title="Select file", filetypes=(
            ("Plain text files", "*.txt"), ("All files", "*.*")))

    def keybind(self):
        self.root.bind('<Motion>', self.motion)
        self.root.bind('<Escape>', self.disbalecustom)

        # VIM-like keybind
        self.root.bind('<q>', self.root.destroy)

    def aprops(self):
        messagebox.showinfo(
            "A propos", "Version: %s\nAuteurs:\n\rPierre-Yves Douault\nVincent Leurent\nPierre-Antoine Soyer" % (version))


    def Delaunay(self):  # Triangulation de Delaunay

        keeped = self.Triangles()

        for j in range(len(keeped)):

            tri = keeped[j]

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

            r = self.Dist([xo, yo], [xa, ya])
            self.create_trans_circle(xo, yo, r)
            self.create_circle(xo, yo, 4, "green")

    def Triangles(self):  # Selection des triangles utilisables
        self.disbalecustom(self.motion)
        listetri = list(combinations(dots, 3))
        keeptri.clear()
        thall.clear()

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
                thall.append([xo, yo, r])
                self.can.create_line(xa, ya, xb, yb, fill="green", width=2)
                self.can.create_line(xc, yc, xb, yb, fill="green", width=2)
                self.can.create_line(xa, ya, xc, yc, fill="green", width=2)

        return keeptri













    # Pire système de scan de tous les temps
    def pixeler(self, i, j):

        distance = 2 * self.width
        if len(dots) > 9:
            rang = 10
        else:
            rang = len(dots)
        for k in range(rang):

            xtemp = dots[k][0]
            ytemp = dots[k][1]

            dist = math.sqrt((xtemp - i)**2 + (ytemp - j)**2)

            if dist < distance:
                distance = dist
                nearest = k

            tempcol = dots[nearest][2]

            self.can.create_rectangle(
                i, j, i+1, j+1, fill=tempcol, outline=tempcol)

    def cpuhell(self):

        # Scan pixel par pixel
        # plus connu sous le nom de
        # L'ENFER DES CPU

        for i in range(0, self.width):
            for j in range(0, self.height):
                self.pixeler(i+1, j+1)
        print("Ended")

        for i in range(10):
            self.create_circle(dots[i][0], dots[i][1], 2, "black")


if __name__ == "__main__":
    ost.play()
    time.sleep(1.7)
    AIO()
