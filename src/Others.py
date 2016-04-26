# coding: UTF-8
import numpy as np
import matplotlib.pyplot as plt

def export_pyramid(filepath, pyramid):
    print "exporting \"" + filepath + "\" ......";
    fileHandler = open(filepath, "w");
    for o in range(len(pyramid)):
        m, n = np.shape(pyramid[o][0]);
        fileHandler.write("octave:" + str(o) + "|shape:" + str(m) + "," + str(n) + "\n");
        for s in range(len(pyramid[o])):
            fileHandler.write(image_to_string(pyramid[o][s]) + "\n");
    fileHandler.close();

def image_to_string(image):
    array = np.array(image);
    m, n = np.shape(array);
    s = "";
    for i in range(m):
        for j in range(n):
            s += str(array[i, j]) + ",";
    return s[:-1];

def plot_pyramid(modelfile, plotfolder):
    print "ploting pyramid ......";
    file = open(modelfile);
    pyramid = [];
    index = -1;
    m = 0;
    n = 0;
    octave = [];
    for line in file.readlines():
        if line[:6] == "octave":
            if index > -1:
                pyramid.append(octave);
            octave = [];
            
            lineArr = line.strip().split('|');
            for arr in lineArr:
                key, val = arr.split(':');
                if key == "octave":
                    index = int(val);
                elif key == "shape":
                    val = val.split(",");
                    m = int(val[0]);
                    n = int(val[1]);
        else:
            data = line.split(',');
            for i in range(len(data)):
                data[i] = float(data[i]);
            data = np.reshape(data, (m, n));
            octave.append(data);
    file.close();
    
    for o in range(len(pyramid)):
        for s in range(len(pyramid[o])):
            fig = plt.figure();
            ax = fig.add_subplot(111);
            ax.imshow(pyramid[o][s], cmap="gray");
            plt.savefig(plotfolder + str(o) + "_" + str(s) + ".png")

