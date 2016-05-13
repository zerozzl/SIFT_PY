# coding: UTF-8
import numpy as np
import matplotlib.pyplot as plt

def export_pyramid(filepath, pyramid, nLayers):
    print "Exporting \"" + filepath + "\" ......";
    fileHandler = open(filepath, "w");
    
    fileHandler.write("nOctaves:" + str(len(pyramid) / nLayers)
                      + "|nLayers:" + str(nLayers) + "\n");
    
    nOctaves = -1;
    for idx in range(len(pyramid)):
        if idx % nLayers == 0:
            nOctaves += 1;
            m, n = np.shape(pyramid[idx]);
            fileHandler.write("octave:" + str(nOctaves) + "|shape:" + str(m) + "," + str(n) + "\n");
        fileHandler.write(image_to_string(pyramid[idx]) + "\n");
    fileHandler.close();

def image_to_string(image):
    array = np.array(image);
    m, n = np.shape(array);
    s = "";
    for i in range(m):
        for j in range(n):
            s += str(array[i, j]) + ",";
    return s[:-1];

def load_pyramid(modelfile):
    print "Loading \"" + modelfile + "\" ......";
    file = open(modelfile);
    pyramid = [];
    nOctaves = 0;
    nLayers = 0;
    m = 0; n = 0;
    for line in file.readlines():
        if line[:8] == "nOctaves":
            lineArr = line.strip().split('|');
            for arr in lineArr:
                key, val = arr.split(':');
                if key == "nOctaves":
                    nOctaves = int(val);
                elif key == "nLayers":
                    nLayers = int(val);
        elif line[:6] == "octave":
            lineArr = line.strip().split('|');
            for arr in lineArr:
                key, val = arr.split(':');
                if key == "shape":
                    val = val.split(",");
                    m = int(val[0]);
                    n = int(val[1]);
        else:
            data = line.split(',');
            for i in range(len(data)):
                data[i] = float(data[i]);
            data = np.reshape(data, (m, n));
            pyramid.append(data);
    file.close();
    
    return nOctaves, nLayers, pyramid;

def plot_pyramid(modelfile, plotfolder):
    print "Ploting pyramid ......";
    nOctaves, nLayers, pyramid = load_pyramid(modelfile);
    idx = 0;
    for o in range(nOctaves):
        for s in range(nLayers):
            fig = plt.figure();
            ax = fig.add_subplot(111);
            ax.imshow(pyramid[idx], cmap="gray");
            plt.savefig(plotfolder + str(o) + "_" + str(s) + ".png");
            idx += 1;
