######## Import #############
import cv2
from scipy import misc
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import argparse
import imutils


######## Function ##########
def computePositionObject(img, obj):
    nb_ball_max = 25;
    
    # ORB Detector
    orb = cv2.ORB_create(nfeatures=1000, scoreType=cv2.ORB_FAST_SCORE)
    kp1, des1 = orb.detectAndCompute(obj, None)
    kp2, des2 = orb.detectAndCompute(img, None)
    
    # Brute Force Matching
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(des1, des2)
    matches = sorted(matches, key = lambda x:x.distance)
    
    matches_pts = []
    for i in range(0,len(matches)):
        matches_pts.append(kp2[matches[i].trainIdx].pt);
    
    
    matches_pts = np.array(matches_pts)
    
    optimal_k = 0
    score = 0
    for n_cluster in range(2, nb_ball_max):
        kmeans = KMeans(n_clusters=n_cluster).fit(matches_pts)
        label = kmeans.labels_
        sil_coeff = silhouette_score(matches_pts, label, metric='euclidean')
        if score < sil_coeff:
            optimal_k = n_cluster
            score = sil_coeff
    
    kmeans = KMeans(n_clusters=optimal_k, random_state=0).fit(matches_pts)
    centers = np.array(kmeans.cluster_centers_)
    
    return centers


def computeBodyBinary(img):
    blur = cv2.GaussianBlur(img,(21,21),0)
    
    edges = cv2.Canny(blur,1,20)
    
    
    (thresh, blackAndWhiteImage) = cv2.threshold(edges, 0, 255, cv2.THRESH_BINARY)
    
    kernel = np.ones((5,5), np.uint8) 
    
    closed_img = cv2.morphologyEx(blackAndWhiteImage, cv2.MORPH_CLOSE, kernel, iterations=20)
    #img_dilation = cv2.dilate(blackAndWhiteImage, kernel, iterations=25) 
    #img_erode = cv2.erode(img_dilation, kernel, iterations=25)
    
    return cv2.cvtColor(closed_img,cv2.COLOR_GRAY2RGB)


def computeLinks(centers, body, img): 
    steps = 100
    for i in range(0, len(centers)):
        for j in range(0, len(centers)):
            if i != j :
                xDiff = centers[j][0] - centers[i][0];
                yDiff = centers[j][1] - centers[i][1];
                
                xStep = xDiff/steps;
                yStep = yDiff/steps;
                
                compt = 0;
                transitivity = [];
                
                centerColor = tuple(body[int(centers[i][1]), int(centers[i][0])])
                
                for k in range(1,steps):
                    pixel = [0] * 2;
                    pixel[0] = centers[i][0] + xStep * k; 
                    pixel[1] = centers[i][1] + yStep * k; 
                    
                    if tuple(body[int(pixel[1]), int(pixel[0])]) != (0,0,0):
                        compt = compt + 1;
                    if tuple(body[int(pixel[1]), int(pixel[0])]) != (0,0,0) and tuple(body[int(pixel[1]), int(pixel[0])]) != (255,255,255) and tuple(body[int(pixel[1]), int(pixel[0])]) != centerColor:
                        if(tuple(body[int(pixel[1]), int(pixel[0])]) not in transitivity):
                            transitivity.append(tuple(body[int(pixel[1]), int(pixel[0])]));
                
                
                if compt > 0.7 * steps and len(transitivity) < 2:
                    cv2.line(img, (int(centers[i][0]),int(centers[i][1])) , (int(centers[j][0]),int(centers[j][1])), (0, 255, 0), thickness=3, lineType=8)
                    cv2.circle(img,(int(centers[i][0]),int(centers[i][1])), 20, (0,0,255), -1)



######### MAIN ############

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to the input image")
args = vars(ap.parse_args())


img = cv2.imread(args["image"])
old_size = float(img.shape[0])
img = imutils.resize(img, width=1024)
ratio = float(img.shape[0]) / old_size

obj = cv2.imread("spheres/sphere.png", 1)
obj = imutils.resize(obj, width=int(obj.shape[0] * ratio))

cv2.imshow("image", img)

body = computeBodyBinary(img)

#cv2.imshow('body', body)

centers = computePositionObject(img, obj)

for i in range(0, len(centers)):
    cv2.circle(body,(int(centers[i][0]),int(centers[i][1])), 40, (int(255/(i+1)),0,0), -1)
  
    
computeLinks(centers, body, img);

img = imutils.resize(img, width=512)
#cv2.imshow("body", body)
cv2.imshow("image", img)
cv2.waitKey(0)






