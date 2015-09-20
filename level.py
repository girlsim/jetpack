import pygame
from PIL import Image

import tiles

class Level:

    def __init__(self,image):
        # load map from an image
        im = Image.open(image)
        pixels = im.load()
        (width,height) = im.size
        self.map = []
        (x,y) = (0,0)
        while y < height:
            x = 0
            ll = []
            while x < width:
                (r,g,b) = pixels[x,y]
                # hacky but simple: list value = r+g+b % 50
                ll.append((r+g+b)%50)
                x += 1
            self.map.append(ll)
            y += 1
