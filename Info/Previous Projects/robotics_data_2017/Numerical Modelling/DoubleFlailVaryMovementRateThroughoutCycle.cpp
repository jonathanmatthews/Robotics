//double flail movement optimisation
//harry pratten

#include <cmath>
#include <fstream>
#include <iomanip>
#include <iostream>

using namespace std;

//define functions

//differential equations to be solved
inline double theta_deriv(double omega)
{
    return omega;
}

inline double omega_deriv(double theta, double t2, double t2Dot, double t2DDot, double t3, double t3Dot, double t3DDot, double t4, double t4Dot, double t4DDot, double t5, double t5Dot, double t5DDot, double omega)

{
    double l1=1.815, l2=0.2115, l3=0.1, l4=0.11441, l5=0.14809;
    double r1=l1, r2=l2/2, r3=l3/2, r4=l4/2, r5=l5/2;
    double m1=0.42068, m2=2.20676, m3=0.77936, m4=0.68375, m5=1.21484;

    double g=9.81;

    return (-m2*r1*l2*(t2DDot*cos(theta-t2)+t2Dot*t2Dot*sin(theta-t2)) - m3*r1*l3*(t3DDot*cos(theta-t3)+t3Dot*t3Dot*sin(theta-t3)) - m4*r1*(r2*t2DDot*cos(theta-t2)+r2*t2Dot*t2Dot*sin(theta-t2))+(r4*t4DDot*cos(theta-t4)+r4*t4Dot*t4Dot*sin(theta-t4)) - m5*r1*(r3*t3DDot*cos(theta-t3)+r3*t3Dot*t3Dot*sin(theta-t3))+(r5*t5DDot*cos(theta-t5)+r5*t5Dot*t5Dot*sin(theta-t5)) - (m1*g*l1+(m2+m3+m4+m5)*g*r1)*sin(theta))/(m1*l1*l1+(m2+m3+m4+m5)*r1*r1)-0.006726*2*(m1+m2+m3+m4+m5)*omega;
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

    //Runge Kutta parameters
    double h=0.002; //step size for Runge Kutta
    double N=2500; //number of intervals for Runge Kutta
    double omega1=0, omega2=0, omega3 =0; //omega at half interval in Runge Kutta calculation
    double wk1=0,wk2=0,wk3=0,wk4=0; // for omega
    double theta1 =0, theta2 =0, theta3 =0; //theta at half interval in Runge Kutta calculation
    double ok1=0,ok2=0,ok3=0,ok4=0; // for theta

    //limits, relative to previous limb //get from joint rotation file //check!
    double t2max=0.236;//torso
    double t3max=0;//upper leg
    double t4max=0.593;//head
    double t5max=0.82;//lower leg
    double l1=1.815, l2=0.2115, l3=0.1, l4=0.11441, l5=0.14809;
    double r1=l1, r2=l2/2, r3=l3/2, r4=l4/2, r5=l5/2;
    double m1=0.42068, m2=2.20676, m3=0.77936, m4=0.68375, m5=1.21484;

    //Link output file
    ofstream outFile("double_hinged_flail_sawtooth_cycle.txt");

    //Ouput headings
    //single run
    //outFile << "time\ttheta\tterm1\ttheta_max\ttheta_max_prev\ta\tarea\tomega\tCOM_Y\n";
    //outFile << "t\tx1\ty1\tx2\ty2\tx3\ty3\tx4\ty4\tx5\ty5\n";
    //outFile << "t\ttheta\n";
    outFile << "startratio\toscillation\tamplitude\tt\n";

    double freqmin=0;
    double freqmax=5;
    double freq=freqmin;
    double df=0.01;

    double maxamp=0;

    //system parameters
    double length=1.815; //NB must be the same as l1 in function for 2nd order deriv
    double omega=0; //angular velocity
    double a=0; //angular acceleration
    double x=0; //x position
    double y=0; //y position
    double t=0; //time
    double tmax=250; //time simulation is run for

    //Define step size
    N=tmax/h;

    //paramters to be chosen
    double w=2.16;
    double pi=3.14;
    double T0 = 2*pi/w; //=1/f0
    cout << "T0 = " << T0 << "\n";


	//define double flail movement parameters
    double term1=0;
    double term1d=0;
    double term1dd=0;

	
    double thetastart=pi/64; //initial angle
    double theta=thetastart;

    //initialising angle parameters, note 'term1' will vary in the range -1 <= term1 <= 1
    //upper leg
    double t3=theta+1.57,                   	t3Dot=omega,                    t3DDot=a;                            //theta accel=0 for starting at equilibrium
    //torso
    double t2=theta-2.319-t2max-t2max*term1,   	t2Dot=omega-t2max*term1d,       t2DDot=a-t2max*term1dd;              //theta accel=0 for starting at equilibrium
    //head
    double t4=t2-0.0785-t4max*term1,        	t4Dot=t2Dot-t4max*term1d,       t4DDot=t2DDot-t4max*term1dd;
    //lower leg
    double t5=t3-0.733-t5max*term1,         	t5Dot=t3Dot-t5max*term1d,       t5DDot=t3DDot-t5max*term1dd;

	//x positions 
    //seat
    double x1 = XPosition(length,theta),    y1 = YPosition(length,theta);
    //upper leg
    double x3 = x1 + l3*sin(t3),            y3 = y1 + l3*cos(t3);
    //torso
    double x2 = x1 + l2*sin(t2),            y2 = y1 + l2*cos(t2);
    //head
    double x4 = x2 + l4*sin(t4),            y4 = y2 + l4*cos(t4);
    //lower leg
    double x5 = x3 + l5*sin(t5),            y5 = y3 + l5*cos(t5);

    /////for COM examination
    //seat
    double xm1 = XPosition(length,theta),    ym1 = YPosition(length,theta);
    //upper leg
    double xm3 = xm1 + r3*sin(t3),            ym3 = ym1 + r3*cos(t3);
    //torso
    double xm2 = xm1 + r2*sin(t2),            ym2 = ym1 + r2*cos(t2);
    //head
    double xm4 = xm2 + r4*sin(t4),            ym4 = ym2 + r4*cos(t4);
    //lower leg
    double xm5 = xm3 + r5*sin(t5),            ym5 = ym3 + r5*cos(t5);

    double COM_Y = (ym1*m1 + ym2*m2 + ym3*m3 + ym4*m4 + ym5*m5)/(m1+m2+m3+m4+m5); //calculate centre of mass

    //////////adapted movement variables/////////////
    double move_term=0;
    bool move_right=false;
    bool move_left=false;
    double theta_max_prev=thetastart;
    bool reached=false;
    double omega_prev=0;
    double theta_prev=0;
    double var=2;
    double speed=2*var/T0;
    //double dang=var*2*h/T0; //n steps = T0/2*h
    double speed_inst=0.0013;
    double dang=0;
    double theta_max=0;
    double term1lim=1;

    term1=term1lim;
    double speed_min=1.1*(2*term1lim)*w/pi;
    double speed_max=2*speed_min;
    double dang_min=speed_min*h;
    double dang_max=speed_max*h;
    double term1_prev=0;
    double start_ratio=-0.5;

    dang=3.5*dang_min;

    term1=-term1lim;

    ///////////////////////////////////////

    ///////////adapted movement variables end//////////////

    //// trapezium rule for acceleration
    //good as over an interval of h, acceleration will vary linearly
    double trap_prev=0;
    double trap_now=0;
    double area=0;

    //counting oscillations
    double oscillation=1;
    double oscillationlimit=21;
    double finalamplitude=0;

    double ratio_min=-1;
    double ratio_max=1;
    double drat=0.01;
    start_ratio=ratio_min;

    while ( start_ratio <= ratio_max ){

        ///reset parameters

        omega=0; //angular velocity
        a=0; //angular acceleration
        x=0; //x position
        y=0; //y position
        t=0; //time

        term1d=0;
        term1dd=0;

        thetastart=pi/64; //initial angle
        theta=thetastart;

        move_right=false;
        move_left=false;
        theta_max_prev=thetastart;
        reached=false;
        omega_prev=0;
        theta_prev=0;
        theta_max=0;

        term1_prev=0;

        term1=-term1lim;

        trap_prev=0;
        trap_now=0;
        area=0;

        //counting oscillations
        oscillation=1;
        finalamplitude=0;

    //loop for Runge Kutta calculation
    for(int n=0; n<=N; n++){

        //Calculates x, y and a
        x = XPosition(length, theta);
        y = YPosition(length, theta);
        a = omega_deriv(theta, t2, t2Dot, t2DDot, t3, t3Dot, t3DDot, t4, t4Dot, t4DDot, t5, t5Dot, t5DDot, omega);

        //joints
        x1 = XPosition(length,theta),    y1 = YPosition(length,theta);
        x3 = x1 + l3*sin(t3),            y3 = y1 + l3*cos(t3);
        x2 = x1 + l2*sin(t2),            y2 = y1 + l2*cos(t2);
        x4 = x2 + l4*sin(t4),            y4 = y2 + l4*cos(t4);
        x5 = x3 + l5*sin(t5),            y5 = y3 + l5*cos(t5);

        //COM
        //seat
        xm1 = XPosition(length,theta),    ym1 = YPosition(length,theta);
        //upper leg
        xm3 = x1 + r3*sin(t3),            ym3 = y1 + r3*cos(t3);
        //torso
        xm2 = x1 + r2*sin(t2),            ym2 = y1 + r2*cos(t2);
        //head
        xm4 = x2 + r4*sin(t4),            ym4 = y2 + r4*cos(t4);
        //lower leg
        xm5 = x3 + r5*sin(t5),            ym5 = y3 + r5*cos(t5);

        COM_Y = ym1 - (ym1*m1 + ym2*m2 + ym3*m3 + ym4*m4 + ym5*m5)/(m1+m2+m3+m4+m5);

        //for single run
        //outFile << t <<"\t"<< theta <<"\t"<< term1 << "\t" << theta_max << "\t" << theta_max_prev << "\t" << term1dd <<"\t"<< area << "\t" << omega << "\t" << COM_Y << "\n";
        //outFile << t <<"\t"<< x1<<"\t"<<y1<<"\t"<<x2<<"\t"<<y2<<"\t"<<x3<<"\t"<<y3<<"\t"<<x4<<"\t"<<y4<<"\t"<<x5<<"\t"<<y5<<"\n";
        //outFile << t << "\t" << theta << "\n";

        ///////////adapted movement parameters//////////////

        if(omega > 0){
            if( theta > -start_ratio*theta_max_prev){
                move_left = false;
                move_right = true;
            }
        }
        if(omega < 0){
            if( theta < -start_ratio*theta_max_prev){
                move_right = false;
                move_left = true;
            }
        }

        //check within limits
        if ( (right) && (term1 > term1lim) ){

            move_right=false;
        }
        if ( (left) && (term1 < -term1lim) ){

            move_left=false;
        }

        if( omega*omega_prev < 0 ){

            theta_max_prev=theta_max;
        }

        //if at zero, reset 'reached'
        if (theta*theta_prev < 0){

            reached = false;
            theta_max=0;
            if(oscillation == oscillationlimit){

                finalamplitude=theta_max_prev;
                outFile << start_ratio << "\t" << oscillation << "\t" << finalamplitude << "\t" << t << "\n";
                cout << start_ratio << "\t" << oscillation << "\t" << finalamplitude << "\t" << t << "\n";
                break;
            }

            oscillation++;
        }

        term1_prev=term1;

        //motion rotating right
        if (move_right){

            term1 += dang;
        }

        //motion rotating left
        if (move_left){

            term1 -= dang;
        }

        term1dd = (-((term1-term1_prev)/h)-term1d)/h; //acceleration of double flail rotation
        term1d = -(term1-term1_prev)/h; //speed of double flail rotation

        theta_prev=theta;
        omega_prev=omega;

        //update movement parameters
        t3=theta+1.57,                   t3Dot=omega,                    t3DDot=a;
        t2=theta-2.319-t2max-t2max*term1,   t2Dot=omega-t2max*term1d,       t2DDot=a-t2max*term1dd;
        t4=t2-0.0785-t4max*term1,        t4Dot=t2Dot-t4max*term1d,       t4DDot=t2DDot-t4max*term1dd;
        t5=t3-0.733-t5max*term1,         t5Dot=t3Dot-t5max*term1d,       t5DDot=t3DDot-t5max*term1dd;

        //step part 1
        ok1 = theta_deriv(omega);
        wk1 = omega_deriv(theta, t2, t2Dot, t2DDot, t3, t3Dot, t3DDot, t4, t4Dot, t4DDot, t5, t5Dot, t5DDot, omega);
        theta1= theta + ok1*(h/2);
        omega1 = omega + wk1*(h/2);

        //step part 2
        ok2 = theta_deriv(omega1);
        wk2 = omega_deriv(theta1, t2, t2Dot, t2DDot, t3, t3Dot, t3DDot, t4, t4Dot, t4DDot, t5, t5Dot, t5DDot, omega1);
        theta2 = theta + ok2*(h/2);
        omega2 = omega + wk2*(h/2);

        //step part 3
        ok3 = theta_deriv(omega2);
        wk3 = omega_deriv(theta2, t2, t2Dot, t2DDot, t3, t3Dot, t3DDot, t4, t4Dot, t4DDot, t5, t5Dot, t5DDot, omega2);
        theta3 = theta + ok3*(h);
        omega3 = omega + wk3*(h);

        //step part 4
        ok4 = theta_deriv(omega3);
        wk4 = omega_deriv(theta3, t2, t2Dot, t2DDot, t3, t3Dot, t3DDot, t4, t4Dot, t4DDot, t5, t5Dot, t5DDot, omega3);

        //increases theta and omega
        theta = theta + (ok1+2*ok2+2*ok3+ok4)*(h/6);
        omega = omega + (wk1+2*wk2+2*wk3+wk4)*(h/6);

        //calculates t after a whole step
        t += h;

        if (abs(theta) > abs(theta_max)){

            theta_max = theta;
        }

        ///trap rule
        trap_now=term1dd;
        area += (trap_prev+trap_now)*h;
        trap_prev=trap_now;
        ///
    }

    start_ratio += drat;
    }

    //user instructions
    printf ("Results have been output to a file called \"double_hinged_flail_sawtooth_cycle.txt\"\n");

    return 0;
}
