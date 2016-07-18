# coding: UTF-8
import numpy as np
import math
from KeyPoint import KeyPoint

def findScaleSpaceExtrema(gpyr, dogpyr, nOctaves, nOctaveLayers,
                          contrastThreshold, edgeThreshold, sigma,
                          SIFT_FIXPT_SCALE, SIFT_IMG_BORDER,
                          SIFT_MAX_INTERP_STEPS, SIFT_ORI_HIST_BINS,
                          SIFT_ORI_SIG_FCTR, SIFT_ORI_RADIUS):
    print "Finding scale space extrema......";
    threshold = math.floor(0.5 * contrastThreshold / nOctaveLayers * 255 * SIFT_FIXPT_SCALE);
    n = SIFT_ORI_HIST_BINS;
    keypoints = [];
    
    for o in range(nOctaves):
        for i in range(1, nOctaveLayers + 1):
            idx = o * (nOctaveLayers + 2) + i;
            img = dogpyr[idx];
            prev_l = dogpyr[idx - 1];
            next_l = dogpyr[idx + 1];
            rows, cols = np.shape(img);
            
            for r in range(SIFT_IMG_BORDER, rows - SIFT_IMG_BORDER):
                for c in range(SIFT_IMG_BORDER, cols - SIFT_IMG_BORDER):
                    val = img[r, c];
                    if (np.abs(val) > threshold and
                        ((val > 0 and val >= img[r - 1, c - 1] and val >= img[r - 1, c]
                        and val >= img[r - 1, c + 1] and val >= img[r, c - 1]
                        and val >= img[r, c + 1] and val >= img[r + 1, c - 1]
                        and val >= img[r + 1, c] and val >= img[r + 1, c + 1]
                        and val >= prev_l[r - 1, c - 1] and val >= prev_l[r - 1, c]
                        and val >= prev_l[r - 1, c + 1] and val >= prev_l[r, c - 1]
                        and val >= prev_l[r, c] and val >= prev_l[r, c + 1]
                        and val >= prev_l[r + 1, c - 1] and val >= prev_l[r + 1, c]
                        and val >= prev_l[r + 1, c + 1]
                        and val >= next_l[r - 1, c - 1] and val >= next_l[r - 1, c]
                        and val >= next_l[r - 1, c + 1] and val >= next_l[r, c - 1]
                        and val >= next_l[r, c] and val >= next_l[r, c + 1]
                        and val >= next_l[r + 1, c - 1] and val >= next_l[r + 1, c]
                        and val >= next_l[r + 1, c + 1])
                         or (val < 0 and val <= img[r - 1, c - 1] and val <= img[r - 1, c]
                        and val <= img[r - 1, c + 1] and val <= img[r, c - 1]
                        and val <= img[r, c + 1] and val <= img[r + 1, c - 1]
                        and val <= img[r + 1, c] and val <= img[r + 1, c + 1]
                        and val <= prev_l[r - 1, c - 1] and val <= prev_l[r - 1, c]
                        and val <= prev_l[r - 1, c + 1] and val <= prev_l[r, c - 1]
                        and val <= prev_l[r, c] and val <= prev_l[r, c + 1]
                        and val <= prev_l[r + 1, c - 1] and val <= prev_l[r + 1, c]
                        and val <= prev_l[r + 1, c + 1]
                        and val <= next_l[r - 1, c - 1] and val <= next_l[r - 1, c]
                        and val <= next_l[r - 1, c + 1] and val <= next_l[r, c - 1]
                        and val <= next_l[r, c] and val <= next_l[r, c + 1]
                        and val <= next_l[r + 1, c - 1] and val <= next_l[r + 1, c]
                        and val <= next_l[r + 1, c + 1]))):
                        r1 = r; c1 = c; lay = i;
                        isKpt, kpt, layer, row, col = adjustLocalExtrema(dogpyr, o, lay, r1, c1,
                                                nOctaveLayers, contrastThreshold,
                                                edgeThreshold, sigma,
                                                SIFT_FIXPT_SCALE, SIFT_IMG_BORDER,
                                                SIFT_MAX_INTERP_STEPS);
                        if(not isKpt):
                            continue;
                        
                        scl_octv = kpt.size * 0.5 / (1 << o);
                        omax = calcOrientationHist(
                                    gpyr[o * (nOctaveLayers + 3) + layer],
                                    [row, col],
                                    round(SIFT_ORI_RADIUS * scl_octv),
                                    SIFT_ORI_SIG_FCTR * scl_octv, n);
                        
                        keypoints.append(kpt);
    
    print len(keypoints);             
    pass;

