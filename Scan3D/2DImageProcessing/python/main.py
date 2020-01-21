################## IMPORT ##################
import cv2
import imutils
import numpy as np
import math
from matplotlib import pyplot as plt
import argparse
from sklearn.cluster import MeanShift, estimate_bandwidth
import time

################## FUNCTION ##################

ref_colors = [
    np.asarray([48, 202, 215], np.float32), #yellow
    np.asarray([50, 49, 152], np.float32), #red
    np.asarray([68, 124, 35], np.float32), #green
    np.asarray([109, 39, 39], np.float32), #blue
]

def normalized(vec):
    n = np.linalg.norm(vec)
    if n == 0:
        return vec
    else:
        return vec / n

def criteria(a, b):
    a = a / 255
    b = b / 255
    l = 0.4
    dist = np.linalg.norm(a - b)
    dist = dist * dist
    prod = np.dot(normalized(a), normalized(b))
    return l * dist - (1 - l) * prod

def find_color(pixel):
    best = 0
    best_dist = 100000;
    i = 0
    for ref in ref_colors:
        dist = criteria(pixel, ref)
        if dist < best_dist:
            best_dist = dist
            best = i
        i = i + 1
    return best

def normalize(img):
    max = np.amax(img);
    if max != 0:
        img = img/max;
    return img;

def L2_norm(vec1, vec2):
    return math.sqrt((float(vec2[0]) - float(vec1[0]))**2 + (float(vec2[1]) - float(vec1[1]))**2 + (float(vec2[2]) - float(vec1[2]))**2);

def channel_difference(vec):
    return math.sqrt( (float(vec[0]) - float(vec[1]))**2 + (float(vec[0]) - float(vec[2]))**2 + (float(vec[1]) - float(vec[2]))**2);

def gradient(img, threshold):   
    grad = np.zeros((len(img), len(img[0])), np.float64);
    
    for i in range(len(img) -1):
        for j in range(len(img[0]) -1):
            grad[i,j] = L2_norm(img[i,j],img[i+1,j]) + L2_norm(img[i,j],img[i,j+1]);
    grad = normalize(grad);
    
    np.where(grad < threshold, 0, grad)

    return grad;

def apply_threshold(img, threshold):
    newImg = np.zeros((len(img), len(img[0])), np.float64);
    for i in range(len(img)):
        for j in range(len(img[0])):
            if img[i,j] < threshold:
                newImg[i,j] = 0;
            else:
                newImg[i,j] = img[i,j]
    return newImg;

def apply_threshold_binary(img, threshold):
    newImg = np.zeros((len(img), len(img[0])), np.uint8);
    for i in range(len(img)):
        for j in range(len(img[0])):
            if img[i,j] <= threshold:
                newImg[i,j] = 0;
            else:
                newImg[i,j] = 255;
    return newImg;

def detect_gray_edge(grad, img):
    grey_map = np.zeros((len(img), len(img[0])), np.uint8);
    for i in range(len(grad)-1):
        for j in range(len(grad[0])-1):
            if grad[i,j] > 0:
             if L2_norm(img[i,j], (30,30,30)) < 100 and channel_difference(img[i,j]) < 30: 
                grey_map[i,j] = 255;
    return grey_map

def detect_links(centroids, grad, grey_map, img):
    links = []
    samples = 100
    for i in range(len(centroids)):
        for j in range(i,len(centroids)):
            if i != j:
                x_step = (centroids[j][0] - centroids[i][0])/samples
                y_step = (centroids[j][1] - centroids[i][1])/samples
                link = True
                x = centroids[i][0]
                y = centroids[i][1]
                
                count = 0
                class_compt = 0
                previous_class = False
                sum_color = np.zeros([1, 3])
                color_samples = 0
                while link and count < samples :
                    
                    pixel = img[int(y), int(x)]
                    if(grey_map[int(y), int(x)] < 0.5 ):
                        sum_color = sum_color + pixel
                        color_samples = color_samples + 1
                    
                    # I think this is probably a bit too harsh. Maybe stop if it happens multiple times instead of only once. 
                    # If really think this criteria is too sensible to the camera we use to take the pixtures and the resolution at which we make the processing
                    if grad[int(y), int(x)] == 0.0:
                        link = False
                    
                    if not previous_class:
                        if grey_map[int(y), int(x)] > 0.0:
                            previous_class = True
                            class_compt +=1 
                    else:
                        if grey_map[int(y), int(x)] == 0.0:
                            previous_class = False
                        
                        
                    count += 1
                    x = x + x_step
                    y = y + y_step
                
                if link and class_compt < 3:
                    estimated_color = sum_color[0] / color_samples
                    index_color = find_color(estimated_color)
                    links.append([i,j, index_color])
                
    return links

