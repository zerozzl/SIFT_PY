# coding: UTF-8
import numpy as np
import math
from GaussianBlur import GaussianBlur

# 构建高斯金字塔
def build_gaussian_pyramid(base, sigma_0, nOctaves, nOctaveLayers):
    print "Building gaussian pyramid......";
    sigmas = np.zeros(nOctaveLayers + 3);
    gpyr = [];
    
    sigmas[0] = sigma_0;
    k = math.pow(2.0, 1.0 / nOctaveLayers);
    
    for i in range(1, nOctaveLayers + 3):
        sig_pre = math.pow(k, i - 1) * sigma_0;
        sig_cur = sig_pre * k;
        sigmas[i] = np.sqrt(sig_cur * sig_cur - sig_pre * sig_pre);
    
    for o in range(nOctaves):
        for i in range(nOctaveLayers + 3):
            if o == 0 and i == 0:
                gpyr.append(base);
            elif i == 0:
                img = gpyr[(o - 1) * (nOctaveLayers + 3) + nOctaveLayers];
                gpyr.append(img.resize((img.size[0] / 2, img.size[1] / 2)));
            else:
                img = gpyr[o * (nOctaveLayers + 3) + i - 1];
                gpyr.append(img.filter(GaussianBlur(sigmas[i])));
    
    return gpyr;

# 构建高斯差分金字塔
def build_DoG_pyramid(gpyr, nOctaves, nOctaveLayers):
    print "Building DoG pyramid......";
    dogpyr = [];
    for o in range(nOctaves):
        for i in range(nOctaveLayers + 2):
            diff = np.array(gpyr[o*(nOctaveLayers + 3) + i]) - np.array(gpyr[o*(nOctaveLayers + 3) + i + 1]);
            dogpyr.append(diff);
    
    return dogpyr;
