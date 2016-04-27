# coding: UTF-8
import numpy as np
import math
import Image
from GaussianBlur import GaussianBlur
import Others

def build_gaussian_pyramid(image, sigma_0, octave, scale):
    print "building gaussian pyramid......";
    sigmas = np.zeros(scale + 3);
    pyramid = [];
    
    sigmas[0] = sigma_0;
    k = math.pow(2.0, 1.0 / scale);
    
    for i in range(1, scale + 3):
        sig_pre = math.pow(k, i - 1) * sigma_0;
        sig_cur = sig_pre * k;
        sigmas[i] = np.sqrt(np.square(sig_cur) - np.square(sig_pre));
    
    for o in range(octave):
        print "process octave " + str(o + 1) + "/" + str(octave);
        oct_o = [];
        for i in range(scale + 3):
            if o == 0 and i == 0:
                oct_o.append(image);
            elif i == 0:
                img = pyramid[o - 1][scale];
                oct_o.append(img.resize((img.size[0] / 2, img.size[1] / 2)));
            else:
                img = oct_o[i - 1];
                img_blur = img.filter(GaussianBlur(sigmas[i]));
                oct_o.append(img_blur);
        pyramid.append(oct_o);
    
    return pyramid;

def build_DoG_pyramid(gaussian_pyramid):
    print "building DoG pyramid......";
    pyramid = [];
    octave = len(gaussian_pyramid);
    
    for o in range(octave):
        print "process octave " + str(o + 1) + "/" + str(octave);
        oct_o = [];
        scale = len(gaussian_pyramid[o]);
        for s in range(scale - 1):
            diff = np.array(gaussian_pyramid[o][s + 1]) - np.array(gaussian_pyramid[o][s]);
            oct_o.append(diff);
        pyramid.append(oct_o);
    
    return pyramid;
 
def build_pyramid(root, filename, sigma_0, scale, export=False):
    image = Image.open(root + filename);
    image = image.resize((2 * image.size[0], 2 * image.size[1])).convert("L");
    octave = int(np.log2(min(image.size))) - 3;
    
    # 构建高斯金字塔
    gaussian_pyramid = build_gaussian_pyramid(image, sigma_0, octave, scale);
    # 构建高斯差分金字塔
    dog_pyramid = build_DoG_pyramid(gaussian_pyramid);
    
    if export == True:
        # 导出高斯金字塔
        gaussian_pyramid_folder = root + "/gaussian_pyramid/";
        gaussian_pyramid_file = gaussian_pyramid_folder + "gaussian_pyramid.txt";
        Others.export_pyramid(gaussian_pyramid_file, gaussian_pyramid);
        Others.plot_pyramid(gaussian_pyramid_file, gaussian_pyramid_folder)

        # 导出高斯差分金字塔
        dog_pyramid_folder = root + "/dog_pyramid/";
        dog_pyramid_file = dog_pyramid_folder + "dog_pyramid.txt";
        Others.export_pyramid(dog_pyramid_file, dog_pyramid);
        Others.plot_pyramid(dog_pyramid_file, dog_pyramid_folder)
    
    return dog_pyramid;
