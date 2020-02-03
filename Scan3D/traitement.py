#!/usr/bin/python3
# -*- coding: utf-8 -*-

#from PySide2 import QtCore, QtGui, QtWidgets
from PyQt5 import QtWidgets, QtCore, QtGui 
import interface  # import du fichier interface.py généré par pyuic5
import cv2
import sys
import imutils
import numpy as np
import math
from matplotlib import pyplot as plt
import argparse
from sklearn.cluster import MeanShift, estimate_bandwidth
import time
import ImageProcessing as imp
import Treat_Image as timg

class MyWindow(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.ui = interface.Ui_MainWindow()
        self.ui.setupUi(self)
        
       
        # Action sur les boutons de l'interface
        self.ui.CapturePhoto.clicked.connect(self.TakePhoto2)
        self.ui.CancelButton.clicked.connect(self.closeInterface)
        self.ui.PlayPhotoButton.clicked.connect(self.TreatementImageBoucle)
        self.ui.launchTreatment.clicked.connect(self.TreatementImage2)
 		
       

        # img = QtGui.QPixmap('./test1.jpg')
        # img = QtGui.QPixmap('./data/hexa.JPG')
        # img = QtGui.QPixmap('./data/image1.jpeg')
        # self.ui.label.setPixmap(img.scaled(self.ui.label.size(), QtCore.Qt.IgnoreAspectRatio))
        # self.ui.label.resize(self.width(), 300)
        # self.ui.label.show()
        # # for i in range(20):
        #     self.ui.listWidget.addItem(str(i))
    

        # Todo : Appliquer les traitement sur img  :  A voir

        # self.ui.labelLoadedImage.showMessage("Input Image")
        # self.ui.labelResutImage.showMessage("Output Image")

        # lb = QtGui.QLabel(self)
        # pixmap = QtWidgets.QPixmap("./test.jpg")
        # height_label = 100
        # labelLoadedImage.resize(self.width(), height_label)
        # labelLoadedImage.setPixmap(pixmap.scaled(lb.size(), QtCore.Qt.IgnoreAspectRatio))
        # self.show() 


    def closeInterface(self): 
    	self.close()

    def TakePhoto(self, img_name):
        #img_name = "image1.jpeg"
        img = QtGui.QPixmap('./data/'+ img_name)
        self.ui.label.setPixmap(img.scaled(self.ui.label.size(), QtCore.Qt.IgnoreAspectRatio))
        self.ui.label.resize(self.width(), 300)
        self.ui.label.show()
        # timg.TreatImage(img_name)

    def TakePhoto2(self):
        img_name = "image1.jpeg"
        self.TakePhoto(img_name)
    
    def TreatementImage(self, img_name):
        # img_name = "image1.jpeg"
        timg.TreatImage(img_name)
        img_res = QtGui.QPixmap("results/"+ img_name)  
        self.ui.labelResult.setPixmap(img_res.scaled(self.ui.labelResult.size(), QtCore.Qt.IgnoreAspectRatio))
        self.ui.labelResult.resize(self.width(), 300)
        self.ui.labelResult.show()

    def TreatementImage2(self):
        img_name = "image1.jpeg"
        self.TreatementImage(img_name)


    def TreatementImageBoucle(self):
        img_names = ["hexa.JPG", "image1.jpeg"]
        for i in img_names:   
            self.TakePhoto(i)
            self.TreatementImage(i)
            time.sleep(1)

        # self.TakePhoto(img_names[1])
        # time.sleep(2)
        # self.TreatementImage(img_names[1])
        # time.sleep(5)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())