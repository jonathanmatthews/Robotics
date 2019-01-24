//driven rotation of dumbell no damping using RK4
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
    return -omega;
}

inline double omega_deriv(double length, double length_deriv , double theta, double omega, double t, double spin_accel, double radius, double w0)

{
    return spin_accel*radius*radius/(length*length + radius*radius) + w0*w0*sin(theta);
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

int main()
{
    //declare variables

    //system parameters
    double thetastart = 0; //initial angle = pi/2
    double theta=thetastart;
    double omega=0; //angular velocity
    double a=0; //angular acceleration
    double x=0; //x position
    double y=0; //y position
    double t=0; //time
    double tmax=50; //time simulation is run for

    //Runge Kutta parameters
    double h=0.02; //step size for Runge Kutta
    double N=2500; //number of intervals for Runge Kutta
    double omega1=0, omega2=0, omega3 =0; //omega at half interval in Runge Kutta calculation
    double wk1=0,wk2=0,wk3=0,wk4=0; // for omega
    double theta1 =0, theta2 =0, theta3 =0; //theta at half interval in Runge Kutta calculation
    double ok1=0,ok2=0,ok3=0,ok4=0; // for theta

    //Link output file
    ofstream outFileOmega("driven_rotation_optimal_freq.txt");

    //Ouput headings
    //outFileOmega << "Time \tTheta \tx \ty \tomega \ta" << endl;
    //outFileOmega << "w/w0\tw\tmax_theta/start_theta\tmax_theta" << endl;
    outFileOmega << "t\tx1\ty1\tx2\ty2\tx3\ty3\n";

    //Define step size
    N = tmax/h;

    //paramenters for finding optimal frequency
    double length_0=2.5; //initial length (equilibrium)
    double length=length_0; //swing length
    double length_deriv=0;

    double theta_max=0;

    double spin_accel=0;
    double radius=0.2*length_0;
    double max_spin=2;

    double w0=(9.81*length_0)/(length_0*length_0 + radius*radius);

    double wmin=0*w0; //minimum bound for frequency iteration
    double wmax=3*w0; //upper bound for frequency iteration
    double dw=0.01; //change in frequency with each iteration
    double w=w0;

    double phi = max_spin*sin(w*t);

    double x1 = XPosition(length,theta), y1 = YPosition(length,theta) ;
    double x2 = x1 + radius*cos(phi), y2 = y1 + radius*sin(phi);
    double x3 = x1 - radius*cos(phi), y3 = y1 - radius*sin(phi);

//    while(true){

//        if(w>wmax){
//            //user instructions
//            printf ("Results have been output to a file called \"driven_rotation_optimal_freq.txt\"\n");
//            return 0;
//        }

//        theta_max=0;
//        t=0;
//        theta=thetastart;
//        omega=0;

        //loop for Runge Kutta calculation
        for(int n=0; n<=N; n++){

            //calculate spin change
            //phi(spin angle) = max_spin*sin(w*t);

            phi = -max_spin*sin(w*t);

            x1 = XPosition(length,theta),   y1 = YPosition(length,theta) ;
            x2 = x1 + radius*cos(phi),      y2 = y1 + radius*sin(phi);
            x3 = x1 - radius*cos(phi),      y3 = y1 - radius*sin(phi);

            spin_accel = max_spin*w*w*sin(w*t);

            //Calculates x, y and a
            x = XPosition(length, theta);
            y = YPosition(length, theta);
            a = omega_deriv(length, length_deriv, theta, omega, t, spin_accel, radius, w0);

            outFileOmega << t <<"\t"<< x1 <<"\t"<< y1 <<"\t"<< x2 <<"\t"<< y2 <<"\t"<< x3 <<"\t"<< y3 <<"\n";

            //calculates t, theta and omega after half a step

            //step part 1
            ok1 = theta_deriv(length, length_deriv, theta, omega, t);
            wk1 = omega_deriv(length, length_deriv, theta, omega, t, spin_accel, radius, w0);
            theta1= theta + ok1*(h/2);
            omega1 = omega + wk1*(h/2);

            //calculate spin change
            //phi(spin angle) = max_spin*sin(w*t);
            spin_accel = -max_spin*w*w*sin(w*(t+h/2));
            //step part 2
            ok2 = theta_deriv(length, length_deriv, theta1, omega1, t);
            wk2 = omega_deriv(length, length_deriv, theta1, omega1, t, spin_accel, radius, w0);
            theta2 = theta + ok2*(h/2);
            omega2 = omega + wk2*(h/2);

            //calculate spin change
            //phi(spin angle) = max_spin*sin(w*t);
            spin_accel = -max_spin*w*w*sin(w*(t+h/2));
            //step part 3
            ok3 = theta_deriv(length, length_deriv, theta2, omega2, t);
            wk3 = omega_deriv(length, length_deriv, theta2, omega2, t, spin_accel, radius, w0);
            theta3 = theta + ok3*(h);
            omega3 = omega + wk3*(h);

            //calculate spin change
            //phi(spin angle) = max_spin*sin(w*t);
            spin_accel = -max_spin*w*w*sin(w*(t+h));
            //step part 4
            ok4 = theta_deriv(length, length_deriv, theta3, omega3, t);
            wk4 = omega_deriv(length, length_deriv, theta3, omega3, t, spin_accel, radius, w0);

            //increases theta and omega
            theta = theta + (ok1+2*ok2+2*ok3+ok4)*(h/6);
            omega = omega + (wk1+2*wk2+2*wk3+wk4)*(h/6);

            //update theta_max
            if(theta > theta_max){
                theta_max = theta;
            }

            //calculates t after a whole step
            t = t+h;
        }

//        outFileOmega << w/w0 << "\t" << w << "\t" << theta_max/thetastart << "\t" << theta_max << endl;
//        w += dw;
//    }

    return 0;
}