# 特征点精确定位
def adjustLocalExtrema(dog_pyr, octv, layer, row, col, nOctaveLayers,
                       contrastThreshold, edgeThreshold, sigma,
                       SIFT_FIXPT_SCALE, SIFT_IMG_BORDER, SIFT_MAX_INTERP_STEPS):
    img_scale = 1.0 / (255 * SIFT_FIXPT_SCALE);  # 1 / h, 255是为了归一化
    deriv_scale = 0.5 * img_scale;  # 1 / 2h
    second_deriv_scale = img_scale;  # 1 / h^2, h等于1，所以可以直接表示
    cross_deriv_scale = 0.25 * img_scale;  # 1 / (4 * h^2), h等于1，所以可以直接表示
     
    xc = 0; xr = 0; xi = 0;
    i = 0;
     
    while(i < SIFT_MAX_INTERP_STEPS):
        idx = octv * (nOctaveLayers + 2) + layer;  
        img = dog_pyr[idx];  
        prev_l = dog_pyr[idx - 1];  
        next_l = dog_pyr[idx + 1]; 
        
        dD = np.array([(img[row, col + 1] - img[row, col - 1]) * deriv_scale,
                       (img[row + 1, col] - img[row - 1, col]) * deriv_scale,
                       (next_l[row, col] - prev_l[row, col]) * deriv_scale]);
        
        dcc = (img[row, col + 1] + img[row, col - 1] - img[row, col] * 2.0) * second_deriv_scale;
        drr = (img[row + 1, col] + img[row - 1, col] - img[row, col] * 2.0) * second_deriv_scale;
        dll = (next_l[row, col] + prev_l[row, col] - img[row, col] * 2.0) * second_deriv_scale;
        
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
            return False, None, None, None, None;
        
        xc = -X[0];
        xr = -X[1];
        xi = -X[2];
        
        if(np.abs(xc) < 0.5 and np.abs(xr) < 0.5 and np.abs(xi) < 0.5):
            break;
        
        col = int(col + round(xc));
        row = int(row + round(xr));
        layer = int(layer + round(xi));
        
        img_size = np.shape(img);
        if(layer < 1 or layer > nOctaveLayers
           or col < SIFT_IMG_BORDER or col >= img_size[1] - SIFT_IMG_BORDER
           or row < SIFT_IMG_BORDER or row >= img_size[0] - SIFT_IMG_BORDER):
            return False, None, None, None, None;
        
        i += 1;
    
    if i >= SIFT_MAX_INTERP_STEPS:
        return False, None, None, None, None;
    
    idx = octv * (nOctaveLayers + 2) + layer;
    img = dog_pyr[idx];
    prev_l = dog_pyr[idx - 1];
    next_l = dog_pyr[idx + 1];
     
    dD = np.array([(img[row, col + 1] - img[row, col - 1]) * deriv_scale,
                   (img[row + 1, col] - img[row - 1, col]) * deriv_scale,
                   (next_l[row, col] - prev_l[row, col]) * deriv_scale]);
     
    contr = img[row, col] * img_scale + np.dot(dD, [xc, xr, xi]) * 0.5;
    if(np.abs(contr) * nOctaveLayers < contrastThreshold):
        return False, None, None, None, None;
      
    dcc = (img[row, col + 1] + img[row, col - 1] - img[row, col] * 2.0) * second_deriv_scale;
    drr = (img[row + 1, col] + img[row - 1, col] - img[row, col] * 2.0) * second_deriv_scale;
    dcr = (img[row + 1, col + 1] - img[row + 1, col - 1] - img[row - 1, col + 1] + 
            img[row - 1, col - 1]) * cross_deriv_scale;
    tr = dcc + drr;
    det = dcc * drr - dcr * dcr;
    
    if(det <= 0 or tr * tr * edgeThreshold >= (edgeThreshold + 1) * (edgeThreshold + 1) * det):
        return False, None, None, None, None;
    
    kpt = KeyPoint((col + xc) * (1 << octv),
                   (row + xr) * (1 << octv),
                   octv + (layer << 8) + (int(round((xi + 0.5) * 255)) << 16),
                   sigma * math.pow(2.0, (layer + xi) / nOctaveLayers) * (1 << octv) * 2,
                   np.abs(contr));
    
    return True, kpt, layer, row, col;

# 计算特定点的梯度方向直方图
def calcOrientationHist(img, pt, radius, sigma, n):
    len = (radius * 2 + 1) * (radius * 2 + 1);
    expf_scale = -1.0 / (2.0 * sigma * sigma);

