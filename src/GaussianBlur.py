#-*- coding: utf-8 -*-
from PIL import Image, ImageFilter
import math

class GaussianBlur(ImageFilter.Filter):
    
    def __init__(self, sigma):
        self.radius = math.ceil(sigma * 3)
    
    def filter(self, image):
        return image.gaussian_blur(self.radius)
