#-*- coding: utf-8 -*-
from PIL import Image, ImageFilter
import math

# 高斯模糊
class GaussianBlur(ImageFilter.Filter):
    
    def __init__(self, sigma):
        self.radius = math.ceil(sigma * 3)
    
    def filter(self, image):
        return image.gaussian_blur(self.radius)
