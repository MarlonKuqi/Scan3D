#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>

namespace Ui {
class MainWindow;
}

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = 0);
    ~MainWindow();
<<<<<<< HEAD

private slots:
    void on_MainWindow_toolButtonStyleChanged(const Qt::ToolButtonStyle &toolButtonStyle);

=======
public slots:
    void ouvrirDialogue();
>>>>>>> 62948996c5c50f0ed6663895e094049530ff1245
private:
    Ui::MainWindow *ui;

};

#endif // MAINWINDOW_H
