# coding: UTF-8
import Image
import numpy as np
import BuildPyramid
from GaussianBlur import GaussianBlur
import FindLocalExtrema
import Others

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
        self.nfeatures = nfeatures;
        self.nOctaveLayers = nOctaveLayers;
        self.contrastThreshold = contrastThreshold;
        self.edgeThreshold = edgeThreshold;
        self.sigma = sigma;
        
        self.SIFT_INIT_SIGMA = 0.5;  # 即输入图像的尺度
        self.SIFT_FIXPT_SCALE = 1;  # 即输入图像的尺度
        self.SIFT_IMG_BORDER = 5; # 该变量的作用是保留一部分图像的四周边界
        self.SIFT_MAX_INTERP_STEPS = 5; # 表示特征点定位，循环迭代最多5次
        self.SIFT_ORI_HIST_BINS = 36; # 定义梯度方向的数量
        self.SIFT_ORI_SIG_FCTR = 1.5; # 表示特征点方向分配窗口半径系数
        self.SIFT_ORI_RADIUS = 3 * self.SIFT_ORI_SIG_FCTR; # 表示特征点方向分配窗口半径
    
    def operator(self, image_path, export_pyramid=False, export_folder=None):
        print "Begin SIFT......";
        # 读取图像，并扩大输入图像长宽尺寸操作
        base = self.createInitialImage(image_path, self.sigma);
        nOctaves = int(round(np.log(np.min(base.size)) / np.log(2.0) - 2) + 1);
        
        # 构建高斯差分金字塔
        gpyr = BuildPyramid.build_gaussian_pyramid(base, self.sigma, nOctaves, self.nOctaveLayers);
        dogpyr = BuildPyramid.build_DoG_pyramid(gpyr, nOctaves, self.nOctaveLayers);
        
        if export_pyramid == True:
            # 导出高斯金字塔
            Others.export_pyramid(export_folder + "/gaussian_pyramid/gaussian_pyramid.txt", gpyr, self.nOctaveLayers + 3);
            Others.plot_pyramid(export_folder + "/gaussian_pyramid/gaussian_pyramid.txt", export_folder + "/gaussian_pyramid/");
            # 导出高斯差分金字塔
            Others.export_pyramid(export_folder + "/dog_pyramid/dog_pyramid.txt", dogpyr, self.nOctaveLayers + 2);
            Others.plot_pyramid(export_folder + "/dog_pyramid/dog_pyramid.txt", export_folder + "/dog_pyramid/");
        
        # 在DoG尺度空间内找到极值点
        FindLocalExtrema.findScaleSpaceExtrema(gpyr, dogpyr, nOctaves, self.nOctaveLayers,
                                               self.contrastThreshold, self.edgeThreshold,
                                               self.sigma, self.SIFT_FIXPT_SCALE, self.SIFT_IMG_BORDER,
                                               self.SIFT_MAX_INTERP_STEPS, self.SIFT_ORI_HIST_BINS,
                                               self.SIFT_ORI_SIG_FCTR, self.SIFT_ORI_RADIUS);
    
    def createInitialImage(self, image_path, sigma):
        print "Initing Image......"
        image = Image.open(image_path).convert("L");
        image = image.resize((2 * image.size[0], 2 * image.size[1]));
        sig_diff = np.sqrt(np.max(sigma * sigma - self.SIFT_INIT_SIGMA * self.SIFT_INIT_SIGMA * 4, 0.01));
        image_blur = image.filter(GaussianBlur(sig_diff));
        return image_blur;

# image = "Z:/SIFT/lena.jpg";
image = "Z:/SIFT/jobs.jpg";
export_folder = "z:/SIFT/";

sift = SIFT();
sift.operator(image);

print "SIFT Complete!";
