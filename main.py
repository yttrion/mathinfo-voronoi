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


#Importation des fichiers dans lib/
import lib.gui.splash as sp
import lib.gui.voronoi as vor


# Selection au cas où le script est lancé dans un système UNIX (OSX, BSD, Linux)
dirr = "\\" if platform.system().lower() == "windows" else "/"

curDir = os.path.dirname(os.path.abspath(__file__)) + dirr
configfile = curDir + "lib" + dirr + "config" + dirr + "vor.cfg"
config = configparser.ConfigParser()
config.read(configfile)


class Startup:
    s = config.getint("config", "size")
    sp.Splashscreen(s)




Startup()