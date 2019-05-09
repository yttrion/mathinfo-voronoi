#!/usr/bin/python
# -*- coding: utf-8 -*-

import tkinter as Tk
import sys
import os
import threading
import configparser


curDir = os.path.dirname(os.path.abspath(__file__)) + '/'
configFile = curDir + "./vor.cfg"
config = configparser.ConfigParser()
config.read(configFile)

def clearScr():
    os.system("clear||cls")

class interface:
    def __init__(self):
        self.root = Tk.Tk()
        self.height = 400
        self.width = 400
        self.bg = "white"
        self.title = self.root.title("Voronoi")
        self.menubar = Tk.Menu(self.root)
        self.root.config(menu=self.menubar)
        
        self.filemenu = Tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="File", menu=self.filemenu)
        self.filemenu.add_command(label="Open")
        self.filemenu.add_command(label="Run", command=run())
        self.filemenu.add_command(label="Quit", command=self.root.destroy)
        
        self.custommenu = Tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Custom", menu=self.custommenu)
        self.custommenu.add_command(label="Create points", command=self.enablecustom)
        
        self.savemenu = Tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Save", menu=self.savemenu)
        self.savemenu.add_command(label="Save plots")

        self.can = Tk.Canvas(self.root, height=self.height, width=self.width, bg=self.bg)
        self.can.pack(side=Tk.BOTTOM)
        self.root.bind('<Motion>', self.motion)
        self.root.bind('<Escape>', self.disbalecustom)
        self.root.mainloop()

    def motion(self, event):
        x, y = event.x, event.y
        print("%s - %s" % (x, y))

    def clicked(self, event):
        x, y = event.x, event.y
        if config.getboolean("config", "custom-plot"):
            self.can.create_oval(x+2,y+2,x-2,y-2, fill="red", tags=str(x)+','+str(y))
        else:
            clearScr()

    def enablecustom(self):
        config.set("config","custom-plot", "1")
        self.root.bind('<Button-1>', self.clicked)
    
    def disbalecustom(self, event):
        config.set("config","custom-plot", "0")


class run:
    def __init__(self):















if __name__=="__main__":
    interface()