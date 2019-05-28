import tkinter as tk

import time
import sys
import os
import platform
import math


from PIL import ImageTk, Image



def clearScr():
    os.system("clear||cls")



class Splashscreen:

    def __init__(self, dirr, config):

        curDir = os.path.dirname(os.path.abspath(__file__)) + dirr
        clearScr()
        if config.getboolean("config", "extras"):
            import pygame
            pygame.init()
            splash = pygame.mixer.Sound(curDir + "sounds" + dirr + "splash.wav")
            splash.play()            

        self.root = tk.Tk()

        self.bg = "grey"
        self.title = self.root.title("Booting...")
        self.can = tk.Canvas(self.root, height=424,width=356, bg=self.bg)
        self.can.pack()

        #Splash screen
        self.img = curDir + "assets" + dirr + "splash.png"
        self.bg = ImageTk.PhotoImage(file=self.img)
        self.can.create_image(1,1,image=self.bg, anchor="nw")

        #Delay avant destruction
        self.root.after(2000, lambda: self.root.destroy())
        self.root.mainloop()