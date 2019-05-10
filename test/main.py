#!/usr/bin/python
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import simpledialog
from tkinter import filedialog


from itertools import combinations

import sys
import os
import threading
import platform
import numpy as np
import math
import random
import configparser

if platform.system().lower() == "windows":
    dirr="\\"
else:
    dirr ="/"

curDir = os.path.dirname(os.path.abspath(__file__)) + dirr
configfile = curDir + "vor.cfg"
config = configparser.ConfigParser()
config.read(configfile)

def clearScr():
    os.system("clear||cls")

global dots, H, W, offset, flag, tri

dots = []
H = 400
W = 400
offset = 100
tri = None
flag = True

class Interface:
    def __init__(self):
        clearScr()
        self.root = tk.Tk()
        self.width = W
        self.height = H
        self.root.geometry(str(H)+"x"+str(W)+"+100+100")
        self.bg = "white"
        self.title = self.root.title("Voronoi")
        self.menubar = tk.Menu(self.root)
        self.root.config(menu=self.menubar)
        
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="File", menu=self.filemenu)
        self.filemenu.add_command(label="Open", command=self.openfile)
        self.filemenu.add_command(label="Run", command=self.drawtri)
        self.filemenu.add_command(label="Quit", command=self.root.destroy)
        
        self.custommenu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Edit", menu=self.custommenu)
        self.custommenu.add_command(label="Create dots", command=self.enablecustom)
        self.custommenu.add_command(label="Randomize", command=self.randomize)
        self.custommenu.add_command(label="Drag & drop")
        
        self.savemenu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Save", menu=self.savemenu)
        self.savemenu.add_command(label="Save plots")

        self.can = tk.Canvas(self.root, height=self.height, width=self.width, bg=self.bg)
        self.can.pack(side=tk.BOTTOM)
        self.keybind()

        self.root.mainloop()

    def motion(self, event):
        x, y = event.x, event.y

    def clicked(self, event):
        x, y = event.x, event.y
        if config.getboolean("config", "custom-plot"):
            self.can.create_oval(x+2,y+2,x-2,y-2, fill="red", tags=str(x)+','+str(y))
            dots.append([x,y])

    def enablecustom(self):
        config.set("config","custom-plot", "1")
        self.root.bind('<Button-1>', self.clicked)
    
    def disbalecustom(self, event):
        config.set("config","custom-plot", "0")


    def randomize(self):
        config.set("config","custom-plot", "0")
        n = simpledialog.askinteger("Number of dots", self.root)
        self.can.delete("all")
        dots.clear()
        for k in range(n):
            x, y = random.randint(10,W-10), random.randint(10,H-10)
            self.can.create_oval(x+2,y+2,x-2,y-2, fill="black", tags=str(x)+','+str(y))
            dots.append([x,y])

    def openfile(self):
        self.root.filename = filedialog.askopenfilename(initialdir = dir,title = "Select file",filetypes = (("Plain text files","*.txt"),("All files","*.*")))

    def keybind(self):
        self.root.bind('<Motion>', self.motion)
        self.root.bind('<Escape>', self.disbalecustom)











    def triang(self):
        global output
        listetri = list(combinations(dots, 3))
        flag = True
        listed=[]
        trivide = []
        output = []

        for tri in listetri:
            #print("Tour: ",tri)
            #Premiere mediatrice
            a1 = 2 * (tri[1][0]-tri[0][0])
            b1 = 2 * (tri[1][1]-tri[0][1])
            c1 = (tri[0][0])**2 + (tri[0][1])**2 - (tri[1][0])**2 - (tri[1][1])**2
            #Deuxieme mediatrice
            a2 = 2 * (tri[2][0]-tri[1][0])
            b2 = 2 * (tri[2][1]-tri[1][1])
            c2 = (tri[1][0])**2 + (tri[1][1])**2 - (tri[2][0])**2 - (tri[2][1])**2
            #Intersection
            X = (c1*b2 - c2*b1)//(a2*b1 - a1*b2)
            Y = (c1*a2 - a1*c2)//(a1*b2 - b1*a2)
            center = [X,Y]
            r = math.sqrt((tri[1][0] - center[0])**2 + (tri[1][1] - center[1])**2)

            #Verification conditions delaunay
            for p in dots:
                if not(p in tri):
                    dist = (p[0] - center[0])**2 + (p[1] - center[1])**2
                    listed.append(dist)
                for d in listed:
                    if d<=r:
                        flag=False
                        break;
            if flag is True:
                trivide.append(tri)
        output = trivide
    
    def listcenter(self):
        global out1
        liste = []
        out1 = []

        self.triang()

        for p in output:
            a1 = 2 * (p[1][0]-p[0][0])
            b1 = 2 * (p[1][1]-p[0][1])
            c1 = (p[0][0])**2 + (p[0][1])**2 - (p[1][0])**2 - (p[1][1])**2
            #Deuxieme mediatrice
            a2 = 2 * (p[2][0]-p[1][0])
            b2 = 2 * (p[2][1]-p[1][1])
            c2 = (p[1][0])**2 + (p[1][1])**2 - (p[2][0])**2 - (p[2][1])**2
            #Intersection
            X = (c1*b2 - c2*b1)//(a2*b1 - a1*b2)
            Y = (c1*a2 - a1*c2)//(a1*b2 - b1*a2)
            center = [X,Y]
            liste.append(center)
        out1 = liste
    
        
    
    def drawtri(self):
        self.listcenter()
        print(out1)


        for j in range(len(out1)):
            x1, y1 = out1[j][0], out1[j][1]
            #x2, y2 = out1[j-1][0], out1[j-1][1]
            self.can.create_oval(x1,y1,x1+7,y1+7, fill="red")


        #for n in out1:
        #    self.can.create_line(n[0],n[1], fill="red")
    
    













if __name__=="__main__":
    Interface() 