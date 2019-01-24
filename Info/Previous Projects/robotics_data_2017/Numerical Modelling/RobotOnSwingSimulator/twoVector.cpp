/*
 *  twoVector.cpp
 *
 *  Created on: 03/12/2016
 *      Author: Joshua Torbett
 */

#include <math.h>
#include "twoVector.h"

//constructors
twoVector::twoVector()
    : fX(0.0), fY(0.0) {}
twoVector::twoVector(const twoVector & p)
    : fX(p.fX), fY(p.fY) {}
twoVector::twoVector(double x, double y)
    : fX(x), fY(y) {}
twoVector::twoVector(const double * x0)
    : fX(x0[0]), fY(x0[1]) {}

//de-constructor
twoVector::~twoVector() {}

//calculates magnitude of two vector
double twoVector::Mag() const
{return sqrt(Mag2());}


//operators
twoVector operator + (const twoVector & a, const twoVector & b) {
return twoVector(a.GetX() + b.GetX(), a.GetY() + b.GetY());
}


twoVector operator - (const twoVector & a, const twoVector & b) {
    return twoVector(a.GetX() - b.GetX(), a.GetY() - b.GetY());
}
twoVector operator * (const double & p, const twoVector & a) {	return twoVector(a.GetX()*p, a.GetY()*p);}
