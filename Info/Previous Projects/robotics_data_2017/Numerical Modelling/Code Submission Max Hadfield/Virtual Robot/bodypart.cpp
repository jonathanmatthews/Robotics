#include "BodyPart.h"

#include <cmath>
#include <iostream>
//#include <QDebug>
BodyPart::BodyPart(BodyPart* parent,double mass,double angle,double length):
    fParent(parent),
    fMass(mass),
    fAngle(angle),
    fLength(length)
{
    fPosition=TwoVector(0,0);
    fVelocity=TwoVector(0,0);
    fAcceleration=TwoVector(0,0);
    fAngularVelocity=0;
    fAngularAcceleration=0;
    fMotionComplete=true;
}

BodyPart::~BodyPart(){}

//movement in a step-like manner with a constant acceleration
void BodyPart::move(double thetaI, double thetaF, double speed, double dt, bool isMovingForward){

    if(fMotionComplete==true){

        if(fAngularVelocity==0){
            setAngularAcceleration(0);
        }

        else{

            double Acc = speed/0.48;

            if (isMovingForward==true){

                if(fAngle!=thetaF){setAngularAcceleration(-Acc);}

                if(getAngularVelocity()>0){setAngularVelocity(getAngularVelocity()+getAngularAcceleration()*dt);}
                else{setAngularVelocity(0);}

                setAngle(fAngle+getAngularVelocity()*dt);

            }

            else{

                if(fAngle!=thetaI){setAngularAcceleration(Acc);}

                if(getAngularVelocity()<0){setAngularVelocity(getAngularVelocity()+getAngularAcceleration()*dt);}
                else{setAngularVelocity(0);}

                setAngle(fAngle+getAngularVelocity()*dt);

            }

        }
    }

    else{

        double Acc = speed/0.48;

        if(isMovingForward==true){

            if(fAngle!=thetaF){setAngularAcceleration(Acc);}

            if(abs(getAngularVelocity())<=speed){setAngularVelocity(getAngularVelocity()+getAngularAcceleration()*dt);}

            setAngle(fAngle+getAngularVelocity()*dt);

            if(getAngularVelocity()>0){if(fAngle>=(thetaF-(thetaF-thetaI)/2)){fMotionComplete=true;}}
            if(getAngularVelocity()<0){if(fAngle<=(thetaF-(thetaF-thetaI)/2)){fMotionComplete=true;}}


        }

        else{

            if(fAngle!=thetaI){setAngularAcceleration(-Acc);}

            if(abs(getAngularVelocity())<=speed){setAngularVelocity(getAngularVelocity()+getAngularAcceleration()*dt);}
            setAngle(fAngle+getAngularVelocity()*dt);

            if(getAngularVelocity()>0){if(fAngle>=thetaI+(thetaF-thetaI)/2){fMotionComplete=true;}}
            if(getAngularVelocity()<0){if(fAngle<=thetaI+(thetaF-thetaI)/2){fMotionComplete=true;}}


        }
    }
}
