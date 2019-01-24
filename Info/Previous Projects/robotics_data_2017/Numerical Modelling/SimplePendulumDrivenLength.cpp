//driven length simple pendulum using RK4
//harry pratten

#include <cmath>
#include <fstream>
#include <iomanip>

using namespace std;

//define functions

//differential equations to be solved
inline double theta_deriv(double length, double length_deriv, double theta, double omega, double t)
{
    return -omega;
}

inline double omega_deriv(double length, double length_deriv , double theta, double omega, double t, double spin_accel, double radius, double w0)

{
    return 2*length_deriv*omega/length + 9.81*sin(theta)/length;
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
    double thetastart = 0.1*atan(1); //initial angle = pi/2
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
    ofstream outFile("length_pendulum.txt");

    //Ouput headings
    //outFile << "t\ttheta\tx\ty\tomega\ta\tkinetic\tpotential\ttotalE" << endl;
    //outFileOmega << "w\tt\trotational_accel\tx\ty\ttheta" << endl;
    outFile << "t\tx\ty\tlength\n";

    //Define step size
    N = tmax/h;

    //paramenters for finding optimal frequency
    double g=9.81;
    double length_0=2.5; //initial length (equilibrium)
    double w0=pow(g/length_0,0.5);
    double w=2*w0;
    double max_var=length_0*0.1; //max length variation
    double length=length_0 + max_var*sin(w*t); //swing length
    double length_deriv=max_var*w*cos(w*t);

    double pi=3.14;
    double kinetic=pow(omega*length,2)/2;
    double potential=-g*(y-length);
    double totalE=0;

    //irrelevant
    double spin_accel=0;
    double radius=0;





    //loop for Runge Kutta calculation
    for(int n=0; n<=N; n++){



        length = length_0 + max_var*sin(w*t);
        length_deriv = max_var*w*cos(w*t);

        kinetic=pow(omega*length,2)/2;
        potential=-g*(y-length);
        totalE=kinetic+potential;

        //Calculates x, y and a
        x = XPosition(length, theta);
        y = YPosition(length, theta);
        a = omega_deriv(length, length_deriv, theta, omega, t, spin_accel, radius, w0);

        //outFile << t << "\t" << theta << "\t" << x << "\t" << y << "\t" << omega << "\t" << a << "\t" << kinetic << "\t" << potential << "\t" << totalE << endl;
        outFile << t << "\t" << x << "\t" << y << "\t" << length <<"\n";

        //calculates t, theta and omega after half a step

        //step part 1
        ok1 = theta_deriv(length, length_deriv, theta, omega, t);
        wk1 = omega_deriv(length, length_deriv, theta, omega, t, spin_accel, radius, w0);
        theta1= theta + ok1*(h/2);
        omega1 = omega + wk1*(h/2);

        //step part 2
        ok2 = theta_deriv(length, length_deriv, theta1, omega1, t);
        wk2 = omega_deriv(length, length_deriv, theta1, omega1, t, spin_accel, radius, w0);
        theta2 = theta + ok2*(h/2);
        omega2 = omega + wk2*(h/2);

        //step part 3
        ok3 = theta_deriv(length, length_deriv, theta2, omega2, t);
        wk3 = omega_deriv(length, length_deriv, theta2, omega2, t, spin_accel, radius, w0);
        theta3 = theta + ok3*(h);
        omega3 = omega + wk3*(h);

        //step part 4
        ok4 = theta_deriv(length, length_deriv, theta3, omega3, t);
        wk4 = omega_deriv(length, length_deriv, theta3, omega3, t, spin_accel, radius, w0);

        //increases theta and omega
        theta = theta + (ok1+2*ok2+2*ok3+ok4)*(h/6);
        omega = omega + (wk1+2*wk2+2*wk3+wk4)*(h/6);

        //calculates t after a whole step
        t += h;
    }

    //user instructions
    printf ("Results have been output to a file called \"length_pendulum.txt\"\n");

    return 0;
}
