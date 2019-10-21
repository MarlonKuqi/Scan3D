#include "mainwindow.h"
#include <QApplication>

#include <iostream>

#include <QAction>
#include <QDebug>
#include <QDir>
#include <QFileDialog>
#include <QMessageBox>
#include <QPushButton>
#include <QString>


#include "stdlib.h"


int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    MainWindow w;

    w.show();


    return a.exec();
}
