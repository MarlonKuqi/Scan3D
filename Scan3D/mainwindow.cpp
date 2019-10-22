#include "mainwindow.h"
#include "ui_mainwindow.h"

#include <iostream>

#include <QAction>
#include <QDebug>
#include <QDesktopWidget>
#include <QDir>
#include <QLabel>
#include <QFileDialog>
#include <QMessageBox>
#include <QString>
#include <QStyle>
#include <QTimer>
#include <QToolBar>

#include <QPixmap>
#include "stdlib.h"


MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    ui->progressBar->hide();
    QObject::connect(ui->openFile, SIGNAL(triggered()), this, SLOT(ouvrirDialogue()));
    QObject::connect(ui->launchTreatment, SIGNAL(clicked()), this, SLOT(displayResultingImage()));
}

void MainWindow::ouvrirDialogue(){
    QString nomImage = QFileDialog::getOpenFileName(this, "Ouvrir un fichier", QDir::homePath()+"/Images", "Images (*.png *.gif *.jpg *.jpeg)");
    QMessageBox::information(this, "Fichier", "Vous avez sélectionné :\n" + nomImage);
    imageLoaded = QPixmap(nomImage);
    ui->label->setPixmap(imageLoaded);
    ui->label->setScaledContents(true);
    ui->label->show();
    qDebug() << nomImage;
}

void MainWindow::displayResultingImage(){
    ui->labelResult->setPixmap(imageLoaded);
    ui->labelResult->setScaledContents(true);
    ui->labelResult->show();
}

MainWindow::~MainWindow()
{
    delete ui;
}
