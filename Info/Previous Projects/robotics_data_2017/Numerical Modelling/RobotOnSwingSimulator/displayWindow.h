/*
 * displayWindow.h
 *
 *  Created on: 01/03/2017
 *      Author: Joshua Torbett
 */

#ifndef DISPLAYWINDOW_H
#define DISPLAYWINDOW_H

#include <QWidget>
#include <QPainter>
#include <QTimer>
#include <fstream>
#include <iostream>
#include <string>
#include "twoVector.h"

namespace Ui {
class displayWindow;
}

class displayWindow : public QWidget
{
    Q_OBJECT

public:

    //constructor
    explicit displayWindow(int type, QWidget *parent = 0);

    //de-constructor
    ~displayWindow();

    //setting file for simulation
    void SetFile(std::string name, std::string location);



public slots:

    //reads file for simulation
    void readFile(std::string location);


private slots:

    //paint event to draw system
    void paintEvent(QPaintEvent *);


private:

    Ui::displayWindow *ui;

    int fScale; // scaling factor for positions

    int ft; // psuedo timer

    std::vector<std::vector<twoVector>> fObjects; //list of objects

    std::vector<double> fTime; //holds times

    QTimer *fTimer = new QTimer(this); //timer for system

    //simulation type
    int fType;
    enum{
        kSimple,
        kDumbbell,
        kFlail,
        kRobot
    };

};

#endif // DISPLAYWINDOW_H
