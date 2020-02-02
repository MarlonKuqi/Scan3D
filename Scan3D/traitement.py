#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
#from PySide2 import QtCore, QtGui, QtWidgets
from PyQt5 import QtWidgets, QtCore, QtGui 
import interface  # import du fichier interface.py généré par pyuic5

class MyWindow(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.ui = interface.Ui_MainWindow()
        self.ui.setupUi(self)
        
       
        # Action sur les boutons de l'interface
        self.ui.CapturePhoto.clicked.connect(self.action_bouton)
        self.ui.CancelButton.clicked.connect(self.closeInterface)
        self.ui.PlayPhotoButton.clicked.connect(self.action_bouton)
        self.ui.launchTreatment.clicked.connect(self.action_bouton)
 		
       

        img = QtGui.QPixmap('./test1.jpg')
        self.ui.label.setPixmap(img.scaled(self.ui.label.size(), QtCore.Qt.IgnoreAspectRatio))
        self.ui.label.resize(self.width(), 300)
        self.ui.label.show()
        # for i in range(20):
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




    def action_bouton(self):
        print('Appui bouton A definir pour chaque bouton.')


    def closeInterface(self): 
    	self.close()

    # def on_item_changed(self):
    #     print(self.ui.listWidget.currentItem().text())

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())