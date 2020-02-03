import cv2
import sys
#from PySide2 import QtCore, QtGui, QtWidgets
from PyQt5 import QtWidgets, QtCore, QtGui 
import imutils
import numpy as np
import math
from matplotlib import pyplot as plt
import argparse
from sklearn.cluster import MeanShift, estimate_bandwidth
import time
import ImageProcessing as imp

def TreatImage(img_name):
    start_time = time.time()

    # img_name = QtGui.QPixmap('./data/hexa.JPG')
    # self.ui.label.setPixmap(img_name.scaled(self.ui.label.size(), QtCore.Qt.IgnoreAspectRatio))
    # self.ui.label.resize(self.width(), 300)

    # img_name = "hexa.JPG"
    # img_name = "image1.jpeg" 
    img_path = r'./data/'+img_name
  
    # Using cv2.imread() method 
    img = cv2.imread(img_path) 

    # img = cv2.imread(img_name)
    old_size = float(img.shape[0])
    img = imutils.resize(img, width=512)
        
    """ GET THE SHAPE"""
    print("Processing gradient...")
    grad_img = imp.gradient(img,0.0);
    grad_time = time.time()
    print("Processed in", grad_time - start_time ,"seconds")
        
    """ REDUCE NOISE TO EXCLUDE THE BAKCGROUND"""
    print("Processing blur...")
    blur = cv2.blur(grad_img,(21,21));
    blur = imp.normalize(blur);
    blur_thresholded_high = imp.apply_threshold(blur,0.3);
    blur_thresholded_low = imp.apply_threshold_binary(blur,0.1);
    blur_time = time.time()
    print("Processed in", blur_time - grad_time ,"seconds")
        
    """ KEEP THE EGDGE ASSOCIATED TO GREY PIXELS"""
    print("Processing edges...")
    grey_map = imp.detect_gray_edge(blur_thresholded_high, img)
    grey_map = cv2.blur(grey_map,(51,51));
    grey_map = imp.normalize(grey_map)
    grey_map_thresholded = imp.apply_threshold_binary(grey_map,0.4)
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
    grey_map_low = imp.detect_gray_edge(blur_thresholded_low, img)
    grey_map_low = imp.apply_threshold_binary(grey_map_low,0.0)
    sub_map = imp.substract_binary_maps(blur_thresholded_low, grey_map_low)
    add_map = imp.add_binary_maps(sub_map, grey_map_thresholded)
    #cv2.imshow('gmt', grey_map_thresholded)
    links = imp.detect_links(centroids, add_map, grey_map_thresholded, img)
    link_time = time.time()
    print("Processed in", link_time - centroid_time ,"seconds")
    
    canvas = img * 0
    
    imp.draw_graph(canvas, centroids, links)
    
    graph_str = imp.graph_to_str(centroids, links)
    with open('graph.txt', 'w') as file:
        file.write(graph_str)
    
    print("Saving...")
    cv2.imwrite("results/" + img_name, img);
    
    # img_res = QtGui.QPixmap("results/"+ img_name)  
    # self.ui.labelResult.setPixmap(img_res.scaled(self.ui.labelResult.size(), QtCore.Qt.IgnoreAspectRatio))
    # self.ui.labelResult.resize(self.width(), 300)
    # self.ui.labelResult.show()

    # """ DISPLAY THE IMAGE """
    # cv2.imshow("Resultat", img)
    # cv2.imshow("canvas", canvas)

    # #cv2.imshow("temp_resultat", add_map);
    # cv2.waitKey(0);
    # cv2.destroyAllWindows();
