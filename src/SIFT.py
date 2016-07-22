# coding: UTF-8
import Image
import numpy as np
import BuildPyramid
from GaussianBlur import GaussianBlur
import FindLocalExtrema
import Others
import os

class SIFT:
    
    '''
    nfeatures 特征点数目（算法对检测出的特征点排名，返回最好的nfeatures个特征点, 如果nfeatures=0，则表示输出所有的特征点）
    nOctaveLayers 金字塔中每组的层数
    contrastThreshold 过滤掉较差的特征点的对阈值。contrastThreshold越大，返回的特征点越少
    edgeThreshold 过滤掉边缘效应的阈值。edgeThreshold越大，特征点越多（被多滤掉的越少）
    sigma 金字塔第0层图像高斯滤波系数，也就是σ
    '''
    def __init__(self, nfeatures=0, nOctaveLayers=3,
                 contrastThreshold=0.04, edgeThreshold=10, sigma=1.6):
        # default width of descriptor histogram array
        self.SIFT_DESCR_WIDTH = 4;
        
        # default number of bins per histogram in descriptor array
        self.SIFT_DESCR_HIST_BINS = 8;
        
        # assumed gaussian blur for input image
        self.SIFT_INIT_SIGMA = 0.5;
        
        # width of border in which to ignore keypoints
        self.SIFT_IMG_BORDER = 5;
        
        # maximum steps of keypoint interpolation before failure
        self.SIFT_MAX_INTERP_STEPS = 5;
        
        # default number of bins in histogram for orientation assignment
        self.SIFT_ORI_HIST_BINS = 36;
        
        # determines gaussian sigma for orientation assignment
        self.SIFT_ORI_SIG_FCTR = 1.5;
        
        # determines the radius of the region used in orientation assignment
        self.SIFT_ORI_RADIUS = 3 * self.SIFT_ORI_SIG_FCTR;
        
        # orientation magnitude relative to max that results in new feature
        # self.SIFT_ORI_PEAK_RATIO = 0.8;
        
        # determines the size of a single descriptor orientation histogram
        # self.SIFT_DESCR_SCL_FCTR = 3.0;
        
        # threshold on magnitude of elements of descriptor vector
        # self.SIFT_DESCR_MAG_THR = 0.2;
        
        # factor used to convert floating-point descriptor to unsigned char
        # self.SIFT_INT_DESCR_FCTR = 512.0;
        
        # intermediate type used for DoG pyramids
        self.SIFT_FIXPT_SCALE = 1;
        
        self.nfeatures = nfeatures;
        self.nOctaveLayers = nOctaveLayers;
        self.contrastThreshold = contrastThreshold;
        self.edgeThreshold = edgeThreshold;
        self.sigma = sigma;

    '''
    img 为输入的8位灰度图像
    '''
    def operator(self, img_path, DEBUG=False, EXFolder=None):
        firstOctave = -1;  # firstOctave 表示金字塔的组索引是从0开始还是从‐1开始，‐1表示需要对输入图像的长宽扩大一倍
        actualNOctaves = 0;  # 实际的金字塔的组数
        actualNLayers = 0;  # 实际的金字塔的层数
        
        base = self.createInitialImage(img_path, firstOctave < 0, self.sigma);
        nOctaves = int(round(np.log(np.min(base.size)) / np.log(2.0) - 2) - firstOctave);
        
        gpyr = BuildPyramid.build_gaussian_pyramid(base, self.sigma, nOctaves, self.nOctaveLayers);
        dogpyr = BuildPyramid.build_DoG_pyramid(gpyr, nOctaves, self.nOctaveLayers);
        
        if DEBUG is True:
            # 导出高斯金字塔
            os.mkdir(export_folder + "gaussian_pyramid");
            Others.export_pyramid(export_folder + "gaussian_pyramid/gaussian_pyramid.txt", gpyr, self.nOctaveLayers + 3);
            Others.plot_pyramid(export_folder + "gaussian_pyramid/gaussian_pyramid.txt", export_folder + "/gaussian_pyramid/");
#             # 导出高斯差分金字塔
#             Others.export_pyramid(export_folder + "/dog_pyramid/dog_pyramid.txt", dogpyr, self.nOctaveLayers + 2);
#             Others.plot_pyramid(export_folder + "/dog_pyramid/dog_pyramid.txt", export_folder + "/dog_pyramid/");
         
        # 在DoG尺度空间内找到极值点
        FindLocalExtrema.findScaleSpaceExtrema(gpyr, dogpyr, nOctaves, self.nOctaveLayers,
                                               self.contrastThreshold, self.edgeThreshold,
                                               self.sigma, self.SIFT_FIXPT_SCALE, self.SIFT_IMG_BORDER,
                                               self.SIFT_MAX_INTERP_STEPS, self.SIFT_ORI_HIST_BINS,
                                               self.SIFT_ORI_SIG_FCTR, self.SIFT_ORI_RADIUS);
         
    def createInitialImage(self, img_path, doubleImageSize, sigma):
        print "Initing Image......"
        image = Image.open(img_path).convert("L");
        if(doubleImageSize):
            sig_diff = np.sqrt(np.max(sigma * sigma - self.SIFT_INIT_SIGMA * self.SIFT_INIT_SIGMA * 4, 0.01));
            image = image.resize((2 * image.size[0], 2 * image.size[1]));
            image_blur = image.filter(GaussianBlur(sig_diff));
            return image_blur;
        else:
            sig_diff = np.sqrt(np.max(sigma * sigma - self.SIFT_INIT_SIGMA * self.SIFT_INIT_SIGMA, 0.01));
            image_blur = image.filter(GaussianBlur(sig_diff));
            return image_blur;
        
image = "Z:/SIFT/jobs.jpg";
debug = False;
export_folder = "z:/SIFT/";

sift = SIFT();
sift.operator(image, debug, export_folder);
 
print "SIFT Complete!";
