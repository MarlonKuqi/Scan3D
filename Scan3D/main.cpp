#include "mainwindow.h"
<<<<<<< HEAD
#include <QApplication>
#include <QFileDialog>
#include <QFile>
#include <QMessageBox>
#include <QTextStream>
=======
#include "qapplication.h"
#include "stdlib.h"
#include <iostream>
>>>>>>> 62948996c5c50f0ed6663895e094049530ff1245

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);

    MainWindow w;
<<<<<<< HEAD

    w.show();
=======
    w.showMaximized();
>>>>>>> 62948996c5c50f0ed6663895e094049530ff1245

    return a.exec();
}
