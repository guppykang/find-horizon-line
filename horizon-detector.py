import time 
import os
from skimage import filters, feature
from skimage.morphology import erosion, square
from skimage.io import imread
from skimage.transform import probabilistic_hough_line
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import convolve
#record the amount of time that it took to run this script
directory = 'candidate_package/input/'
out_dir = 'results/'
if not os.path.exists('results/'):
    os.mkdir('results')

# filename = 'frame0030.jpg'
for filename in sorted(os.listdir(directory)):
    start = time.time()
    plt.figure()
    plt.title(filename)
    current_frame = imread(directory + filename, as_gray=True)
    original_output_image = plt.imshow(current_frame)

    erosion_frame = erosion(current_frame, square(6))
    canny_edges = feature.canny(erosion_frame, sigma=2)

    lines = probabilistic_hough_line(canny_edges, threshold=10, line_length=1300, line_gap=400)

    count = 0
    distances = []
    for line in lines: 
        p1, p2 = line
        distances.append((np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2), int(count)))
        count += 1

    if len(distances) != 0:
        distances.sort(key=lambda x: x[0])

        best_line = distances[-1]

        p1, p2 = lines[best_line[1]]
        slope = (p1[1] - p2[1])/(p1[0] - p2[0])
        
        x_vals = []
        y_vals = []
        for i in range(current_frame.shape[1]):
            x_vals.append(i)

        for x in x_vals: 
            y_vals.append(slope * x + p1[1])

        plt.plot(x_vals, y_vals, '--')
        plt.savefig(out_dir + filename)
        print('saving img : ' + str(filename))

    else : 
        print('no horizon found for : ' + filename)

    stop = time.time()
    print('time spent : ' + str(stop-start))
    # plt.show()
    plt.close()








