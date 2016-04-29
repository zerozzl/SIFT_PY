# coding: UTF-8
import Others
import numpy as np
import matplotlib.pyplot as plt

pyramid = Others.load_pyramid("Z:/SIFT/dog_pyramid/dog_pyramid.txt");

target = pyramid[1];

layer = 1;
m, n = np.shape(target[layer]);
keypoint = [];
for i in range(1, m - 1):
    for j in range(1, n - 1):
        cur = target[layer][i, j];
        if (cur >= target[layer-1][i - 1, j - 1] and cur >= target[layer-1][i - 1, j]
            and cur >= target[layer-1][i - 1, j + 1] and cur >= target[layer-1][i, j - 1]
            and cur >= target[layer-1][i, j] and cur >= target[layer-1][i, j + 1]
            and cur >= target[layer-1][i + 1, j - 1] and cur >= target[layer-1][i + 1, j]
            and cur >= target[layer-1][i + 1, j + 1] and cur >= target[layer][i - 1, j - 1]
            and cur >= target[layer][i - 1, j] and cur >= target[layer][i - 1, j + 1]
            and cur >= target[layer][i, j - 1] and cur >= target[layer][i, j + 1]
            and cur >= target[layer][i + 1, j - 1] and cur >= target[layer][i + 1, j]
            and cur >= target[layer][i + 1, j + 1] and cur >= target[layer+1][i - 1, j - 1]
            and cur >= target[layer+1][i - 1, j] and cur >= target[layer+1][i - 1, j + 1]
            and cur >= target[layer+1][i, j - 1] and cur >= target[layer+1][i, j]
            and cur >= target[layer+1][i, j + 1] and cur >= target[layer+1][i + 1, j - 1]
            and cur >= target[layer+1][i + 1, j] and cur >= target[layer+1][i + 1, j + 1]):
            keypoint.append([i, j, 1]);
        elif (cur <= target[layer-1][i - 1, j - 1] and cur <= target[layer-1][i - 1, j]
            and cur <= target[layer-1][i - 1, j + 1] and cur <= target[layer-1][i, j - 1]
            and cur <= target[layer-1][i, j] and cur <= target[layer-1][i, j + 1]
            and cur <= target[layer-1][i + 1, j - 1] and cur <= target[layer-1][i + 1, j]
            and cur <= target[layer-1][i + 1, j + 1] and cur <= target[layer][i - 1, j - 1]
            and cur <= target[layer][i - 1, j] and cur <= target[layer][i - 1, j + 1]
            and cur <= target[layer][i, j - 1] and cur <= target[layer][i, j + 1]
            and cur <= target[layer][i + 1, j - 1] and cur <= target[layer][i + 1, j]
            and cur <= target[layer][i + 1, j + 1] and cur <= target[layer+1][i - 1, j - 1]
            and cur <= target[layer+1][i - 1, j] and cur <= target[layer+1][i - 1, j + 1]
            and cur <= target[layer+1][i, j - 1] and cur <= target[layer+1][i, j]
            and cur <= target[layer+1][i, j + 1] and cur <= target[layer+1][i + 1, j - 1]
            and cur <= target[layer+1][i + 1, j] and cur <= target[layer+1][i + 1, j + 1]):
            keypoint.append([i, j, -1]);

print 'keypoints: ', str(int(len(keypoint)));

img = np.zeros((m, n));
for point in keypoint:
    img[point[0], point[1]] = 1;

fig = plt.figure();
ax = fig.add_subplot(111);
ax.imshow(img, cmap="gray");
plt.show();

print 'success'
