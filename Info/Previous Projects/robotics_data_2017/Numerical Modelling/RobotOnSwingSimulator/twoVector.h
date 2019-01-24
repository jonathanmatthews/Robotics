/*
 * twoVector.h
 *
 *  Created on: 03/12/2016
 *      Author: Joshua Torbett
 */

#ifndef TWOVECTOR_H
#define TWOVECTOR_H


class twoVector
{
public:
    //constructors
    twoVector();
    twoVector(double x, double y);


    //deconstructor
    virtual ~twoVector();


    //get methods
    inline double GetX() const { return fX; };
    inline double GetY() const { return fY; };

    //set methods
    inline void SetX(double x) { fX = x; };
    inline void SetY(double y) { fY = y; };
    inline void SetXY(double x, double y);



    //dot product of 2 two vectors
    inline double Dot(const twoVector & ) const;

    //magnitude of two vector
    double Mag() const;

    //magnitude sqaured of two vector
    double Mag2() const;

    //operators
    inline twoVector & operator = (const twoVector &);
    twoVector(const twoVector &);
    twoVector(const double *);

private:
    //components
    double fX, fY;
};

//operators
twoVector operator + (const twoVector &, const twoVector &);
twoVector operator - (const twoVector &, const twoVector &);
twoVector operator * (const double &, const twoVector&);

// operator
inline twoVector & twoVector::operator = (const twoVector & p) {
    fX = p.fX;
    fY = p.fY;
    return *this;
}

// set components
inline void twoVector::SetXY(double x, double y) {
    fX = x;
    fY = y;
}

//magintude squared of 2 vector
inline double twoVector::Mag2() const { return fX*fX + fY*fY; }

//dot product
inline double twoVector::Dot(const twoVector & p) const {
    return fX*p.fX + fY*p.fY;

}

#endif /* TWOVECTOR_H_ */
