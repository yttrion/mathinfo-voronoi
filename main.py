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
        self.bg = "white"
        self.title = self.root.title("Voronoi")
        self.menubar = Tk.Menu(self.root)
        self.root.config(menu=self.menubar)
        
        self.filemenu = Tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="File", menu=self.filemenu)
        self.filemenu.add_command(label="Open")
        self.filemenu.add_command(label="Run")
        self.filemenu.add_command(label="Quit")
        
        self.custommenu = Tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Custom", menu=self.custommenu)
        self.custommenu.add_command(label="Create points")
        self.custommenu.add_command(label="Drag")
        
        self.savemenu = Tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Save", menu=self.savemenu)
        self.savemenu.add_command(label="Save plots")

        self.can = Tk.Canvas(self.root, height=self.height, width=self.width, bg=self.bg)
        self.can.pack(side=Tk.BOTTOM)
        self.root.bind('<Motion>', self.motion)
        self.root.bind('<Button-1>', self.clicked)
        self.root.mainloop()

    def motion(self, event):
        x, y = event.x, event.y
        print("%s - %s" % (x, y))

    def clicked(self, event):
        x, y = event.x, event.y
        self.can.create_oval(x+2,y+2,x-2,y-2, fill="red")














if __name__=="__main__":
    interface()