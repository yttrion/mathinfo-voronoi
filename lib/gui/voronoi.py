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

def clearScr():
    os.system("clear||cls")

import lib.core.Calculus as calc

global dots, colors, nclic
dots, colors, nclic = [], [], 0

class Main:
    
    def __init__(self, size, dirr, pts=[], ntheme=0):
        global dots
        self.dirr = dirr
        self.curDir = os.path.dirname(os.path.abspath(__file__)) + self.dirr
        configfile = self.curDir + ".." + self.dirr + "config" + self.dirr + "vor.cfg"
        self.config = configparser.ConfigParser()
        self.config.read(configfile)
        self.fensize = size
        self.ntheme = ntheme

        self.version = self.config.get("config", "version")

        test = ["default", "solarized", "gruvbox", "onedark", "vapor"]
        self.theme = test[self.ntheme]


        if self.config.getboolean("config", "extras"):
            import pygame
            pygame.init()
            splash = pygame.mixer.Sound(self.curDir + "sounds" + self.dirr + "main.ogg")
            splash.play()  


        clearScr()

        self.offset = 100000

        self.root = tk.Tk()
        self.width, self.height = size, size
        self.size = 2

        self.root.geometry(str(self.height)+"x"+str(self.height)+"+105+75")

        self.bg = self.config.get(str(self.theme), "bg")
        self.title = self.root.title("【ＶＯＲＯＮＯＩ】")

        self.pt = pts

        self.can = tk.Canvas(self.root, height=self.height,width=self.width, bg=self.bg)
        self.can.pack(side=tk.BOTTOM)


        self.menubar = tk.Menu(self.root)
        self.root.config(menu=self.menubar)

        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Fichier", menu=self.filemenu)
        self.filemenu.add_command(label="Nouveau", command=self.cleaner)
        self.filemenu.add_command(label="Ouvrir", command=self.openfile)
        self.filemenu.add_command(label="Sauver", command=self.save)
        self.filemenu.add_command(label="Couleurs", command=self.setuptheme)
        self.filemenu.add_command(label="Quitter", command=self.root.destroy)

        self.custommenu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Edition", menu=self.custommenu)
        self.custommenu.add_command(label="Création", command=self.enablecustom)
        self.custommenu.add_command(label="Déplacer", command=self.deplacer)
        self.custommenu.add_command(label="Aléatoire", command=self.randomize)
        self.custommenu.add_command(label="Voronoï", command=self.runvor)
        self.custommenu.add_command(label="Delaunay", command=self.rundel)
        self.custommenu.add_command(label="Triangulation", command=self.runtri)

        self.helpmenu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Aide", menu=self.helpmenu)
        self.helpmenu.add_command(label="A propos", command=self.aprops)

        if len(self.pt):
            self.update()
            pass
        self.root.mainloop()

    def cleaner(self):
        self.disbalecustom(self.motion)
        self.can.delete("all")
        dots.clear()       

    def motion(self, event):
        x, y = event.x, event.y

    def enablecustom(self):
        self.config.set("config", "custom-plot", "1")
        self.root.bind('<Button-1>', self.clicked)

    def disbalecustom(self, event):
        self.config.set("config", "custom-plot", "0")    

    def create_circle(self, x, y, r, color):
        self.can.create_oval(x-r, y-r, x+r, y+r, fill=color, outline=color, tags=str(x)+","+str(y))


    def setuptheme(self):
        n = simpledialog.askinteger("Séléction du thème", "Default(1), Solarized(2), Gruvbox(3), OneDark(4), Vaporwave(5)",  minvalue=1, maxvalue=5)
        self.config.set("config", "theme", str(n-1))
        self.root.destroy()
        self.__init__(self.fensize, self.dirr, [], n-1)

    def openfile(self):
        global dots
        filename = filedialog.askopenfilename(initialdir=dir, title="Select file", filetypes=(("Plain text files", "*.txt"), ("All files", "*.*")))

        if len(filename)!=0:
            coord = []
            if filename[-3:] == "txt":
                try :
                    f = open(filename)
                    content = [line.rstrip('\n') for line in f]
                    for i in range(1,len(content)):
                        temp = content[i].split()
                        coord.append([int(temp[0]), int(temp[1])])
                    self.config.set("config", "size", str(content[0]))
                    f.close()   
                    self.root.destroy()
                    self.__init__(content[0], self.dirr, coord, self.ntheme)
                except:
                    messagebox.showerror("Erreur", "Fichier corrompu")
            else:
                messagebox.showerror("Erreur", "Format de fichier non reconnu.")

    def colourize(self):
        a = random.randint(0, 255)
        b = random.randint(0, 255)
        c = random.randint(0, 255)
        return (a, b, c)

    def clicked(self, event):
        x, y = event.x, event.y
        if self.config.getboolean("config", "custom-plot"):
            self.create_circle(x, y, 2, self.config.get(str(self.theme), "dots"))
            col = '#%02x%02x%02x' % self.colourize()
            dots.append([x, y])
            colors.append(col)
        if len(dots)>1:
            calc.Voronoi(dots, self.offset, self.can, self.config, self.ntheme)


    def randomize(self):
        self.config.set("config", "custom-plot", "0")
        n = simpledialog.askinteger("Nombre de points", "Entrez le nombre de points [2-15]",  minvalue=2)
        if n == None:
            return
        self.can.delete("all")
        dots.clear()

        for k in range(n):
            x, y = random.randint(20, self.width-20), random.randint(20, self.height-20)
            self.create_circle(x, y, 2, self.config.get(str(self.theme), "dots"))
            col = '#%02x%02x%02x' % self.colourize()
            dots.append([x, y])
            colors.append(col)    
        
    def runtri(self):
        Disablecustom(self.config)
        calc.Triangulation(dots, self.offset, self.can, self.config, self.ntheme)

    def rundel(self):
        Disablecustom(self.config)
        calc.Delaunay(dots, self.offset, self.can, self.config, self.ntheme)

    def runvor(self):
        Disablecustom(self.config)
        calc.Voronoi(dots, self.offset, self.can, self.config, self.ntheme)

    def save(self):
        output = filedialog.asksaveasfile(mode="w", defaultextension=".txt")
        
        output.write(str(self.width) + "\n")
        
        for i in range(len(dots)):
        
            if abs(dots[i][0]) <= self.width and abs(dots[i][1]) <= self.width:
        
                output.write(str(dots[i][0]) + " " + str(dots[i][1]) + "\n")
        
        output.close()

    def update(self):

        global dots
        for i in range(len(self.pt)):
            self.create_circle(self.pt[i][0], self.pt[i][1], 2, self.config.get(str(self.theme), "dots"))
        dots = []
        dots = self.pt
        print(dots)   

    def deplacer(self):
        self.config.set("config", "custom-plot", "0")
        self.root.bind('<Button-1>', self.clicked2)

    def clicked2(self, event):
        x, y = event.x, event.y
        global nclic,key
        
        if nclic == 0:
            shortest=10000
            
            for k in range(len(dots)):
                dist=calc.Dist([x,y],[dots[k][0],dots[k][1]])
                if dist<shortest:
                    key=k
                    shortest=dist
                    
            if shortest>10:
                return
            
            nclic=1
            return 
        self.create_circle(dots[key][0], dots[key][1], 2, self.bg)
        dots[key][0], dots[key][1] = x, y
        self.create_circle(x, y, 2, self.config.get(str(self.theme), "dots"))
        nclic=0
        Disablecustom(self.config)
        calc.Voronoi(dots, self.offset, self.can, self.config, self.ntheme)

    def aprops(self):
        messagebox.showinfo("A propos", "Version:\t%s\nAuteurs:\tPierre-Yves Douault\n\tVincent Leurent\n\tPierre-Antoine Soyer" % (self.version))

class Disablecustom:
    def __init__(self, config):
        self.config = config
        self.config.set("config", "custom-plot", "0")
        
class Enablecustom:
    def __init__(self, config):
        self.config = config
        self.config.set("config", "custom-plot", "1")