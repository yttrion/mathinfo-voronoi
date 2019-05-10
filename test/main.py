#!/usr/bin/python
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import simpledialog
from tkinter import filedialog

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

global dots, H, W, offset
dots = []
H = 400
W = 400
offset = 100


class Interface:
    def __init__(self):
        self.root = tk.Tk()
        self.height = H
        self.width = W
        self.bg = "white"
        self.title = self.root.title("Voronoi")
        self.menubar = tk.Menu(self.root)
        self.root.config(menu=self.menubar)
        
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="File", menu=self.filemenu)
        self.filemenu.add_command(label="Open", command=self.openfile)
        self.filemenu.add_command(label="Run")
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
        dots = []
        for k in range(n):
            x, y = random.randint(10,W-10), random.randint(10,H-10)
            self.can.create_oval(x+2,y+2,x-2,y-2, fill="black", tags=str(x)+','+str(y))
            dots.append([x,y])

    def openfile(self):
        self.root.filename = filedialog.askopenfilename(initialdir = dir,title = "Select file",filetypes = (("Plain text files","*.txt"),("All files","*.*")))

    def keybind(self):
        self.root.bind('<Motion>', self.motion)
        self.root.bind('<Escape>', self.disbalecustom)



if __name__=="__main__":
    Interface() 