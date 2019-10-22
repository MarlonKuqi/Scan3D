#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QPixmap>

namespace Ui {
class MainWindow;
}

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = 0);
    ~MainWindow();
public slots:
    void ouvrirDialogue();
    void displayResultingImage();
private:
    Ui::MainWindow *ui;
    QPixmap imageLoaded;

};

#endif // MAINWINDOW_H
