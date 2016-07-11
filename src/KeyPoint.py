# coding: UTF-8

# 关键点
class KeyPoint:
    
    def __init__(self, x, y, octave, size, contr):
        self.x = x;
        self.y = y;
        self.octave = octave;
        self.size = size;
        self.response = contr;
