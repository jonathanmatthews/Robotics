#include "controlWindow.h"
#include <QApplication>



int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    //creates an instance of control window
    controlWindow w;
    //displays control window
    w.show();


    return a.exec();
}
