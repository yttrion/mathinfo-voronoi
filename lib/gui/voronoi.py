#!/usr/bin/python
# -*- coding: utf-8 -*-

import tkinter as tk 

from tkinter import simpledialog, filedialog, messagebox

from itertools import combinations

import os
import time
import platform
import configparser

import pygame, time

import math
import random

def clearScr():
    os.system("clear||cls")

import lib.core.Calculus as calc

global dots, colors
dots, colors = [], []




class Main:
    
    def __init__(self, size, dirr):

        self.dirr = dirr
        self.curDir = os.path.dirname(os.path.abspath(__file__)) + self.dirr
        configfile = self.curDir + ".." + self.dirr + "config" + self.dirr + "vor.cfg"
        self.config = configparser.ConfigParser()
        self.config.read(configfile)

        
        pygame.init()
        main = pygame.mixer.Sound(self.curDir + "sounds" + self.dirr + "Mii.ogg")
        main.play(-1)
        clearScr()

        self.offset = 100000

        self.root = tk.Tk()
        self.width, self.height = size, size
        self.size = 2

        self.root.geometry(str(self.height)+"x"+str(self.height)+"+105+75")

        self.bg = "white"
        self.title = self.root.title("【ＶＯＲＯＮＯＩ】")


        self.can = tk.Canvas(self.root, height=self.height,width=self.width, bg=self.bg)
        self.can.pack(side=tk.BOTTOM)


        self.menubar = tk.Menu(self.root)
        self.root.config(menu=self.menubar)

        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Fichier", menu=self.filemenu)
        self.filemenu.add_command(label="Ouvrir")
        self.filemenu.add_command(label="Sauver")
        self.filemenu.add_command(label="Quitter")

        self.custommenu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Edition", menu=self.custommenu)
        self.custommenu.add_command(label="Création", command=self.enablecustom)
        self.custommenu.add_command(label="Aléatoire", command=self.randomize)
        self.custommenu.add_command(label="Voronoï")
        self.custommenu.add_command(label="Delaunay", command=self.rundel)
        self.custommenu.add_command(label="Triangulation", command=self.runtri)

        self.helpmenu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Aide", menu=self.helpmenu)
        self.helpmenu.add_command(label="A propos")
        self.helpmenu.add_command(label="Enfer du CPU")

        self.root.mainloop()

        

    def enablecustom(self):
        self.can.delete("all")
        dots.clear()
        self.config.set("config", "custom-plot", "1")
        self.root.bind('<Button-1>', self.clicked)

    def disbalecustom(self, event):
        self.config.set("config", "custom-plot", "0")    

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
                AIO(coord)
                    
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
            if len(dots)==15:
                messagebox.showinfo("Info", "Pas plus de 15 points sur le canvas")
                self.disbalecustom(self.motion)
            elif len(dots)<15:
                self.create_circle(x, y, 2, "black")
                
                col = '#%02x%02x%02x' % self.colourize()
                dots.append([x, y])
                colors.append(col)

    def randomize(self):
        self.config.set("config", "custom-plot", "0")
        n = simpledialog.askinteger("Nombre de points", "Entrez le nombre de points [2-15]",  minvalue=2)
        self.can.delete("all")
        dots.clear()

        for k in range(n):
            x, y = random.randint(20, self.width-20), random.randint(20, self.height-20)
            self.create_circle(x, y, 2, "black")
            col = '#%02x%02x%02x' % self.colourize()
            dots.append([x, y])
            colors.append(col)    
        
    def runtri(self):
        calc.Triangulation(dots, self.offset, self.can)

    def rundel(self):
        calc.Delaunay(dots, self.offset, self.can)




class Disablecustom:
    def __init__(self, config):
        self.config = config
        self.config.set("config", "custom-plot", "0")
        

class Enablecustom:
    def __init__(self, config):
        self.config = config
        self.config.set("config", "custom-plot", "1")