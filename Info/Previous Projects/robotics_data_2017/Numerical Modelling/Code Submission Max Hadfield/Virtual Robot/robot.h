#ifndef ROBOT_H
#define ROBOT_H

#include "BodyPart.h"
#include <vector>
#include <iostream>

class Robot: public BodyPart
{
public:
    Robot(TwoVector Position);
    virtual ~Robot();

    void addBodyPart(BodyPart* part);

    inline double getCOMMass();
    inline TwoVector getCOMPosition();
    inline TwoVector getCOMVelocity();
    inline TwoVector getCOMAcceleration();
    inline std::vector<BodyPart*> getBodyParts();

private:
    std::vector<BodyPart*>fParts;
};

inline double Robot::getCOMMass(){
    double total=getMass();
    BodyPart* part;
    for(unsigned int i=0;i<fParts.size();i++){
        part=fParts[i];
        total+=part->getMass();
    }
    return total;
}

inline TwoVector Robot::getCOMPosition(){
    //TwoVector total=getPosition()*getMass();
    TwoVector total(0,0);
    BodyPart* part;
    for(unsigned int i=0;i<fParts.size();i++){
        part=fParts[i];
        //total.print();
        total+=(part->getCOMPosition()*part->getMass());
    }
    //return total/(2*getCOMMass());
    return total/(getCOMMass());
}

inline TwoVector Robot::getCOMVelocity(){
    //TwoVector total =getVelocity()*getMass();
    TwoVector total(0,0);
    BodyPart* part;
    for(unsigned int i=0;i<fParts.size();i++){
        part=fParts[i];
        total+=(part->getVelocity()*part->getMass());
        //std::cout << part->getLength() << std::endl;
        //part->getVelocity().print();
        //total.print();
        //std::cout << i << std::endl;
    }
    //return total/(2*getCOMMass());
    return total/(getCOMMass());
}
inline TwoVector Robot::getCOMAcceleration(){
    //TwoVector total =getAcceleration()*getMass();
    TwoVector total(0,0);
    BodyPart* part;
    for(unsigned int i=0;i<fParts.size();i++){
        part=fParts[i];
        total+=(part->getAcceleration()*part->getMass());
    }
    //return total/(2*getCOMMass());
    return total/(getCOMMass());
}

inline std::vector<BodyPart*> Robot::getBodyParts(){return fParts;};

#endif // ROBOT_H
