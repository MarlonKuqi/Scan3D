import cv2
import imutils
import numpy as np
import math
from sklearn.cluster import MeanShift, estimate_bandwidth

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
    
    for i in range(len(grad) -1):
        for j in range(len(grad[0]) -1):
            if grad[i,j] < threshold:
                grad[i,j] = 0;
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
            if img[i,j] < threshold:
                newImg[i,j] = 0;
            else:
                newImg[i,j] = 255;
    return newImg;
            
img = cv2.imread("images/image4.jpeg",1);
img = imutils.resize(img, width=512);

grad_img = gradient(img,0.0);

blur = cv2.blur(grad_img,(21,21));
blur = normalize(blur);

blur_thresholded = apply_threshold(blur,0.3);

grey_map = np.zeros((len(img), len(img[0])), np.uint8);
grey = []
for i in range(len(blur_thresholded)-1):
    for j in range(len(blur_thresholded[0])-1):
        if blur_thresholded[i,j] > 0:
         if L2_norm(img[i,j], (30,30,30)) < 100 and channel_difference(img[i,j]) < 30: 
            grey.append([i,j]);
            grey_map[i,j] = 255;

grey_map = cv2.blur(grey_map,(51,51));
grey_map = normalize(grey_map);

grey_map_thresholded = apply_threshold_binary(grey_map,0.4)

ret, thresh = cv2.threshold(grey_map_thresholded,0,255,0)

connectivity = 8

num_cc, labels, stats, centroids = cv2.connectedComponentsWithStats(thresh, connectivity)

centroids = np.delete(centroids,0,0);

for coord in centroids:
    cv2.circle(img, (int(coord[0]),int(coord[1])), 40, (255,255,0))

cv2.imshow("Originale", img);
cv2.imshow("Resultat", grey_map_thresholded);
cv2.waitKey(0);
cv2.destroyAllWindows();
