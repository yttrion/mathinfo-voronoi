import tkinter as tk

import pygame

import time
import sys
import os
import platform

def clearScr():
    os.system("clear||cls")



class Splashscreen:

    def __init__(self, size):
        # Selection au cas où le script est lancé dans un système UNIX (OSX, BSD, Linux)
        dirr = "\\" if platform.system().lower() == "windows" else "/"
        curDir = os.path.dirname(os.path.abspath(__file__)) + dirr
        pygame.init()
        splash = pygame.mixer.Sound(curDir + "sounds" + dirr + "splash.wav")
        splash.play()
        clearScr()
        self.root = tk.Tk()
        self.width, self.height = size, size
        self.root.geometry(str(self.height)+"x"+str(self.height)+"+25+25")
        self.bg = "grey"
        self.title = self.root.title("【ＶＯＲＯＮＯＩ】")
        self.can = tk.Canvas(self.root, height=self.height,width=self.width, bg=self.bg)
        self.can.pack(side=tk.BOTTOM)
        self.keybind()
        self.root.mainloop()

    def keybind(self):
        self.root.bind('<Button-1>', self.vor

    def vor(self, event):
        
