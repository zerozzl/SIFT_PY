# coding: UTF-8
import BuildDoGPyramid

root = "Z:/SIFT/";
filename = "lena.jpg";
sigma = 1.6;
scale = 3;
dog_pyramid = BuildDoGPyramid.build_pyramid(root, filename, sigma, scale);

print "SIFT Complete!";
