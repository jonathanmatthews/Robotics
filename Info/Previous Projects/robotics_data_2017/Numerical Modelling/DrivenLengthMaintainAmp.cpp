//driven length custom simple pendulum using RK4
//harry pratten

#include <cmath>
#include <fstream>
#include <iomanip>
#include <iostream>

using namespace std;

//define functions

//differential equations to be solved
inline double theta_deriv(double length, double length_deriv, double theta, double omega, double t)
{
    return omega;
}

inline double omega_deriv(double length, double length_deriv , double theta, double omega, double t)
{
    return -(9.81/length)*sin(theta) - 2*length_deriv*omega/length;
}

//function to calculate x position of mass
inline double XPosition(double length, double theta)
{
    return length * sin(theta);
}

//function to calculate y position of mass
inline double YPosition(double length, double theta)
{
    return length * cos(theta);
}

inline double SetLength(double length, double w, double a, double y, double theta, double dl, double uplim, double lowlim){

    if (length == uplim){ return length;}
    if (length > uplim){ return length-dl;}
    if (length == lowlim){ return length;}
    if (length < lowlim){ return length+dl;}

    double g=9.81;
    double pi=3.14;
    double kinetic=pow(w*length,2)/2;
    double potential=g*y;

    if (kinetic > 0.95*potential){ return length;}

    if ((a > 0) && (w > 0)){ //moving towards centre
        return length-dl;
    }
    if ((a > 0) && (w < 0)){ //moving away from centre
        return length+dl;
    }
    if ((a < 0) && (w > 0)){ //moving away from centre
        return length+dl;
    }
    if ((a < 0) && (w < 0)){ //moving towards centre
        return length-dl;
    }
}

int main()
{
    //declare variables

    //paramenters for finding optimal frequency
    double length_0=2.5; //initial length (equilibrium)
    double length_deriv=0; //rate of change of length
    double length=length_0; //swing length
    double uplim = 1.05*length_0;
    double lowlim = 0.95*length_0;
    double dl = 0.05*length_0;

    double w0=pow(9.81/length_0,0.5); //natural frequency at equilibrium length
    double wa = 2*w0;

    //system parameters
    double thetastart = 0.1*atan(1); //initial angle
    double theta=thetastart; //set intial angle
    double omega=0; //angular velocity
    double a=0; //angular acceleration
    double x=XPosition(length, theta); //x position
    double y=YPosition(length, theta); //y position
    double t=0; //time
    double tmax=1000; //time simulation is run for

    //Runge Kutta parameters
    double h=0.02; //step size for Runge Kutta
    int N=2500; //number of intervals for Runge Kutta
    double omega1=0, omega2=0, omega3 =0; //omega at half interval in Runge Kutta calculation
    double wk1=0,wk2=0,wk3=0,wk4=0; // for omega
    double theta1 =0, theta2 =0, theta3 =0; //theta at half interval in Runge Kutta calculation
    double ok1=0,ok2=0,ok3=0,ok4=0; // for theta

    //Link output file
    ofstream outFileCustom("driven_length_custom.txt");

    //Ouput headings
    //outFileCustom << "Time \tTheta \tx \ty \tomega \ta" << endl;
    //outFileCustom << "t\ttheta\tx\ty\ta\tlength" << endl;
    outFileCustom << "t\tx\ty\n";

    //Define N steps
    N = (int)tmax/h;

//    for(int count=0; count<=N; count++){

//        t=0;
//        theta=thetastart;
//        omega=0;

//        outFileCustom << t << "\t" << theta << "\t" << x << "\t" << y << "\t" << a << "\t" << length << endl;

        //loop for Runge Kutta calculation
        for(int n=0; n<=N; n++){

            //Calculates x, y and a
            x = XPosition(length, theta);
            y = YPosition(length, theta);
            a = omega_deriv(length, length_deriv, theta, omega, t);

            //calculates t, theta and omega after half a step

            //step part 1
            ok1 = theta_deriv(length, length_deriv, theta, omega, t);
            wk1 = omega_deriv(length, length_deriv, theta, omega, t);
            theta1= theta + ok1*(h/2);
            omega1 = omega + wk1*(h/2);

            //step part 2
            ok2 = theta_deriv(length, length_deriv, theta1, omega1, t);
            wk2 = omega_deriv(length, length_deriv, theta1, omega1, t);
            theta2 = theta + ok2*(h/2);
            omega2 = omega + wk2*(h/2);

            //step part 3
            ok3 = theta_deriv(length, length_deriv, theta2, omega2, t);
            wk3 = omega_deriv(length, length_deriv, theta2, omega2, t);
            theta3 = theta + ok3*(h);
            omega3 = omega + wk3*(h);

            //step part 4
            ok4 = theta_deriv(length, length_deriv, theta3, omega3, t);
            wk4 = omega_deriv(length, length_deriv, theta3, omega3, t);

            //increases theta and omega
            theta = theta + (ok1+2*ok2+2*ok3+ok4)*(h/6);
            omega = omega + (wk1+2*wk2+2*wk3+wk4)*(h/6);

            //calculates t after a whole step
            t = t+h;

            //outFileCustom << t << "\t" << theta << "\t" << x << "\t" << y << "\t" << a << "\t" << length << endl;
            outFileCustom << t <<"\t"<< x << "\t" << y <<"\n";

            //double new_length = SetLength(length,omega,a,y,theta,dl,uplim,lowlim);
            double new_length = length_0 + dl*sin(wa*t);
            length_deriv = (new_length - length)/h;
            //length = new_length;
            length = length_0 + dl*sin(wa*t);
        }

        printf ("Results have been output to a file called \"driven_length_custom.txt\"\n");
        return 0;
//    }

//    return 0;
}
