#include "mainwindow.h"
#include "qapplication.h"
#include "stdlib.h"
#include <iostream>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);

    MainWindow w;
    w.showMaximized();

    return a.exec();
}
