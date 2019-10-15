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
    blur = cv2.GaussianBlur(img,(5,5),0)
    
    edges = cv2.Canny(blur,1,20)
    
    
    (thresh, blackAndWhiteImage) = cv2.threshold(edges, 0, 255, cv2.THRESH_BINARY)
    
    kernel = np.ones((5,5), np.uint8) 
    
    closed_img = cv2.morphologyEx(blackAndWhiteImage, cv2.MORPH_CLOSE, kernel, iterations=5)
    #img_dilation = cv2.dilate(blackAndWhiteImage, kernel, iterations=25) 
    #img_erode = cv2.erode(img_dilation, kernel, iterations=25)
    
    return cv2.cvtColor(closed_img,cv2.COLOR_GRAY2RGB)



######### MAIN ############

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to the input image")
args = vars(ap.parse_args())


img = cv2.imread(args["image"])
img = imutils.resize(img, width=512)
obj = cv2.imread("data/boule.png", 1)

cv2.imshow("image", img)

#body = computeBodyBinary(img)
centers = computePositionObject(img, obj)

for i in range(0, len(centers)):
    cv2.circle(img,(int(centers[i][0]),int(centers[i][1])), 5, (255,0,0), -1)
  

#cv2.imshow("body", body)
cv2.imshow("image", img)
cv2.waitKey(0)






