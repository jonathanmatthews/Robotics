/*
 * controlWindow.cpp
 *
 *  Created on: 01/03/2017
 *      Author: Joshua Torbett
 */

#include "controlWindow.h"
#include "ui_controlwindow.h"
#include <QMessageBox>
#include <iostream>
#include <fstream>
#include <string>

using namespace std;
//constructor
controlWindow::controlWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::controlWindow)
{
    ui->setupUi(this);


}

//deconstructor
controlWindow::~controlWindow()
{
    delete ui;
}

void controlWindow::on_SimButton_released()
{
    //name of text file
    QString filename = ui->filenameEdit->text();
    std::string name = filename.toLocal8Bit().constData();

    //location of text file
    QString fileLocation = ui->locNameEdit->text();
    std::string location = fileLocation.toLocal8Bit().constData();

    //error checking
    bool fileFound = true;
    //if file or location field is empty
    if (filename.isEmpty() || fileLocation.isEmpty()){
        //file cannot be found
        fileFound = false;
        // user informed
        QMessageBox msgBox;
        msgBox.setText("File name or location are empty, please fill both fields.");
        msgBox.setWindowTitle("Error Message");
        msgBox.setStandardButtons(QMessageBox::Ok );

        int ret = msgBox.exec();

    }
    //adds file name to file location
    location.append(name);



    //checks data stream
    ifstream fin(location);

    //if cannot find file
    if (!fin) {

        fileFound = false;
        //informs user
        QMessageBox msgBox;
        msgBox.setText("File cannot be found. Incorrect file name or location.");
        msgBox.setInformativeText("For example for 'C:/Users/a.txt', Location is 'C:/Users/' and Name is 'a.txt'");
        msgBox.setStandardButtons(QMessageBox::Ok );
        msgBox.setWindowTitle("Error Message");
        int ret = msgBox.exec();

    }
    //if can find file
    else{

        fileFound = true;
        //informs user of processing time
        QMessageBox msgBox;
        msgBox.setText("File found, depending on file size you may need to wait.");
        msgBox.setStandardButtons(QMessageBox::Ok );
        msgBox.setWindowTitle("File Located");
        int ret = msgBox.exec();
    }

    // if file is found simulation can occur
    if (fileFound == true){

    //create instance of a display window for the simulation

        if (ui->simpleRad->isChecked() == true){ // if the simulation is for a simple pendulum
            displayWindow * d = new displayWindow(0);
            d->SetFile(name,location);
            d->show();
        }

        if (ui->dumbbellRad->isChecked() == true){ // if the simulation is for a dumbbell pendulum
            displayWindow * d = new displayWindow(1);
            d->SetFile(name,location);
            d->show();
        }

        if (ui->flailRad->isChecked() == true){ // if the simulation is for a flail pendulum
            displayWindow * d = new displayWindow(2);
            d->SetFile(name,location);
            d->show();
        }

        if (ui->robotRad->isChecked() == true){ // if the simulation is for a virtual robot
            displayWindow * d = new displayWindow(3);
            d->SetFile(name,location);
            d->show();
        }
    }

}




