#ifndef BODYPART_H
#define BODYPART_H

#include "TwoVector.h"
#include <vector>
class BodyPart
{
public:
    BodyPart(BodyPart* parent, double mass, double angle, double length);
    virtual ~BodyPart();

    inline TwoVector getPosition();
    inline TwoVector getCOMPosition();
    inline TwoVector getVelocity();
    inline TwoVector getAcceleration();
    inline double getAngularVelocity();
    inline double getAngularAcceleration();
    inline double getMass();
    inline double getAngle();
    inline double getLength();
    inline bool getMotionCompete();

    inline void setPosition(TwoVector);
    inline void setVelocity(TwoVector);
    inline void setAcceleration(TwoVector);
    inline void setAngularVelocity(double);
    inline void setAngularAcceleration(double);
    inline void setAngle(double);
    inline void addPart(BodyPart *part);
    inline void setMotionComplete(bool);

    virtual void move(double thetaI, double thetaF, double speed, double dt,bool isMovingForward);

    //could not find a way to access otherwise, so made public
    BodyPart* fParent; // if no parent = 0
private:

    double fMass;
    double fAngle;
    TwoVector fPosition;
    TwoVector fVelocity;
    TwoVector fAcceleration;
    TwoVector fCOMPosition;
    double fAngularVelocity;
    double fAngularAcceleration;

    double fLength;
    std::vector<BodyPart*>fParts;
    bool fMotionComplete;
};

//
inline TwoVector BodyPart::getPosition(){

    if(fParent==0){return TwoVector((fLength/2)*cos(getAngle()),(fLength/2)*sin(getAngle()));}
    else{return fParent->getPosition()+TwoVector((fLength/2)*cos(getAngle()),(fLength/2)*sin(getAngle()));}

}

inline double BodyPart::getAngle(){

    if(fParent==0){return fAngle;}
    else{return fParent->getAngle()+fAngle;}
}

inline double BodyPart::getAngularVelocity(){

    if(fParent==0){return fAngularVelocity;}
    else{return fParent->getAngularVelocity()+fAngularVelocity;}
}

inline double BodyPart::getAngularAcceleration(){

    if(fParent==0){return fAngularAcceleration;}
    else{return fParent->getAngularAcceleration()+fAngularAcceleration;}
}

inline TwoVector BodyPart::getVelocity(){

    if(fParent==0){return fVelocity;}
    else{return fParent->getVelocity()+fVelocity;}
}

inline TwoVector BodyPart::getAcceleration(){

    if(fParent==0){return fAcceleration;}
    else{return fParent->getAcceleration()+fAcceleration;}
}

//inline TwoVector BodyPart::getCOMPosition(){return fPosition.operator *(0.5);}
inline TwoVector BodyPart::getCOMPosition(){return TwoVector((fLength/2)*cos(fAngle),(fLength/2)*sin(fAngle));}
//inline TwoVector BodyPart::getVelocity(){return fVelocity;}
//inline TwoVector BodyPart::getAcceleration(){return fAcceleration;}
//inline double BodyPart::getAngularVelocity(){return fAngularVelocity;}
//inline double BodyPart::getAngularAcceleration(){return fAngularAcceleration;}
inline double BodyPart::getMass(){return fMass;}
inline double BodyPart::getLength(){return fLength;}
inline bool BodyPart::getMotionCompete(){return fMotionComplete;}



inline void BodyPart::setPosition(TwoVector tV){fPosition=tV;}

inline void BodyPart::setVelocity(TwoVector tV){
    fVelocity=tV;
    fAngularVelocity=fVelocity.getX()*sin(fAngle)+fVelocity.getY()*cos(fAngle);
}
inline void BodyPart::setAcceleration(TwoVector tV){
    fAcceleration=tV;
    fAngularAcceleration=fAcceleration.getX()*sin(fAngle)+fAcceleration.getY()*cos(fAngle);
}

inline void BodyPart::setAngularVelocity(double w){
    fAngularVelocity=w;
    fVelocity=TwoVector(getCOMPosition().absolute()*w*cos(fAngle),getCOMPosition().absolute()*w*sin(fAngle));
    //fVelocity=TwoVector(w*sin(fAngle),w*cos(fAngle));
}

inline void BodyPart::setAngularAcceleration(double w){
    fAngularAcceleration=w;
    //fAcceleration=TwoVector(w*sin(fAngle),w*cos(fAngle));
    fAcceleration=TwoVector(getCOMPosition().absolute()*w*cos(fAngle),getCOMPosition().absolute()*w*sin(fAngle));


}
inline void BodyPart::setAngle(double angle){fAngle=angle;}
inline void BodyPart::addPart(BodyPart *part){fParts.push_back(part);}
inline void BodyPart::setMotionComplete(bool b){fMotionComplete=b;}


#endif // BODYPART_H
