import time 
import argparse
import os
from skimage import filters, feature
from skimage.morphology import erosion, square
from skimage.io import imread
from skimage.transform import probabilistic_hough_line
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import convolve

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", help="path to input dir (include '/' at the end)", default='candidate_package/input/')
parser.add_argument("-o", "--output", help="path output to dir (include '/' at the end)", default='results/')

args = parser.parse_args()


directory = args.input
out_dir = 'results/'
if not os.path.exists(args.output):
    os.mkdir(args.output)

# filename = 'frame0030.jpg'
for filename in sorted(os.listdir(directory)):
    start = time.time()

    plt.figure()
    plt.title(filename)

    current_frame = imread(directory + filename, as_gray=True)
    original_output_image = plt.imshow(current_frame)

    #erosion for cleaning up noise
    erosion_frame = erosion(current_frame, square(6))

    #get edges from canny. Could use sobel 
    canny_edges = feature.canny(erosion_frame, sigma=2)

    #use hough to get the best lines 
    lines = probabilistic_hough_line(canny_edges, threshold=10, line_length=1300, line_gap=400)

    #get the longest line (probably change this to a better way to get the best line)
    count = 0
    distances = []
    for line in lines: 
        p1, p2 = line
        distances.append((np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2), int(count)))
        count += 1

    if len(distances) != 0:
        distances.sort(key=lambda x: x[0])

        #longest line 
        best_line = distances[-1]

        #get slope
        p1, p2 = lines[best_line[1]]
        slope = (p1[1] - p2[1])/(p1[0] - p2[0])
        
        x_vals = []
        y_vals = []
        for i in range(current_frame.shape[1]):
            x_vals.append(i)

        #get y values for the x values through slope intercept form
        for x in x_vals: 
            y_vals.append(slope * x + p1[1])

        plt.plot(x_vals, y_vals, '--')
        plt.savefig(out_dir + filename)
        print('saving img : ' + str(filename))

    else : 
        print('no horizon found for : ' + filename)

    stop = time.time()

    #calculate the runtime
    print('time spent : ' + str(stop-start))
    # plt.show()
    plt.close()








