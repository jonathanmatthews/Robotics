import math

# Code originally written in C++ by the Numerical Modelling subgroup

# differential equations to be solved
def theta_deriv(length, length_deriv, theta, omega, t):
    return -omega


def omega_deriv(length, length_deriv, theta, omega, t, spin_accel, radius, w0):
    return spin_accel * radius * radius / (length * length + radius * radius) + w0 * w0 * math.sin(theta)


# function to calculate x position of mass
def XPosition(length, theta):
    return length * math.sin(theta)


# function to calculate y position of mass
def YPosition(length, theta):
    return length * math.cos(theta)


def NextVelocity(InitialPosition, InitialVelocity, Force, mass, length):
    # defining system parameters
    # combined mass of the two dumbbell masses
    m = mass
    # arbitrary time
    t = 0
    # velocity and position
    omega = InitialVelocity
    theta = InitialPosition

    # Runge Kutta parameters
    h = 0.01  # step size for Runge Kutta
    N = 2500  # number of intervals for Runge Kutta
    omega1 = 0
    omega2 = 0
    omega3 = 0  # omega at half interval in Runge Kutta calculation
    wk1 = 0
    wk2 = 0
    wk3 = 0
    wk4 = 0  # for omega
    theta1 = 0
    theta2 = 0
    theta3 = 0  # theta at half interval in Runge Kutta calculation
    ok1 = 0
    ok2 = 0
    ok3 = 0
    ok4 = 0  # for theta

    # paramenters for finding optimal frequency
    length_0 = length  # initial length (equilibrium)
    length_1 = length_0  # swing length
    length_deriv = 0

    spin_accel = 0
    radius = 0.1 * length_0

    w0 = (9.81 * length_0) / (length_0 * length_0 + radius * radius)

    # note force is thought of as the angular force (torque), constant throughout whole step
    spin_accel = Force / m

    # step part 1
    ok1 = theta_deriv(length_1, length_deriv, theta, omega, t)
    wk1 = omega_deriv(length_1, length_deriv, theta, omega, t, spin_accel, radius, w0)
    theta1 = theta + ok1 * (h / 2)
    omega1 = omega + wk1 * (h / 2)

    # step part 2
    ok2 = theta_deriv(length_1, length_deriv, theta1, omega1, t)
    wk2 = omega_deriv(length_1, length_deriv, theta1, omega1, t, spin_accel, radius, w0)
    theta2 = theta + ok2 * (h / 2)
    omega2 = omega + wk2 * (h / 2)

    # step part 3
    ok3 = theta_deriv(length_1, length_deriv, theta2, omega2, t)
    wk3 = omega_deriv(length_1, length_deriv, theta2, omega2, t, spin_accel, radius, w0)
    theta3 = theta + ok3 * (h)
    omega3 = omega + wk3 * (h)

    # step part 4
    ok4 = theta_deriv(length, length_deriv, theta3, omega3, t)
    wk4 = omega_deriv(length, length_deriv, theta3, omega3, t, spin_accel, radius, w0)

    # increases theta and omega
    theta = theta + (ok1 + 2 * ok2 + 2 * ok3 + ok4) * (h / 6)
    omega = omega + (wk1 + 2 * wk2 + 2 * wk3 + wk4) * (h / 6)

    return omega


def NextPosition(InitialPosition, InitialVelocity, Force, mass, length):
    # defining system parameters
    # combined mass of the two dumbbell masses
    m = mass
    # arbitrary time
    t = 0
    # velocity and position
    omega = InitialVelocity
    theta = InitialPosition

    # Runge Kutta parameters
    h = 0.01  # step size for Runge Kutta
    N = 2500  # number of intervals for Runge Kutta
    omega1 = 0
    omega2 = 0
    omega3 = 0  # omega at half interval in Runge Kutta calculation
    wk1 = 0
    wk2 = 0
    wk3 = 0
    wk4 = 0  # for omega
    theta1 = 0
    theta2 = 0
    theta3 = 0  # theta at half interval in Runge Kutta calculation
    ok1 = 0
    ok2 = 0
    ok3 = 0
    ok4 = 0  # for theta

    length_0 = length  # initial length (equilibrium)
    length_1 = length_0  # swing length
    length_deriv = 0

    spin_accel = Force / m  # note force is thought of as the angular force, constant force throughout whole step
    radius = 0.1 * length_0

    w0 = (9.81 * length_0) / (length_0 * length_0 + radius * radius)

    # step part 1
    ok1 = theta_deriv(length_1, length_deriv, theta, omega, t)
    wk1 = omega_deriv(length_1, length_deriv, theta, omega, t, spin_accel, radius, w0)
    theta1 = theta + ok1 * (h / 2)
    omega1 = omega + wk1 * (h / 2)

    # step part 2
    ok2 = theta_deriv(length_1, length_deriv, theta1, omega1, t)
    wk2 = omega_deriv(length_1, length_deriv, theta1, omega1, t, spin_accel, radius, w0)
    theta2 = theta + ok2 * (h / 2)
    omega2 = omega + wk2 * (h / 2)

    # step part 3
    ok3 = theta_deriv(length_1, length_deriv, theta2, omega2, t)
    wk3 = omega_deriv(length_1, length_deriv, theta2, omega2, t, spin_accel, radius, w0)
    theta3 = theta + ok3 * (h)
    omega3 = omega + wk3 * (h)

    # step part 4
    ok4 = theta_deriv(length_1, length_deriv, theta3, omega3, t)
    wk4 = omega_deriv(length_1, length_deriv, theta3, omega3, t, spin_accel, radius, w0)

    # increases theta and omega
    theta = theta + (ok1 + 2 * ok2 + 2 * ok3 + ok4) * (h / 6)
    omega = omega + (wk1 + 2 * wk2 + 2 * wk3 + wk4) * (h / 6)

    return theta