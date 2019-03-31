'''
Created on Mar 30, 2019

@author: Jiaming
'''
from PIL import Image
from PIL import ImageTk
import tkinter as tk


class WordCard:
    def __init__(self, name, image_url, index, width = 200, height=200):
        self.name = name
        self.width = width
        self.height = height
        self.index = index
        self.image = self.resize_image(Image.open(image_url))
        
        
        
        
    def resize_image(self, im):
        im = im.resize((self.width, self.height), Image.ANTIALIAS)
        return ImageTk.PhotoImage(im)
    
