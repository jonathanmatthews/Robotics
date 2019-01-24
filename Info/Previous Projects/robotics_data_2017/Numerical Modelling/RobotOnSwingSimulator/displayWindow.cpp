/*
 * displayWindow.cpp
 *
 *  Created on: 01/03/2017
 *      Author: Joshua Torbett
 */

#include "displayWindow.h"
#include "ui_displayWindow.h"
#include <QMessageBox>
#include <QDebug>
using namespace std;

displayWindow::displayWindow(int type, QWidget *parent):
    QWidget(parent),
    ui(new Ui::displayWindow)
{
    ui->setupUi(this);

    //sets type of simulation
    fType = type;

    //sets screen size
    setFixedSize(600,400);


    //Sets inital conditions for display window
    setStyleSheet("background-color:black");
    setAutoFillBackground(false);

    //set inital variables values
    fScale = 50; // default scale increase for simulation
    ft = 0;

    //Show the window
    show();

    //Prevent implicit redraw of the background
    setAttribute(Qt::WA_OpaquePaintEvent);

    //set timer linked to update slot, so that is triggers the paint event every tick
    connect(fTimer, SIGNAL(timeout()), this, SLOT(update()));




}

displayWindow::~displayWindow()
{
    delete ui;
}



void displayWindow::paintEvent(QPaintEvent *)
{

    //gets value  dt and length of simulation
    double dt = fTime[1] - fTime[0]; // time step
    double tFinal = fTime[fTime.size()-2];


    //set up Qpainter
    QPainter painter(this);
    painter.setBrush(Qt::white);
    painter.setPen(Qt::white);

    //clear window
    painter.fillRect(QRect(0,0,width()-1,height()-1),QPalette::Text);

    //variables for simulation
    double h = this->height(), w = this->width(); // height and width of screen
    double pH = 50; // pendulum height

    //drawing masses
    for (int j = 0; j < fObjects.size(); j++){
        //variable to make code clearer - position of mass connected to pivot
             double x1 = fObjects[0][ft].GetX()*fScale, y1 = fObjects[0][ft].GetY()*fScale;

        //position of each mass
    double xPos = (fObjects[j][ft].GetX()*fScale+w/2), yPos = (fObjects[j][ft].GetY()*fScale+h/2);

         int r = 10; //radius of masses

        //corrections to make flail  model simulate properly
        if (fType == kFlail){ h = 0;} //different h value for flail to fit in screen
        if (fType == kFlail && j ==0){ //redraws mass main mass, as isn't included without this
            painter.drawEllipse(x1 + w/2, y1 + h/2 ,r,r);
        }

          painter.drawEllipse(xPos,yPos,r,r);// draw mass



        //drawing lines to and between masses

           if (fType == kSimple){ // for simple pendulum

               fScale = 50; // setting scale for model

               //drawing line from pivot to mass
             painter.drawLine(w/2,pH,xPos + r/2,yPos);

             //set painter for drawing trace
             painter.setPen(Qt::red);

             for (int k = 0; k < ft; k++)
             {   //trace the path of the mass connected to the pivot
                 painter.drawPoint((fObjects[0][k].GetX()*fScale + w/2 + r/2),(fObjects[0][k].GetY()*fScale + h/2 + r/2));
            }

             //set painter for drawing lines and masses
             painter.setPen(Qt::white);
           }

           if (fType == kDumbbell){ //for dumbbbel pendulum

               fScale = 50; // setting scale for model

               //variables to make code clearer
               double x2 = fObjects[1][ft].GetX()*fScale, y2 = fObjects[1][ft].GetY()*fScale;
               double x3 = fObjects[2][ft].GetX()*fScale, y3 = fObjects[2][ft].GetY()*fScale;

               //line from pivot to m1
                 painter.drawLine(w/2,pH,x1 + w/2 + r/2,y1 + h/2 + r/2);

                 //line m2 to m3
               painter.drawLine(x2 + w/2 + r/2,y2 +h/2 + r/2,x3 + w/2 + r/2,y3 + h/2 + r/2);

               //set painter for drawing trace
               painter.setPen(Qt::red);

               for (int k = 0; k < ft; k++)
               {    //trace the path of the mass connect to the pivot
                    painter.drawPoint((fObjects[0][k].GetX()*fScale + w/2 + r/2),(fObjects[0][k].GetY()*fScale + h/2 + r/2));
               }

               //set painter for drawing lines and masses
               painter.setPen(Qt::white);
           }

           if (fType == kFlail){ //for flail pendulum

               fScale = 200; // setting scale for model

               //variables to make code clearer

               double x2 = fObjects[1][ft].GetX()*fScale, y2 = fObjects[1][ft].GetY()*fScale;
               double x3 = fObjects[2][ft].GetX()*fScale, y3 = fObjects[2][ft].GetY()*fScale;
               double x4 = fObjects[3][ft].GetX()*fScale, y4 = fObjects[3][ft].GetY()*fScale;
               double x5 = fObjects[4][ft].GetX()*fScale, y5 = fObjects[4][ft].GetY()*fScale;

               //line to m1
               painter.drawLine(w/2,pH,x1 + w/2 + r/2,y1 + r/2);
               //line m1 to m2
               painter.drawLine(x1 + w/2 + r/2,y1 + r/2,x2 + w/2 + r/2,y2 + r/2);
               //line m1 to m3
               painter.drawLine(x1 + w/2 + r/2,y1 + r/2,x3 + w/2 + r/2,y3 + r/2);
               //line m2 to m4
               painter.drawLine(x2 + w/2 + r/2,y2 + r/2,x4 + w/2 + r/2,y4 + r/2);
               //line m3 to m5
               painter.drawLine(x3 + w/2 + r/2,y3 + r/2,x5 + w/2 + r/2,y5 + r/2);

               //set painter for drawing trace
               painter.setPen(Qt::red);
               for (int k = 0; k < ft; k++)
               {  //traces the mass connect to the pivot, however this caused the program to lag so is currently left out
                  // painter.drawPoint((fObjects[0][k].GetX()*fScale+w/2+r/2),(fObjects[0][k].GetY()*fScale+h/2+r/2));
               }
               //set painter for drawing lines and masses
               painter.setPen(Qt::white);
           }


           if (fType == kRobot){ //for virtual robot

               fScale = 500; //setting scale for model

               //variables to make code clearer
               double torsoX = fObjects[0][ft].GetX()*fScale, torsoY = fObjects[0][ft].GetY()*fScale;
               double headX = fObjects[1][ft].GetX()*fScale, headY = fObjects[1][ft].GetY()*fScale;
               double armX = fObjects[2][ft].GetX()*fScale, armY = fObjects[2][ft].GetY()*fScale;
               double thighX = fObjects[3][ft].GetX()*fScale, thighY = fObjects[3][ft].GetY()*fScale;
               double tibiaX = fObjects[4][ft].GetX()*fScale, tibiaY = fObjects[4][ft].GetY()*fScale;
               double footX = fObjects[5][ft].GetX()*fScale, footY = fObjects[5][ft].GetY()*fScale;
               double baseX = fObjects[6][ft].GetX()*fScale, baseY= fObjects[6][ft].GetY()*fScale;

              //line from robot torso to head
              painter.drawLine(torsoX + w/2 + r/2,torsoY + h/2 + r/2, headX + w/2 + r/2, headY + h/2 + r/2);
              //line from thign to tibia
              painter.drawLine(thighX + w/2 +r/2,thighY + h/2 + r/2, tibiaX + w/2 + r/2, tibiaY + h/2 + r/2);
              //line from tibia to foot
              painter.drawLine(tibiaX + w/2 + r/2,tibiaY + h/2 + r/2, footX + w/2 + r/2, footY + h/2 + r/2);
              //line from torso to arm
              painter.drawLine(torsoX + w/2 + r/2, torsoY + h/2 + r/2, armX + w/2 + r/2, armY + h/2 + r/2);
              //line from torso to base
              painter.drawLine(torsoX + w/2 + r/2, torsoY + h/2 + r/2, baseX + w/2 + r/2, baseY + h/2 + r/2);
              //line from base thigh
              painter.drawLine(baseX + w/2 + r/2, baseY + h/2 + r/2, thighX + w/2 + r/2, thighY + h/2 + r/2);

           }

    }


    ft++; // increase pseudo timer after each painte event

    //checks if the end of the final has been reached
    if ((ft*dt) > tFinal){
     //reset time
     ft = 0;
    }
   }

