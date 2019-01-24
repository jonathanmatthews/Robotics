//driven length simple pendulum using RK4
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

int main()
{
    //declare variables

    //system parameters
    double thetastart = 0.5*atan(1); //initial angle
    double theta=thetastart;
    double omega=0; //angular velocity
    double a=0; //angular acceleration
    double x=0; //x position
    double y=0; //y position
    double t=0; //time
    double tmax=500; //time simulation is run for

    //Runge Kutta parameters
    double h=0.02; //step size for Runge Kutta
    double N=2500; //number of intervals for Runge Kutta
    double omega1=0, omega2=0, omega3 =0; //omega at half interval in Runge Kutta calculation
    double wk1=0,wk2=0,wk3=0,wk4=0; // for omega
    double theta1 =0, theta2 =0, theta3 =0; //theta at half interval in Runge Kutta calculation
    double ok1=0,ok2=0,ok3=0,ok4=0; // for theta

    //Link output file
    ofstream outFileOmega("driven_length_optimal_freq.txt");

    //Ouput headings
    //outFileOmega << "Time \tTheta \tx \ty \tomega \ta" << endl;
    outFileOmega << "w/w0\tw\tmax_theta/start_theta\tmax_theta" << endl;

    //Define step size
    N = tmax/h;

    //paramenters for finding optimal frequency
    double length_0=2.5; //initial length (equilibrium)
    double length_deriv=0; //rate of change of length
    double length=length_0; //swing length

    double max_var=length_0*0.01; //max length variation
    double w0=pow(9.81/length_0,0.5); //natural frequency at equilibrium length

    double theta_max=0;

    double wmin=0*w0; //minimum bound for frequency iteration
    double wmax=3*w0; //upper bound for frequency iteration
    double dw=0.01; //change in frequency with each iteration
    double w=wmin;

    while(true){

        if(w>wmax){
            //user instructions
            printf ("Results have been output to a file called \"driven_length_optimal_freq.txt\"\n");
            return 0;
        }

        theta_max=0;
        t=0;
        theta=thetastart;
        omega=0;

        //loop for Runge Kutta calculation
        for(int n=0; n<=N; n++){

            //calculate length change
            length = length_0 + max_var*sin(w*t);
            length_deriv = max_var*w*cos(w*t);

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

            //calculate length change
            length = length_0 + max_var*sin(w*(t+h/2));
            length_deriv = max_var*w*cos(w*(t+h/2));
            //step part 2
            ok2 = theta_deriv(length, length_deriv, theta1, omega1, t);
            wk2 = omega_deriv(length, length_deriv, theta1, omega1, t);
            theta2 = theta + ok2*(h/2);
            omega2 = omega + wk2*(h/2);

            //calculate length change
            length = length_0 + max_var*sin(w*(t+h/2));
            length_deriv = max_var*w*cos(w*(t+h/2));
            //step part 3
            ok3 = theta_deriv(length, length_deriv, theta2, omega2, t);
            wk3 = omega_deriv(length, length_deriv, theta2, omega2, t);
            theta3 = theta + ok3*(h);
            omega3 = omega + wk3*(h);

            //calculate length change
            length = length_0 + max_var*sin(w*(t+h));
            length_deriv = max_var*w*cos(w*(t+h));
            //step part 4
            ok4 = theta_deriv(length, length_deriv, theta3, omega3, t);
            wk4 = omega_deriv(length, length_deriv, theta3, omega3, t);

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

        outFileOmega << w/w0 << "\t" << w << "\t" << theta_max/thetastart << "\t" << theta_max << endl;
        w += dw;
    }

    return 0;
}
