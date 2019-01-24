/*
 * controlWindow.h
 *
 *  Created on: 01/03/2017
 *      Author: Joshua Torbett
 */

#ifndef CONTROLWINDOW_H
#define CONTROLWINDOW_H

#include <QMainWindow>
#include "displayWindow.h"
#include <fstream>
#include <iostream>
#include <string>

namespace Ui {
class controlWindow;
}

class controlWindow : public QMainWindow
{
    Q_OBJECT

public:

    //constructor
    explicit controlWindow(QWidget *parent = 0);

    //deconstructor
    ~controlWindow();

private slots:

    //on button click event to trigger simulation
    void on_SimButton_released();


private:

    Ui::controlWindow *ui;
};

#endif // CONTROLWINDOW_H
