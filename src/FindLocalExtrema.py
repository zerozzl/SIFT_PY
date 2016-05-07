# coding: UTF-8
import Others
import numpy as np
import matplotlib.pyplot as plt

SIFT_FIXPT_SCALE = 1;
SIFT_MAX_INTERP_STEPS = 5;
SIFT_IMG_BORDER = 1;

pyramid = Others.load_pyramid("Z:/SIFT/dog_pyramid/dog_pyramid.txt");
octave = 1;
layer = 1;
sigma_0 = 1.6;
scale = 3;
contrastThreshold = 1;
edgeThreshold = 1;

def adjustLocalExtrema(dog_pyr, keypoints, octave, layer, row, col,
                       scale, contrastThreshold, edgeThreshold, sigma_0):
    img_scale = 1.0 / (255 * SIFT_FIXPT_SCALE);  # 1 / h, 255是为了归一化
    deriv_scale = 0.5 * img_scale;  # 1 / 2h
    second_deriv_scale = img_scale;  # 1 / h^2, h等于1，所以可以直接表示
    cross_deriv_scale = 0.25 * img_scale;  # 1 / (4 * h^2), h等于1，所以可以直接表示
    
    i = 0;
    
    while(i < SIFT_MAX_INTERP_STEPS):
        img = dog_pyr[octave][layer];
        prev_l = dog_pyr[octave][layer - 1];
        next_l = dog_pyr[octave][layer + 1];
        
        dD = np.array([(img[row, col + 1] - img[row, col - 1]) * deriv_scale,
                       (img[row + 1, col] - img[row - 1, col]) * deriv_scale,
                       (next_l[row, col] - prev_l[row, col]) * deriv_scale]);
        
        dcc = (img[row, col + 1] + img[row, col - 1] - img[row, col] * 2) * second_deriv_scale;
        drr = (img[row + 1, col] + img[row - 1, col] - img[row, col] * 2) * second_deriv_scale;
        dll = (next_l[row, col] + prev_l[row, col] - img[row, col] * 2) * second_deriv_scale;
        
        dcr = (img[row + 1, col + 1] - img[row + 1, col - 1] - img[row - 1, col + 1] + 
                img[row - 1, col - 1]) * cross_deriv_scale;
        dcl = (next_l[row, col + 1] - next_l[row, col - 1] - prev_l[row, col + 1] + 
               prev_l[row, col - 1]) * cross_deriv_scale;
        drl = (next_l[row + 1, col] - next_l[row - 1, col] - prev_l[row + 1, col] + 
               prev_l[row - 1, col]) * cross_deriv_scale;
        
        H = np.mat([[dcc, dcr, dcl],
                    [dcr, drr, drl],
                    [dcl, drl, dll]]);
        
        try:
            X = np.linalg.solve(H, dD);
        except Exception:
            return False;
        
        xc = -X[0];
        xr = -X[1];
        xl = -X[2];
        
        if(np.abs(xc) < 0.5 and np.abs(xr) < 0.5 and np.abs(xl) < 0.5):
            break;
        
        col = int(col + round(xc));
        row = int(row + round(xr));
        layer = int(layer + round(xl));
        
        img_size = np.shape(img);
        if(layer < 1 or layer > scale
           or col < SIFT_IMG_BORDER or col >= img_size[1] - SIFT_IMG_BORDER
           or row < SIFT_IMG_BORDER or row >= img_size[0] - SIFT_IMG_BORDER):
            return False;
        
        i += 1;
    
    if i >= SIFT_MAX_INTERP_STEPS:
        return False;
    
    keypoints.append([row, col, 1]);

target = pyramid[1];
m, n = np.shape(target[layer]);
keypoints = [];
for i in range(1, m - 1):
    for j in range(1, n - 1):
        cur = target[layer][i, j];
        if ((cur > 0 and cur >= target[layer - 1][i - 1, j - 1] and cur >= target[layer - 1][i - 1, j]
            and cur >= target[layer - 1][i - 1, j + 1] and cur >= target[layer - 1][i, j - 1]
            and cur >= target[layer - 1][i, j] and cur >= target[layer - 1][i, j + 1]
            and cur >= target[layer - 1][i + 1, j - 1] and cur >= target[layer - 1][i + 1, j]
            and cur >= target[layer - 1][i + 1, j + 1] and cur >= target[layer][i - 1, j - 1]
            and cur >= target[layer][i - 1, j] and cur >= target[layer][i - 1, j + 1]
            and cur >= target[layer][i, j - 1] and cur >= target[layer][i, j + 1]
            and cur >= target[layer][i + 1, j - 1] and cur >= target[layer][i + 1, j]
            and cur >= target[layer][i + 1, j + 1] and cur >= target[layer + 1][i - 1, j - 1]
            and cur >= target[layer + 1][i - 1, j] and cur >= target[layer + 1][i - 1, j + 1]
            and cur >= target[layer + 1][i, j - 1] and cur >= target[layer + 1][i, j]
            and cur >= target[layer + 1][i, j + 1] and cur >= target[layer + 1][i + 1, j - 1]
            and cur >= target[layer + 1][i + 1, j]
            and cur >= target[layer + 1][i + 1, j + 1])) or ((cur <= target[layer - 1][i - 1, j - 1]
            and cur <= target[layer - 1][i - 1, j]
            and cur <= target[layer - 1][i - 1, j + 1] and cur <= target[layer - 1][i, j - 1]
            and cur <= target[layer - 1][i, j] and cur <= target[layer - 1][i, j + 1]
            and cur <= target[layer - 1][i + 1, j - 1] and cur <= target[layer - 1][i + 1, j]
            and cur <= target[layer - 1][i + 1, j + 1] and cur <= target[layer][i - 1, j - 1]
            and cur <= target[layer][i - 1, j] and cur <= target[layer][i - 1, j + 1]
            and cur <= target[layer][i, j - 1] and cur <= target[layer][i, j + 1]
            and cur <= target[layer][i + 1, j - 1] and cur <= target[layer][i + 1, j]
            and cur <= target[layer][i + 1, j + 1] and cur <= target[layer + 1][i - 1, j - 1]
            and cur <= target[layer + 1][i - 1, j] and cur <= target[layer + 1][i - 1, j + 1]
            and cur <= target[layer + 1][i, j - 1] and cur <= target[layer + 1][i, j]
            and cur <= target[layer + 1][i, j + 1] and cur <= target[layer + 1][i + 1, j - 1]
            and cur <= target[layer + 1][i + 1, j] and cur <= target[layer + 1][i + 1, j + 1])):
            adjustLocalExtrema(pyramid, keypoints, octave, layer, i, j,
                       scale, contrastThreshold, edgeThreshold, sigma_0);

img = np.ones((m, n));
for point in keypoints:
    img[point[0], point[1]] = 0;
 
fig = plt.figure();
ax = fig.add_subplot(111);
ax.imshow(img, cmap="gray");
plt.show();
 
print 'success'
