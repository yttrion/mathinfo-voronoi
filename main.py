#!/usr/bin/python
# -*- coding: utf-8 -*-

import tkinter as Tk
import sys
import os
import threading

class interface:
    def __init__(self):
        self.root = Tk.Tk()
        self.height = 400
        self.width = 400
        self.title = self.root.title("Voronoi")
        self.menubar = Tk.Menu(self.root)
        self.root.config(menu=self.menubar)
        
        self.filemenu = Tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="File", menu=self.filemenu)
        self.filemenu.add_command(label="Open")
        self.filemenu.add_command(label="Run")
        self.filemenu.add_command(label="Quit")
        
        self.custommenu = Tk.Menu(self.menubar, tearoff=1)
        self.menubar.add_cascade(label="Custom", menu=self.filemenu)
        self.custommenu.add_command(label="Create points")
        self.custommenu.add_command(label="Drag")
        
        self.savemenu = Tk.Menu(self.menubar, tearoff=2)
        self.menubar.add_cascade(label="Save", menu=self.filemenu)
        self.savemenu.add_command(label="Save plots")
        

        #self.can = Tk.Canvas(self.root, height=self.height, width=self.width)
        #self.can.pack(side=Tk.BOTTOM)
        self.root.mainloop()

if __name__=="__main__":
    interface()