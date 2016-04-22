# coding: UTF-8
import numpy as np
import math
import Image
import matplotlib.pyplot as plt

# img_src = Image.open("Z:/SIFT/my.png");
# width, height = img_src.size;
# img_lar = img_src.resize((2 * width, 2 * height));
# 
# print img_src.size;
# print img_lar.size;
# 
# 
# fig = plt.figure();
# ax1 = fig.add_subplot(121);
# ax2 = fig.add_subplot(122);
# ax1.imshow(img_src);
# ax2.imshow(img_lar);
# plt.show();
# 
# img_lar.save("Z:/SIFT/my_l.jpg") 

def build_gaussian_pyramid(image, sigma_0, octave, scale):
    sigmas = np.zeros(scale + 3);
    pyramid = [];
    
    sigmas[0] = sigma_0;
    k = math.pow(2.0, 1.0 / scale);
    
    for i in range(1, scale + 3):
        sig_pre = math.pow(k, i - 1) * sigma_0;
        sig_cur = sig_pre * k;
        sigmas[i] = np.sqrt(np.square(sig_cur) - np.square(sig_pre));
    
    for o in range(octave):
        target = [];
        for i in range(scale):
            if o == 0 and i == 0:
                target.append(image);
            elif i == 0:
                pass;
#                 img = pyramid[o - 1][scale];
#                 
#                 target.append();
    
    print sigmas;
    
def build(filepath):
    image = Image.open(filepath);
    image = image.resize((2 * image.size[0], 2 * image.size[1])).convert("L");
    octave = int(np.log2(min(image.size))) - 2;
    sigma_0 = 1.6;
    scale = 3;
    
    image = np.array(image);
    build_gaussian_pyramid(image, sigma_0, octave, scale);

filepath = "Z:/SIFT/my.png";
build(filepath);
