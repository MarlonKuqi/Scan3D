#include "mainwindow.h"
#include "ui_mainwindow.h"
#include <QApplication>
#include <QFileDialog>
#include <QFile>
#include <QMessageBox>
#include <QTextStream>

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

    QString fichier = QFileDialog::getOpenFileName(this, "Ouvrir un fichier", QString(), "Images (*.png *.gif *.jpg *.jpeg)");
    QMessageBox::information(this, "Fichier", "Vous avez sélectionné :\n" + fichier);

    ui->setupUi(this);
    QObject::connect(ui->openFile, SIGNAL(triggered()), this, SLOT(ouvrirDialogue()));
}

void MainWindow::ouvrirDialogue(){
    QString m_FichierImage = QFileDialog::getOpenFileName(this, "Ouvrir un fichier", QDir::homePath()+"/Images", "Images (*.png *.gif *.jpg *.jpeg)");
    QMessageBox::information(this, "Fichier", "Vous avez sélectionné :\n" + m_FichierImage);
    ui->label->setPixmap(QPixmap(m_FichierImage));
    ui->label->show();
    qDebug() << m_FichierImage;
}

MainWindow::~MainWindow()
{
    delete ui;
}
