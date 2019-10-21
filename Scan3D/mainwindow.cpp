#include "mainwindow.h"
#include "ui_mainwindow.h"

#include <iostream>

#include <QAction>
#include <QDebug>
#include <QDir>
#include <QFileDialog>
#include <QMessageBox>
#include <QString>
#include <QToolBar>


#include "stdlib.h"


MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    QObject::connect(ui->openFile, SIGNAL(clicked()), this, SLOT(ouvrirDialogue()));
}

void MainWindow::ouvrirDialogue(){
    QString fichier = QFileDialog::getOpenFileName(this, "Ouvrir un fichier", QDir::homePath()+"/Images", "Images (*.png *.gif *.jpg *.jpeg)");
    QMessageBox::information(this, "Fichier", "Vous avez sélectionné :\n" + fichier);

    qDebug() << fichier;
}


MainWindow::~MainWindow()
{
    delete ui;
}