void displayWindow::readFile(std::string location){

    //location of text file
    std::string filename = location ;


    //gets data for simulation

    ifstream fin(filename);


    //read headings out
    std::string headings;
    getline(fin, headings);

    //assgin varaibles to read data into vector later
    double var1, var2, var3, var4, var5, var6, var7, var8, var9, var10, var11, var12, var13, var14, var15;

    if (fType == kSimple){ //for simple pendulum

        //vector(s) to store mass position data
        vector<twoVector> m1;

        //read data from file into variables
        while (fin >> var1 >> var2 >> var3 )
        {
            //put data from variables into vector(s)
           m1.push_back(twoVector(var2,var3));
            fTime.push_back(var1);
        }

        //put mass vectors into object vector
    fObjects.push_back(m1);
    }

    if (fType == kDumbbell){//for dumbbell pendulum

        //vector(s) to store mass position data
        vector<twoVector> m1, m2, m3;

        //read data from file into variables
        while (fin >> var1 >> var2 >> var3 >> var4 >> var5 >> var6 >> var7)
        {
            //put data from variables into vector(s)
           m1.push_back(twoVector(var2,var3));
           m2.push_back(twoVector(var4,var5));
           m3.push_back(twoVector(var6,var7));
            fTime.push_back(var1);
        }

        //put mass vectors into object vector
        fObjects.push_back(m1);
        fObjects.push_back(m2);
        fObjects.push_back(m3);
    }

    if (fType == kFlail){ //for flail pendulum

        //vector(s) to store mass position data
        vector<twoVector> m1, m2, m3, m4, m5;

        //read data from file into variables
        while (fin >> var1 >> var2 >> var3 >> var4 >> var5 >> var6 >> var7 >> var8 >> var9 >> var10 >> var11){

            //put data from variables into vector(s)
            m1.push_back(twoVector(var2,var3));
            m2.push_back(twoVector(var4,var5));
            m3.push_back(twoVector(var6,var7));
            m4.push_back(twoVector(var8,var9));
            m5.push_back(twoVector(var10,var11));

            fTime.push_back(var1);
        }

        //put mass vectors into object vector
        fObjects.push_back(m1);
        fObjects.push_back(m2);
        fObjects.push_back(m3);
        fObjects.push_back(m4);
        fObjects.push_back(m5);
    }

    if (fType == kRobot){ //for virtual robot model

        //vector(s) to store mass position data
         vector<twoVector> torso, head, arm, thigh, tibia, foot, base;

         //read data from file into variables
          while (fin >> var1 >> var2 >> var3 >> var4 >> var5 >> var6 >> var7 >> var8 >> var9 >> var10 >> var11 >> var12 >> var13 >> var14 >> var15)
          {
              //put data from variables into vector(s)
              torso.push_back(twoVector(var2,var3));
              head.push_back(twoVector(var4,var5));
              arm.push_back(twoVector(var6,var7));
              thigh.push_back(twoVector(var8,var9));
              tibia.push_back(twoVector(var10, var11));
              foot.push_back(twoVector(var12,var13));
              base.push_back(twoVector(var14,var15));
              fTime.push_back(var1);
          }

          //put mass vectors into object vector
          fObjects.push_back(torso);
          fObjects.push_back(head);
          fObjects.push_back(arm);
          fObjects.push_back(thigh);
          fObjects.push_back(tibia);
          fObjects.push_back(foot);
          fObjects.push_back(base);


    }



}

void displayWindow::SetFile(std::string name, std::string location)
{
//reads file at location
 this->readFile(location);
 //time step dt
double dt = fTime[1] - fTime[0];

//starts timer based of dt
 fTimer->start(dt*1000); //ticks every dt ms
}