def substract_binary_maps(bin1, bin2):
    sub_map = np.zeros((len(bin1), len(bin1[0])), np.uint8);
    for i in range(len(bin1)):
        for j in range(len(bin1[0])):
            if int(bin1[i,j]) - int(bin2[i,j]) >= 0: 
                sub_map[i,j] = bin1[i,j] - bin2[i,j];
            else:
                sub_map[i,j] = bin1[i,j]
    return sub_map

def add_binary_maps(bin1, bin2):
    sub_map = np.zeros((len(bin1), len(bin1[0])), np.uint8);
    for i in range(len(bin1)):
        for j in range(len(bin1[0])):
            if int(bin1[i,j]) + int(bin2[i,j]) <= 255: 
                sub_map[i,j] = bin1[i,j] + bin2[i,j];
            else:
                sub_map[i,j] = bin1[i,j]
    return sub_map
 

################## MAIN ##################
if __name__ == "__main__":
    start_time = time.time()

    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required=True, help="path to the input image")
    args = vars(ap.parse_args())

    img_name = args["image"]
    img = cv2.imread(img_name)
    old_size = float(img.shape[0])
    img = imutils.resize(img, width=512)
    
    """ GET THE SHAPE"""
    print("Processing gradient...")
    grad_img = gradient(img,0.0);
    grad_time = time.time()
    print("Processed in", grad_time - start_time ,"seconds")
    
    """ REDUCE NOISE TO EXCLUDE THE BAKCGROUND"""
    print("Processing blur...")
    blur = cv2.blur(grad_img,(21,21));
    blur = normalize(blur);
    blur_thresholded_high = apply_threshold(blur,0.3);
    blur_thresholded_low = apply_threshold_binary(blur,0.1);
    blur_time = time.time()
    print("Processed in", blur_time - grad_time ,"seconds")
    
    """ KEEP THE EGDGE ASSOCIATED TO GREY PIXELS"""
    print("Processing edges...")
    grey_map = detect_gray_edge(blur_thresholded_high, img)
    grey_map = cv2.blur(grey_map,(51,51));
    grey_map = normalize(grey_map)
    grey_map_thresholded = apply_threshold_binary(grey_map,0.4)
    edge_time = time.time()
    print("Processed in", edge_time - blur_time ,"seconds")
    
    """ TRANSFORM EVERY CLUSTER OF GREY PIXEL INTO N CENTROIDS """
    print("Processing centroids...")
    ret, thresh = cv2.threshold(grey_map_thresholded,0,255,0)
    connectivity = 8
    num_cc, labels, stats, centroids = cv2.connectedComponentsWithStats(thresh, connectivity)
    centroids = np.delete(centroids,0,0);
    centroid_time = time.time()
    print("Processed in", centroid_time - edge_time ,"seconds")
    
    """ FIND LINKS """
    print("Processing links...")
    grey_map_low = detect_gray_edge(blur_thresholded_low, img)
    grey_map_low = apply_threshold_binary(grey_map_low,0.0)
    sub_map = substract_binary_maps(blur_thresholded_low, grey_map_low)
    add_map = add_binary_maps(sub_map, grey_map_thresholded)
    #cv2.imshow('gmt', grey_map_thresholded)
    links = detect_links(centroids, add_map, grey_map_thresholded, img)
    link_time = time.time()
    print("Processed in", link_time - centroid_time ,"seconds")
    
    print("Drawing...")
    """ DRAW THE CENTROIDS """
    for coord in centroids:
        cv2.circle(img, (int(coord[0]),int(coord[1])), 30, (0,255,0))
    
    """ DRAW LINKS """
    for link in links:
        p1 = (int(centroids[link[0]][0]) , int(centroids[link[0]][1]))
        p2 = (int(centroids[link[1]][0]), int(centroids[link[1]][1]))
        color_index = link[2]
        color = ref_colors[color_index]
        color = (int(color[0]), int(color[1]), int(color[2]))
        cv2.line(img, p1, p2, color, thickness=3, lineType=8)
    draw_time = time.time()
    print("Drawn in", draw_time - link_time ,"seconds")
    
    """ DISPLAY THE IMAGE """
    print("Displaying...")
    cv2.imshow("Resultat", img);
    #cv2.imshow("temp_resultat", add_map);
    cv2.waitKey(0);
    cv2.destroyAllWindows();
    
    print("Saving...")
    cv2.imwrite("results/" + img_name, img);
