// Name: Max Hadfield
// Date: 24.01.16
// Damped Simple Pendulum simulation using 2nd order Runge Kutta method

#include <cmath>
#include <fstream>
#include <iomanip>

using namespace std;

//define functions

//differential equations to be solved
inline double theta_deriv(double omega)
{
    return omega;
}

inline double omega_deriv(double length, double theta, double omega, double gamma, double m)
{
    return -(9.81/length)*sin(theta) - 2*gamma*m*omega;
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
    double theta=0.3647738; //initial angle = -20.9
    double omega=0; //angular velocity
    double a=0; //angular acceleration
    double x=0; //x position
    double y=0; //y position
    double t=0; //time
    double tmax=400; //time simulation is run for
    double length=1.815; //swing length
    double gamma=0.00443;//viscous damping coefficient/2
    double m=5.18253; //mass

    //Runge Kutta parameters
    double h=0; //step size for Runge Kutta
    double N=10000; //number of intervals for Runge Kutta
    double omega1=0, omega2=0, omega3 =0; //omega at half interval in Runge Kutta calculation
    double wk1=0,wk2=0,wk3=0,wk4=0; // for omega
    double theta1 =0, theta2 =0, theta3 =0; //theta at half interval in Runge Kutta calculation
    double ok1=0,ok2=0,ok3=0,ok4=0; // for theta

    //Link output file
    ofstream outFile("damped_simple_pendulum_results.txt");
    ofstream outFile2("GUI_Output.txt");

    //Ouput headings
    //outFile << "Time \tTheta \tx \ty \tomega \ta" << endl;
    outFile << "t\tTheta\ty" << endl;
    outFile2 << "t\tx\ty" << endl;

    //Define step size
    h = tmax/N;

    //loop for Runge Kutta calculation
    for(int n=0; n<=N; n++){

        //Calculates x, y and a
        x = XPosition(length, theta);
        y = YPosition(length, theta);
        a = omega_deriv(length, theta, omega, gamma, m);

        //outputs t, theta, x, y and omega to file
        //outFile << t << "\t" << theta*360/(2*3.1415) << "\t" << x << "\t" << y << "\t" << omega << "\t" << a << endl; // N*h instead of t
        outFile << t << "\t" << theta << "\t" << y << endl; //
        outFile2 << t << "\t" << x << "\t" << y << endl;

        //calculates t, theta and omega after half a step

        //step part 1
        ok1 = theta_deriv(omega);
        wk1 = omega_deriv(length, theta, omega, gamma, m);
        theta1= theta + ok1*(h/2);
        omega1 = omega + wk1*(h/2);

        //step part 2
        ok2 = theta_deriv(omega1);
        wk2 = omega_deriv(length, theta1, omega1, gamma, m);
        theta2 = theta + ok2*(h/2);
        omega2 = omega + wk2*(h/2);

        //step part 3
        ok3 = theta_deriv(omega2);
        wk3 = omega_deriv(length, theta2, omega2, gamma, m);
        theta3 = theta + ok3*(h);
        omega3 = omega + wk3*(h);

        //step part 4
        ok4 = theta_deriv(omega3);
        wk4 = omega_deriv(length, theta3, omega3,gamma, m);

        //increases theta and omega
        theta = theta + (ok1+2*ok2+2*ok3+ok4)*(h/6);
        omega = omega + (wk1+2*wk2+2*wk3+wk4)*(h/6);

        //calculates t after a whole step
        t += h;

    }

    //user instructions
    printf ("Results have been output to a file called \"simple_pendulum_results.txt\"\n");

    return 0;
}
