// Name: Max Hadfield
// Date: 21/03/2017
// Simulation and movement analysis of the Hinged Flail model using 4th order Runge Kutta. This program was used to generate
// the movement analysis of the single which was included in the report

#include <cmath>
#include <fstream>
#include <iomanip>
#include <string>
#include <iostream>
using namespace std;

//Differential equation for theta
inline double thetaDot(double omega)
{   //Change ODE here
    return omega;
}


//Differential equation for omega
inline double omegaDot(double r, double theta, double omega, double gamma, double m2, double m3, double M, double l2, double l3, double t2, double t2Dot, double t2DDot, double t3, double t3Dot, double t3DDot)
{   //Change ODE here
    return (-m2*l2*(t2DDot*cos(theta-t2)+t2Dot*t2Dot*sin(theta-t2))-m3*l3*(t3DDot*cos(theta-t3)+t3Dot*t3Dot*sin(theta-t3))-M*9.81*sin(theta))/M*r - 2*gamma*omega;
}

//function to calculate x position of mass
inline double xPos(double l, double theta)
{
    return l * sin(theta);
}

//function to calculate y position of mass
inline double yPos(double l, double theta)
{
    return l * cos(theta);
}


int main()
{
    //declare variables

    //constants
    const double pi = atan(1)*4;

    //inital conditions
    double theta=-0.175; //initial angle = -10
    double omega = 0; //angular velocity
    double r = 1.815; //swing length, m
    double gamma = 0.00443; //viscous damping coefficient/2m
    double t = 0; //time, s
    double tMax = 600; //time simulation is run for, s
    double m1 = 3.842; //thigh + swing
    double m2 = 2.89051; //torso + head + arm
    double m3 = 1.1947; //leg + foot
    double M = m1 + m2 + m3; //total mass
    double l2 = 0.17121; //torso+head
    double l3 = 0.1406; //legs

    double t2=3.92699; //theta 2 (see Single Flail diagram in report)
    double t2Dot=0; //angular velocity of theta 2
    double t2DDot=0; // angular accelerationof theta 2
    double t2Range=pi/4; //range of motion of t2 45 degrees
    double t2Centre= 3.92699; //centre of motion of t2 225 degrees

    t2=t2Centre-t2Range; //set initial t2

    double t3=pi/4; //theta 3 (see Single Flail diagram in report)
    double t3Dot=0; //angular velocity of theta 3
    double t3DDot=0; // angular accelerationof theta 3
    double t3Range=pi/4; //range of motion of t3 45 degrees
    double t3Centre=pi/4; //centre of motion of t3 225 degrees

    t3=t3Centre-t3Range; //set initial t3

    //Runge Kutta parameters
    double h = 0; //step size for Runge Kutta
    double N = 200000; //number of intervals for Runge Kutta
    //double N = 100000*600/300; //number of intervals for Runge Kutta
    double omega1 = 0, omega2 = 0, omega3 = 0; //omega at intervals in Runge Kutta calculation
    double wk1 = 0,wk2 = 0,wk3 = 0,wk4 = 0; // k values for omega
     double theta1 = 0, theta2 = 0, theta3 = 0; //theta at intervals in Runge Kutta calculation
    double ok1 = 0,ok2 = 0,ok3 = 0,ok4 = 0; // k values for theta
    double oError = 0, wError = 0; //errors on theta and omega

    //movement variables

    double w=2; //0.796088

    bool t2MotionComplete=true; //true when angle is at final value
    bool t3MotionComplete=true; //true when angle is at final value
    bool MovingForward=true; //true when robot is moving forward

    double t2accelcomplete=0; //angle range over which the t2 accelerated
    double t3accelcomplete=0; //angle range over which the t3 accelerated

    double leg_speed=3; //maximum movement speed in rad/s
    double accel=0; //value of angular acceleration the joints can produce
    double TimePeriod=3; //Time period of motion

    double t_centre=0; //time when the swing is at centre of motion
    double t_swing=0; //time after which the robot should move
    double peakindex=0; //index to determine when a peak has been passed

    //analysis variables
    double theta_max = 0; //maximum swing angle achieved

    double theta_previous=0; //value of theta in previous time step
    double omega_previous=0; //value of omega in previous time step

    double w_init=0; //initial value of movement frequency
    double w_max=3; //maximum value of movement frequency
    double w_step=0; //interval for movement frequency variation
    double w_noofsteps=750; //number of steps used in movement frequency variation

    double range_init=0; //initial value of movement range
    double range_max=pi/2; //maximum value of movement range
    double range_step=0; //interval for movement range variation
    double range_noofsteps=500; //number of steps used in movement frequency variation

    w_step = (w_max-w_init)/w_noofsteps; //set movement frequency interval
    range_step = (range_max-range_init)/range_noofsteps; //set movement range interval

    //Link output files
    string fileName = "Hinged_Flail_results.txt";
    ofstream outFile(fileName);
    string fileName2 = "w_variation_results.txt";
    ofstream outFile2(fileName2);

    //File headings
    outFile << "Time \tTheta \tT2 \tT2Dot \tT2DDot \tT3 \tT3Dot \tT3DDot \tMovingForward \tMotionComplete \tOmega" << endl;
    outFile2 << "w \ttheta_max" << endl;

    //step size
    h = tMax/N;

    //loops for stepwise variation of movement range and frequency, uncomment here and the "}" on line 478 to use
    //for(w=w_init; w<=w_max; w+=w_step){
    //for(t2Range=range_init; t2Range<=range_max; t2Range+=range_step){

        t3Range = t2Range; //comment out to have different ranges of motion for each angle
        TimePeriod=1/(w); //comment out to set time period manually

        //loop for Runge Kutta calculation
        for(int n = 0; n <= N; n++){

            //outputs t, theta, x, y and omega to file
            outFile << t << "\t" << theta << "\t" << t2 << "\t" << t2Dot<< "\t" << t2DDot << "\t" << t3 << "\t" << t3Dot<< "\t" << t3DDot << "\t" << MovingForward << "\t" << t2MotionComplete << "\t" << omega << endl;

            //calculates t, theta and omega after half a step

            //step part 1
            ok1 = thetaDot(omega);
            wk1 = omegaDot(r, theta, omega, gamma, m2, m3, M, l2, l3, t2, t2Dot, t2DDot, t3, t3Dot, t3DDot);

            theta1= theta + ok1 * (h/2);
            omega1 = omega + wk1 * (h/2);

            //step part 2
            ok2 = thetaDot(omega1);
            wk2 = omegaDot(r, theta1, omega1, gamma, m2, m3, M, l2, l3, t2, t2Dot, t2DDot, t3, t3Dot, t3DDot);
            theta2 = theta + ok2 * (h/2);
            omega2 = omega + wk2 * (h/2);

            //step part 3
            ok3 = thetaDot(omega2);
            wk3 = omegaDot(r, theta2, omega2, gamma, m2, m3, M, l2, l3, t2, t2Dot, t2DDot, t3, t3Dot, t3DDot);
            theta3 = theta + ok3 * (h);
            omega3 = omega + wk3 * (h);

            //step part 4
            ok4 = thetaDot(omega3);
            wk4 = omegaDot(r, theta3, omega3, gamma, m2, m3, M, l2, l3, t2, t2Dot, t2DDot, t3, t3Dot, t3DDot);;

            //calculates new values of theta and omega
            theta += (ok1 + 2*ok2 + 2*ok3 + ok4) * (h/6);
            omega += (wk1 + 2*wk2 + 2*wk3 + wk4) * (h/6);

            //calculates errors on theta and omega
            wError += (8.0/15.0) * pow((wk3 -wk2), 3.0) * 1/(pow((wk4-wk1),2.0));
            oError += (8.0/15.0) * pow((ok3 -ok2), 3.0) * 1/(pow((ok4-ok1),2.0));

            //Movement function

            //Sinusoidal Movement

            //Uncomment for sinusoidal motion between minimum and maximum angle
            /*
            t2 = t2Centre + t2Range*sin(w*t);
            t2Dot = t2Range*w*cos(w*t);
            t2DDot = -t2Range*w*w*sin(w*t);

            t3 = t3Centre + t3Range*sin(w*t);
            t3Dot = t3Range*w*cos(w*t);
            t3DDot = -t3Range*w*w*sin(w*t);
            */

            //Step function

            //Uncomment for step function motion between minimum and maximum angle


            //loop to start motion at a swing peak
            if(theta*theta_previous < 0 && peakindex==0 ){

                t_centre=t;
                t_swing=t+TimePeriod/4;

                if(omega<0){MovingForward=false;}
                if(omega>0){MovingForward=true;}

                peakindex++;

            }

            //loop to move robot at preset time period

            if(t>t_swing && t_swing!=0){

                t2MotionComplete=false;
                t3MotionComplete=false;
                t_swing+=TimePeriod/2;


                if(omega<0){MovingForward=false;}
                if(omega>0){MovingForward=true;}

                if(t2>t2Centre){MovingForward=false;}
                if(t2<t2Centre){MovingForward=true;}

            }

            //Step function loop
            if(t2MotionComplete==false){

                if(MovingForward==true){

                    if(t2<t2Centre+t2Range){

                        accel=leg_speed/0.25;

                        //Accelerates robot if t2 is less than halfway through its motion
                        //and has speed lower than its max speed

                        if(t2Dot<leg_speed&&t2<t2Centre){

                            t2DDot=accel;
                            t2Dot+=accel*h;
                            t2+=t2Dot*h;
                            t2accelcomplete=t2;
                        }

                        //Decelerates robot when t2 is near the peak

                        else{

                            if(t2>=(t2Centre+t2Range)-0.85*(t2accelcomplete-(t2Centre-t2Range))){

                                t2DDot=-accel;
                                t2Dot+=t2DDot*h;
                                t2+=t2Dot*h;

                            }

                            else{

                                t2DDot=0;
                                t2+=t2Dot*h;
                            }
                        }

                    }

                    //prevents robot from moving past maximum value

                    else{

                        t2Dot=0;
                        t2DDot=0;
                        t2MotionComplete=true;

                    }

                }

                if(MovingForward==false){

                    if(t2>t2Centre-t2Range){

                        accel=-leg_speed/0.25;

                        //Accelerates robot if t2 is less than halfway through its motion
                        //and has speed lower than its max speed

                        if(t2Dot>-leg_speed&&t2>t2Centre){

                            t2DDot=accel;
                            t2Dot+=accel*h;
                            t2+=t2Dot*h;
                            t2accelcomplete=t2;
                        }

                        //Decelerates robot when t2 is near the peak

                        else{

                            if(t2<=(t2Centre-t2Range)-0.7*(t2accelcomplete-(t2Centre+t2Range))){

                                t2DDot=-accel;
                                t2Dot+=t2DDot*h;
                                t2+=t2Dot*h;

                            }

                            else{

                                t2DDot=0;
                                t2+=t2Dot*h;
                            }
                        }
                    }

                    else{

                        t2Dot=0;
                        t2DDot=0;
                        t2MotionComplete=true;

                    }
                }

            }

            //prevents robot from moving past maximum value

            else{

                t2Dot=0;
                t2DDot=0;

            }

            //Step function t3 (same as for t2)
            if(t3MotionComplete==false){

                if(MovingForward==true){

                    if(t3<t3Centre+t3Range){

                        accel=leg_speed/0.25;

                        if(t3Dot<leg_speed&&t3<t3Centre){

                            t3DDot=accel;
                            t3Dot+=accel*h;
                            t3+=t3Dot*h;
                            t3accelcomplete=t3;
                        }

                        else{

                            if(t3>=(t3Centre+t3Range)-0.7*(t3accelcomplete-(t3Centre-t3Range))){

                                t3DDot=-accel;
                                t3Dot+=t3DDot*h;
                                t3+=t3Dot*h;

                            }

                            else{

                                t3DDot=0;
                                t3+=t3Dot*h;
                            }
                        }

                    }

                    else{

                        t3Dot=0;
                        t3DDot=0;
                        t3MotionComplete=true;

                    }

                }

                if(MovingForward==false){

                    if(t3>t3Centre-t3Range){

                        accel=-leg_speed/0.25;

                        if(t3Dot>-leg_speed&&t3>t3Centre){

                            t3DDot=accel;
                            t3Dot+=accel*h;
                            t3+=t3Dot*h;
                            t3accelcomplete=t3;
                        }

                        else{

                            if(t3<=(t3Centre-t3Range)-0.75*(t3accelcomplete-(t3Centre+t3Range))){

                                t3DDot=-accel;
                                t3Dot+=t3DDot*h;
                                t3+=t3Dot*h;

                            }

                            else{

                                t3DDot=0;
                                t3+=t3Dot*h;
                            }
                        }
                    }


                    else{

                        t3Dot=0;
                        t3DDot=0;
                        t3MotionComplete=true;

                    }
                }

            }

            else{

                t3Dot=0;
                t3DDot=0;

            }
            //End of step function


            //calculate maximum swing angle achieved
            if(t>tMax*0.8&&abs(theta)>theta_max){theta_max=abs(theta);}

            //calculates t after a whole step
            t = t+h;

            //sets previous values of theta and omega
            theta_previous=theta;
            omega_previous=omega;
        }

        //output results
        //outFile2 << t2Range << "\t" << theta_max << endl;
        //cout << t2Range << endl;


        //reset parameters
        t=0;
        theta = -0.175;
        omega = 0;
        theta_max=0;

        t2=3.92699;
        t2Dot=0;
        t2DDot=0;

        t3=0;
        t3Dot=0;
        t3DDot=0;

        t2accelcomplete=0;
        t3accelcomplete=0;
        t_swing=0;
        peakindex=0;

    //uncomment "{" when using movement frequency or range variation loops
    //}

    //user instructions
    printf ("Results have been output to a file called '%s'\n",fileName.c_str());

    return 0;
}
