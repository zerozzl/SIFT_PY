# coding: UTF-8
import numpy as np
import math
from GaussianBlur import GaussianBlur

import cv2

# 构建高斯金字塔
def build_gaussian_pyramid(base, sigma, nOctaves, nOctaveLayers):
    print "Building gaussian pyramid......";
    sig = np.zeros(nOctaveLayers + 3);
    gpyr = [];
    
    sig[0] = sigma;
    k = math.pow(2.0, 1.0 / nOctaveLayers);
    
    for i in range(1, nOctaveLayers + 3):
        sig_pre = math.pow(k, i - 1) * sigma;
        sig_cur = sig_pre * k;
        sig[i] = np.sqrt(sig_cur * sig_cur - sig_pre * sig_pre);
    
    for o in range(nOctaves):
        for i in range(nOctaveLayers + 3):
            if o == 0 and i == 0:
                gpyr.append(base);
            elif i == 0:
                img = gpyr[(o - 1) * (nOctaveLayers + 3) + nOctaveLayers];
                gpyr.append(img.resize((img.size[0] / 2, img.size[1] / 2)));
            else:
                img = gpyr[o * (nOctaveLayers + 3) + i - 1];
                gpyr.append(img.filter(GaussianBlur(sig[i])));
    
    return gpyr;

# 构建高斯差分金字塔
def build_DoG_pyramid(gpyr, nOctaves, nOctaveLayers):
    print "Building DoG pyramid......";
    dogpyr = [];
    for o in range(nOctaves):
        for i in range(nOctaveLayers + 2):
            src1 = gpyr[o * (nOctaveLayers + 3) + i];
            src2 = gpyr[o * (nOctaveLayers + 3) + i + 1];
            height, width = np.shape(src1);
            src1= np.reshape(src1.getdata(), (height, width));
            src2= np.reshape(src2.getdata(), (height, width));
            diff = src2 - src1;
            dogpyr.append(diff);
    
    return dogpyr;
