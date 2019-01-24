// Name: Max Hadfield
// Virtual Robot Model

//Note: we could not get this model to give out reasonable results, code is submitted to illustrate concept
//and show the work done on the model

#include <cmath>
#include <fstream>
#include <iomanip>
#include <string>
#include <vector>
#include <algorithm>
#include <Robot.h>
#include <iostream>

using namespace std;

//Differential equation for theta
inline double thetaDot(double omega)
{
    return omega;
}

//Differential equation for omega
inline double omegaDot(double l, double theta, double theta_dot, double phi, double phi_dot, double phi_double_dot, double r, double r_dot, double r_doubledot, double t, double gamma, double m1, double m2)
{
    double term1 = m2*sin(phi-theta)*(l*r*phi_dot*phi_dot - l*r*phi_dot*theta_dot - l*r_doubledot + l*r*theta_dot*phi);

    double term2 = m2*cos(phi-theta)*(l*r*phi_double_dot+2*l*r_dot*theta_dot);

    return (term1-term2)/(l*l*(m1+m2)) - 9.81*sin(theta)/l - 2*(m1+m2)*gamma*theta_dot;
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
    double theta=-0.0175; //initial angle = 10
    double omega = 0; //angular velocity
    const double l = 1.815; //swing length, cm
    double gamma = 0.00443; //viscous damping coefficient/2m
    const double m1 = 2.642; //mass of swing
    double t = 0; //time, s
    const double tMax = 180; //time simulation is run for, s
    double phi = 2*atan(1); //angle between swing and mass
    double phi_dot = 0; //angular velocity of mass around swing
    double phi_doubledot = 0; //angular acceleration of mass around swing
    double r = 1; //distance of mass from swing
    double r_dot = 0; //velocity of mass away from swing
    double r_doubledot = 0; //acceleration of mass away from swing
    bool isMovingForward=true; //true when robot is moving forwards

    //calculated values
    double a = 0; //angular acceleration of swing
    double x = 0; //x position of swing
    double y = 0; //y position of swing

    //Runge Kutta parameters
    double h = 0; //step size for Runge Kutta
    double N = 100000; //number of intervals for Runge Kutta
    double omega1 = 0, omega2 = 0, omega3 = 0; //omega at intervals in Runge Kutta calculation
    double wk1 = 0,wk2 = 0,wk3 = 0,wk4 = 0; // k values for omega
    double theta1 = 0, theta2 = 0, theta3 = 0; //theta at intervals in Runge Kutta calculation
    double ok1 = 0,ok2 = 0,ok3 = 0,ok4 = 0; // k values for theta
    double oError = 0, wError = 0; //errors on theta and omega
    bool loopbreaker=false; //bool sometimes used to end simulation loop

    //Robot variables
    double MassRobot=0; //mass of robot centre of mass
    double xRobot=0; //x position of robot centre of mass
    double yRobot=0; //y position of robot centre of mass
    double VxRobot=0; //x velocity of robot centre of mass
    double VyRobot=0; //y velocity of robot centre of mass
    double AxRobot=0; //x acceleration of robot centre of mass
    double AyRobot=0; //y acceleration of robot centre of mass

    //analysis variables
    double theta_max=0; //maximum value of theta

    double t_peak=0; //time swing is at peak
    double t_peak_2=0; //time swing was previously at peak
    double t_peak_tot=0; //total of times between peaks (used for average)
    double t_peak_count=0; //count of number of peak times measured (used for average)

    double TimePeriod=2.5; //time period of motion

    double t_centre=0; //time when the swing is at centre of motion
    double t_centre_2=0; //time swing was previously at centre
    double t_centre_tot=0; //total of times between peaks (used for average)
    double t_centre_count=0; //count of number of peak times measured (used for average)

    double t_swing=0; //time after which the robot should move

    double frequency=0.796088; //motion frequency
    double frequency_init=0; //initial value of movement frequency
    double frequency_max=3; //maximum value of movement frequency
    double frequency_step=0; //interval for movement frequency variation
    double frequency_noofsteps=1000; //number of steps used in movement frequency variation

    double analysis_time = 40; //time certain motions analyse swing motion for to determine natural frequency of pendulum
    double analysis_time_init=1; //initial analysis time
    double analysis_time_max=180; //maximum analysis time
    double analysis_time_step=0; //interval for analysis time variation
    double analysis_time_noofsteps=360; //number of steps used in analysis time variation

    //motion variables
    double theta_prev=0; //value of theta from previous time period
    double omega_previous=0; //value of omega from previous time period
    int peakindex=0; //index to determine when a peak has been passed

    double leg_speed=3; //angular velocity of leg motion

    double leg_speed_init=0; //initial angular velocity of leg motion
    double leg_speed_max=15; //final angular velocity of leg motion
    double leg_speed_step=0; //interval size which leg speed is increased with
    double leg_speed_noofsteps=100; // number of steps leg speed is increased by

    double offset_time = 0; //time certain motions were offset from the peak by
    double offset_time_init = -1; //initial offset time
    double offset_time_max = 1; //maximum offset time
    double offset_time_step = 0; //interval for offset time variation
    double offset_time_noofsteps=100; //number of steps used in offset time variation

    //Link output file
    string fileName = "controlled_double_pendulum_results.txt";
    ofstream outFile(fileName);
    string fileName2 = "leg_speed_variation_results.txt";
    ofstream outFile2(fileName2);
    string fileName3 = "GUI_Output.txt";
    ofstream outFile3(fileName3);

    //File headings
    outFile << "Time\tTheta\tLegAngle\tLegVelocity\tLegAcceleration\tMotionComplete\tTorsoAngle\tTorsoVelocity\tTorsoAcceleration\tTorsoMotionComplete\tOmega\tPhi\tr\tCOMX\tCOMY\tTibiaXVelocity" << endl;
    outFile2 << "leg_speed \tthetha+max" << endl;
    outFile3 << "Time \tTorso x\t Torso y \tHead x \tHead y \tArm x \tArm y \tThigh x \tThigh y \tTibia x \tTibia y \tFoot x \tFoot y\tRobot x \tRobot y" << endl;
    //outFile3 << "Time \tTorso x\t Torso y \tTibia x \tTibia y " << endl;

    //step size
    h = tMax/N;

    //offset_time_max = 100*h;
    leg_speed_step = (leg_speed_max-leg_speed_init)/leg_speed_noofsteps;
    analysis_time_step = (analysis_time_max-analysis_time_init)/analysis_time_noofsteps;
    offset_time_step = (offset_time_max-offset_time_init)/offset_time_noofsteps;
    frequency_step = (frequency_max-frequency_init)/frequency_noofsteps;

    //loops for stepwise variation of analysis time/leg_speed/offset_time/movement frequency

    //for(analysis_time=analysis_time_init; analysis_time<=analysis_time_max; analysis_time+=analysis_time_step){
    //for(leg_speed=leg_speed_init; leg_speed<=leg_speed_max; leg_speed+=leg_speed_step){
    //for(offset_time=offset_time_init; offset_time<=offset_time_max; offset_time+=offset_time_step){
    //for(frequency=frequency_init; frequency<=frequency_max; frequency+=frequency_step){

    theta = -0.0175*5;  //reset initial angle 5 degree
    omega = 0; //reset angular velocity

    //Creating robot and body parts
    Robot * weeBot = new Robot(TwoVector(0,0));
    BodyPart * torso = new BodyPart(weeBot,1.0496,-pi/2-0.97,0.2115);
    BodyPart * head = new BodyPart(torso,0.68375,0,0.11441);
    BodyPart * arm = new BodyPart(torso,1.15716,pi/2,0.2187);
    BodyPart * thigh = new BodyPart(weeBot,1.20004,0,0.1029);
    BodyPart * tibia = new BodyPart(thigh,0.60284,0,0.10);
    BodyPart * foot = new BodyPart(tibia,0.59186,-pi/4,0.04519);

    //adding body parts to robot
    weeBot->addBodyPart(torso);
    weeBot->addBodyPart(head);
    weeBot->addBodyPart(arm);
    weeBot->addBodyPart(thigh);
    weeBot->addBodyPart(tibia);
    weeBot->addBodyPart(foot);

    //set robot mass
    MassRobot=weeBot->getCOMMass();

    //loop for Runge Kutta calculation and robot movement
    while(loopbreaker==false){

        //get information from robot
        xRobot=weeBot->getCOMPosition().getX();
        yRobot=weeBot->getCOMPosition().getY();
        VxRobot=weeBot->getCOMVelocity().getX();
        VyRobot=weeBot->getCOMVelocity().getY();
        AxRobot=weeBot->getCOMAcceleration().getX();
        AyRobot=weeBot->getCOMAcceleration().getY();

        //calculate COM properties
        r=weeBot->getCOMPosition().absolute();
        phi=acos(yRobot/r);

        phi_dot=(VxRobot*cos(phi)+VyRobot*sin(phi))/r;
        r_dot=VxRobot*sin(phi)-VyRobot*cos(phi);

        phi_doubledot=(AxRobot*cos(phi)+AyRobot*sin(phi))/r;
        r_doubledot=AxRobot*sin(phi)-AyRobot*cos(phi);

        //OUTPUT
        outFile << t << "\t" << theta << "\t" << tibia->getAngle() << "\t" << tibia->getAngularVelocity() << "\t" << tibia->getAngularAcceleration() << "\t" << tibia->getMotionCompete() << "\t" << torso->getAngle() << "\t" << torso->getAngularVelocity() << "\t" << torso->getAngularAcceleration() << "\t" << torso->getMotionCompete() << "\t"  << omega << "\t" << phi << "\t" << r << "\t" << weeBot->getCOMPosition().getX() << "\t" << weeBot->getCOMPosition().getY() << "\t" << tibia->getVelocity().getX() << endl;

        //Calculates x, y and a
        x = xPos(l, theta);
        y = yPos(l, theta);
        a = omegaDot(l, theta, omega, phi, phi_dot, phi_doubledot, r, r_dot, r_doubledot, t, gamma, m1, MassRobot);

        //Output for GUI
        outFile3 << t << "\t"
                         << torso->getPosition().getX() << "\t" << torso->getPosition().getY() << "\t"
                         << head->getPosition().getX() << "\t" << head->getPosition().getY() << "\t"
                         << arm->getPosition().getX() << "\t" << arm->getPosition().getY() << "\t"
                         << thigh->getPosition().getX() << "\t" << thigh->getPosition().getY() << "\t"
                         << tibia->getPosition().getX() << "\t" << tibia->getPosition().getY()
                         << "\t" << foot->getPosition().getX() << "\t" << foot->getPosition().getY() << "\t"
                         << weeBot->getPosition().getX() << "\t" << weeBot->getPosition().getY()
                         << endl;


        //calculates t, theta and omega after half a step

        //step part 1
        ok1 = thetaDot(omega);
        wk1 = omegaDot(l, theta, omega, phi, phi_dot, phi_doubledot, r, r_dot, r_doubledot, t, gamma, m1, MassRobot);
        theta1= theta + ok1 * (h/2);
        omega1 = omega + wk1 * (h/2);

        //step part 2
        ok2 = thetaDot(omega1);
        wk2 = omegaDot(l, theta1, omega1, phi, phi_dot, phi_doubledot, r, r_dot, r_doubledot, t, gamma, m1, MassRobot);
        theta2 = theta + ok2 * (h/2);
        omega2 = omega + wk2 * (h/2);

        //step part 3
        ok3 = thetaDot(omega2);
        wk3 = omegaDot(l, theta2, omega2, phi, phi_dot, phi_doubledot, r, r_dot, r_doubledot, t, gamma, m1, MassRobot);
        theta3 = theta + ok3 * (h);
        omega3 = omega + wk3 * (h);

        //step part 4
        ok4 = thetaDot(omega3);
        wk4 = omegaDot(l, theta3, omega3, phi, phi_dot, phi_doubledot, r, r_dot, r_doubledot, t, gamma, m1, MassRobot);

        //calculates new values of theta and omega
        theta += (ok1 + 2*ok2 + 2*ok3 + ok4) * (h/6);
        omega += (wk1 + 2*wk2 + 2*wk3 + wk4) * (h/6);

        //calculates errors on theta and omega
        wError += (8.0/15.0) * pow((wk3 -wk2), 3.0) * 1/(pow((wk4-wk1),2.0));
        oError += (8.0/15.0) * pow((ok3 -ok2), 3.0) * 1/(pow((ok4-ok1),2.0));

        if(theta*theta_prev < 0){t_centre_count++;}

        //Movement when robot goes past peak
        /*

        //uncomment to make robot move when it detects it has passed a swing peak

        //loop to detect when omega == 0
        if(omega*omega_previous <= 0){

            tibia->setMotionComplete(false);
            torso->setMotionComplete(false);

            if(theta<0){

                isMovingForward=true;

            }

            if(theta>0){

                isMovingForward=false;

            }

            t_peak=t;
        }
        */


        //movement at natural frequency of pendulum (peak)
        /*
        //uncomment for robot to analyse the natural frequency of the pendulum (judged from the swing peaks)
        //and to then move at this frequency

        if(t<analysis_time){

            if(omega*omega_previous <= 0){

                t_peak_2 = t_peak;
                t_peak = t;
                t_peak_tot += (t_peak-t_peak_2);
                t_peak_count++;
                frequency = t_peak_count/(2*t_peak_tot);

            }
        }

        else{

            if(omega*omega_previous <= 0 && peakindex==0){t_peak=t;}

            if(t>t_peak+peakindex*(1/(4*frequency))){

                tibia->setMotionComplete(false);
                torso->setMotionComplete(false);

                if(theta<0){

                    isMovingForward=true;

                }

                if(theta>0){

                    isMovingForward=false;

                }

                peakindex++;

            }

        }

        */

        //movement at natural frequency of pendulum (centre)
        /*
        //uncomment for robot to analyse the natural frequency of the pendulum (judged from the swing peaks)
        //and to then move at this frequency

        if(t<=analysis_time){

            if(theta*theta_prev < 0){

                t_centre_2 = t_centre;
                t_centre = t;
                t_centre_tot += (t_centre-t_centre_2);
                //t_centre_count++;
                frequency = t_centre_count/(2*t_centre_tot);
                TimePeriod=(2*t_centre_tot)/t_centre_count;

                //cout << TimePeriod << endl;

            }
        }

        else{

            if(theta*theta_prev < 0 && peakindex==0 ){
                t_centre=t;
                t_swing=t+TimePeriod/4;

                if(omega<0){isMovingForward=false;}
                if(omega>0){isMovingForward=true;}

                peakindex++;
            }

            if(t>t_swing){

                tibia->setMotionComplete(false);
                torso->setMotionComplete(false);

                if(isMovingForward==true){isMovingForward=false;}
                else {isMovingForward=true;}

                t_swing+=TimePeriod/2;

            }
        }
            //if(t<=(t_centre + (1/(2*frequency))) && t+h > (t_centre + (1/(2*frequency)))){
            //if(t<=(t_centre + (1/(2*frequency))) && t+offset_time > (t_peak + (1/(2*frequency)))){
            //if(t>t_centre+peakindex*(1/(8*frequency))){
            /*
            if(t>t_centre+TimePeriod/4){

                tibia->setMotionComplete(false);
                torso->setMotionComplete(false);

                peakindex++;

                t_centre+=TimePeriod/2;

            }

        }

        */

        //movement at preset frequency
        /*
        //uncomment to make the robot move at a constant preset frequency

        if(theta*theta_prev < 0 && peakindex==0){t_centre=t;}

        //if(t<=(t_centre + (1/(2*frequency))) && t+h > (t_centre + (1/(2*frequency)))){
        //if(t<=(t_centre + (1/(2*frequency))) && t+offset_time > (t_peak + (1/(2*frequency)))){
        //if(t>t_centre+peakindex*(1/(2*frequency))){
        if(t>t_centre+TimePeriod/4){

            tibia->setMotionComplete(false);
            torso->setMotionComplete(false);
            //head->setMotionComplete(false);

            if(theta<0){

                isMovingForward=true;

            }

            if(theta>0){

                isMovingForward=false;

            }

            peakindex++;
            t_centre+=TimePeriod;


        }

        */

        //movement at preset time period

        /*

        //uncomment to make the robot move with a constant preset time period


        if(theta*theta_prev < 0 && peakindex==0 ){
            t_centre=t;
            t_swing=t+TimePeriod/4;

            if(omega<0){isMovingForward=false;}
            if(omega>0){isMovingForward=true;}

            peakindex++;
        }

        if(t>t_swing && t_swing!=0){

            tibia->setMotionComplete(false);
            torso->setMotionComplete(false);

            if(isMovingForward==true){isMovingForward=false;}
            else {isMovingForward=true;}

            t_swing+=TimePeriod/2;

        }

        /**/

        //move commands
        tibia->move(0,pi/2,leg_speed,h,isMovingForward);
        torso->move((-pi/2-0.51),(-pi/2-0.97),leg_speed*((0.46)/(pi/2)),h,isMovingForward);

        //determine max value of theta
        if(t>tMax*0.5&&theta>theta_max){theta_max=theta;}

        //condition to end simulation loop

        //if(t_centre_count>=150){
        //if(t>tMax&&omega*omega_previous <= 0){
        if(t>=tMax){
            loopbreaker=true;
        }

        //assign previous values of theta and omega
        theta_prev = theta;
        omega_previous = omega;

        //update t
        t+=h;

        cout << t << endl;

        //getchar();

    }


    //output for stepwise variation of parameters (uncomment relevant one)

    //outFile2 << frequency << "\t" << theta_max << endl;
    //outFile2 << leg_speed << "\t" << theta_max << endl;
    outFile2 << analysis_time << "\t" << theta_max << endl;
    //outFile2 << offset_time << "\t" << theta_max << endl;

    //cout << frequency << endl;
    //cout << leg_speed << endl;
    //cout << theta_max << endl;
    cout << analysis_time << endl;
    //cout << t_peak_count << endl;
    //cout << analysis_time << endl;
    //cout << offset_time << endl;

    //reset parameters

    t=0;
    theta_max=0;
    t_peak=0;
    t_peak_2=0;
    t_peak_count=0;
    t_peak_tot=0;
    peakindex=0;
    frequency=0;
    t_centre=0;
    t_centre_2=0;
    t_centre_count=0;
    t_centre_tot=0;
    loopbreaker=false;
    theta_prev=0;
    omega_previous=0;


    delete weeBot;

    //uncomment "{" to use stepwise parameter variation loops
    //}

    //user instructions
    printf ("Results have been output to a file called '%s'\n",fileName.c_str());

    if(theta_max>0){
    cout << "Maximum angle is " << theta_max*360/(2*pi) << " degrees" << endl;
    }

    return 0;
}
