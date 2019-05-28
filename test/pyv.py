#!/usr/bin/python
# -*- coding: utf-8 -*-

import tkinter as tk  # Pour éviter de tout importer

from tkinter import simpledialog, filedialog, messagebox

from itertools import combinations

import os
import time
import platform
import configparser

import pygame, time

import math
import random


# Selection au cas où le script est lancé dans un système UNIX (OSX, BSD, Linux)
dirr = "\\" if platform.system().lower() == "windows" else "/"


curDir = os.path.dirname(os.path.abspath(__file__)) + dirr
configfile = curDir + "vor.cfg"
config = configparser.ConfigParser()
config.read(configfile)


def clearScr():
    os.system("clear||cls")




pygame.init()
startup = pygame.mixer.Sound(curDir + "src" + dirr + "startup.wav")




global dots, keeptri, version, thall, offset, size
dots, keeptri, thall, version, colors, offset = [], [], [], config.get("config", "version"), [], 1000000

size = config.getint("config", "size")

class AIO:

    def __init__(self, size, point=[]):
        clearScr()
        self.pt = point

        self.root = tk.Tk()
        self.width, self.height = size, size
        self.size = 2

        self.root.geometry(str(self.height)+"x"+str(self.height)+"+25+25")

        self.bg = "grey"
        self.title = self.root.title("【ＶＯＲＯＮＯＩ】")
        config.set("config", "tested", "0")

        self.can = tk.Canvas(self.root, height=self.height,width=self.width, bg=self.bg)
        self.can.pack(side=tk.BOTTOM)
        self.keybind()

        self.menubar = tk.Menu(self.root)
        self.root.config(menu=self.menubar)

        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Fichier", menu=self.filemenu)
        self.filemenu.add_command(label="Ouvrir", command=self.openfile)
        self.filemenu.add_command(label="Sauver", command=self.save)
        self.filemenu.add_command(label="Quitter", command=self.root.destroy)

        self.custommenu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Edition", menu=self.custommenu)
        self.custommenu.add_command(label="Création", command=self.enablecustom)
        self.custommenu.add_command(label="Aléatoire", command=self.randomize)
        self.custommenu.add_command(label="Voronoï", command=self.voronoi)
        self.custommenu.add_command(label="Delaunay", command=self.Delaunay)
        self.custommenu.add_command(label="Triangulation", command=self.Triangles)

        self.helpmenu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Aide", menu=self.helpmenu)
        self.helpmenu.add_command(label="A propos", command=self.aprops)
        self.helpmenu.add_command(label="Enfer du CPU", command=self.cpuhell)
    
        if len(self.pt):
            self.update()

        self.root.mainloop()

    def update(self):
        for i in range(len(self.pt)):
            self.create_circle(self.pt[i][0], self.pt[i][1], 2, "black")
        dots = []
        dots = self.pt
        print(dots)

    def motion(self, event):
        x, y = event.x, event.y

    def clicked(self, event):
        x, y = event.x, event.y
        if config.getboolean("config", "custom-plot"):
            if len(dots)==15:
                messagebox.showinfo("Info", "Pas plus de 15 points sur le canvas")
                self.disbalecustom(self.motion)
            elif len(dots)<15:
                self.create_circle(x, y, 2, "black")
                
                col = '#%02x%02x%02x' % self.colourize()
                dots.append([x, y])
                colors.append(col)

    def enablecustom(self):
        self.can.delete("all")
        dots.clear()
        config.set("config", "custom-plot", "1")
        self.root.bind('<Button-1>', self.clicked)

    def disbalecustom(self, event):
        config.set("config", "custom-plot", "0")

    def randomize(self):
        config.set("config", "custom-plot", "0")
        n = simpledialog.askinteger("Nombre de points", "Entrez le nombre de points [2-15]",  minvalue=2)
        self.can.delete("all")
        dots.clear()

        for k in range(n):
            x, y = random.randint(20, self.width-20), random.randint(20, self.height-20)
            self.create_circle(x, y, 2, "black")
            col = '#%02x%02x%02x' % self.colourize()
            dots.append([x, y])
            colors.append(col)

    def colourize(self):
        a = random.randint(0, 255)
        b = random.randint(0, 255)
        c = random.randint(0, 255)
        return (a, b, c)

    def Dist(self, p1, p2):
        return math.sqrt((p2[0]-p1[0])**2 + (p2[1]-p1[1])**2)

    def create_circle(self, x, y, r, color):
        self.can.create_oval(x-r, y-r, x+r, y+r, fill=color, tags=str(x)+","+str(y))

    def create_trans_circle(self, x, y, r):
        self.can.create_oval(x-r, y-r, x+r, y+r, outline="blue")

    def openfile(self):
        filename = filedialog.askopenfilename(initialdir=dir, title="Select file", filetypes=(("Plain text files", "*.txt"), ("All files", "*.*")))

        if len(filename)!=0:
            coord = []
            if filename[-3:] == "txt":
                f = open(filename)
                content = [line.rstrip('\n') for line in f]
                for i in range(1,len(content)):
                    temp = content[i].split()
                    coord.append([int(temp[0]), int(temp[1])])
                config.set("config", "size", str(content[0]))
                f.close()
                self.root.destroy()
                self.__init__(content[0], coord)
                    
            else:
                messagebox.showerror("Erreur", "Format de fichier non reconnu.")

    def keybind(self):
        self.root.bind('<Motion>', self.motion)
        self.root.bind('<Escape>', self.disbalecustom)

    def aprops(self):
        messagebox.showinfo(
            "A propos", "Version:\t%s\nAuteurs:\tPierre-Yves Douault\n\tVincent Leurent\n\tPierre-Antoine Soyer" % (version))

    def save(self):
        output = filedialog.asksaveasfile(mode="w", defaultextension=".txt")
        
        output.write(str(self.width) + "\n")
        
        for i in range(len(dots)):
        
            if abs(dots[i][0]) <= self.width and abs(dots[i][1]) <= self.width:
        
                output.write(str(dots[i][0]) + " " + str(dots[i][1]) + "\n")
        
        output.close()

    def Delaunay(self):  # Triangulation de Delaunay

        keeped = self.Triangles(0)

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

            r = self.Dist([xo, yo], [xa, ya])
            self.create_trans_circle(xo, yo, r)
            self.create_circle(xo, yo, 4, "green")

    def Triangles(self, tria=1):  # Selection des triangles utilisables

        self.disbalecustom(self.motion)

        dots.append([-offset,offset])
        dots.append([offset,-offset])
        dots.append([-offset,-offset])
        dots.append([offset,offset])

        listetri = list(combinations(dots, 3))
        keeptri.clear()
        thall.clear()
        clearScr()

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

            det = 1 if xab*yac-xac*yab==0 else xab*yac-xac*yab

            xo = ((xab*xi+yab*yi)*yac-(xac*xj+yac*yj)*yab)/det
            yo = ((xac*xj+yac*yj)*xab-(xab*xi+yab*yi)*xac)/det

            r = self.Dist([xa, ya],[xo, yo])

            for n in range(len(dots)):

                p = dots[n]

                if p not in tri:
                    px, py = p[0], p[1]
                    dist = self.Dist([px, py], [xo, yo])
                    listedist.append(dist)

                    for D in listedist:
                        if D <= r:
                            flag = False
                            break

            if flag == True:

                keeptri.append(tri)
                thall.append([xo, yo])
                
                if tria == 1:

                    self.can.create_line(xa, ya, xb, yb, fill="green", width=2)
                    self.can.create_line(xc, yc, xb, yb, fill="green", width=2)
                    self.can.create_line(xa, ya, xc, yc, fill="green", width=2)

        print("%s triangles saved" % len(keeptri))
        return keeptri
        
    def voronoi(self):

        keeped = self.Triangles(0)
        tag = 0

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

                            self.can.create_line(thall[i][0], thall[i][1], thall[j][0], thall[j][1], fill="red", width=2)
                            tag +=1

                        elif (C in TEST) and (A in TEST):

                            self.can.create_line(thall[i][0], thall[i][1], thall[j][0], thall[j][1], fill="red", width=2)
                            tag +=1

                        elif (C in TEST) and (B in TEST):

                            self.can.create_line(thall[i][0], thall[i][1], thall[j][0], thall[j][1], fill="red", width=2)
                            tag +=1       
        print("%s lines made" % tag)  





                    













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

            dist = self.Dist([i, j], [xtemp, ytemp])

            if dist < distance:
                distance = dist
                nearest = k

            try :
                tempcol = colors[nearest]

                self.can.create_rectangle(i, j, i+1, j+1, fill=tempcol, outline=tempcol)
            except :
                pass

    def cpuhell(self):

        # Scan pixel par pixel
        # plus connu sous le nom de
        # L'ENFER DES CPU

        for i in range(0, self.width):
            for j in range(0, self.height):
                self.pixeler(i+1, j+1)

        for i in range(10):
            self.create_circle(dots[i][0], dots[i][1], 2, "black")


if __name__ == "__main__":
    startup.play()          # 【A】【E】【S】【T】【H】【E】【T】【I】【C】【S】
    AIO(size)