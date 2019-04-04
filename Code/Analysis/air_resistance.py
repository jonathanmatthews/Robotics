import numpy as np

rod1 = 1.2
rod2 = 0.3
rod3 = 0.2
bar_width = 0.5
bar_thickness = 0.02
seat_thickness = 0.02
rod_thickness = 0.02

def thickness(y):
    if -rod1 < y <= 0:
        area_y = rod_thickness
    elif -(rod1 + rod2) < y <= -rod1:
        area_y = rod_thickness
    elif -(rod1 + rod2) - bar_thickness < y <= -(rod1 + rod2):
        area_y = bar_width  
    elif -(rod1 + rod2 + rod3) < y <= -(rod1 + rod2) - bar_thickness:
        area_y = rod_thickness
    elif -(rod1 + rod2 + rod3) - seat_thickness < y <= -(rod1 + rod2 + rod3):
        area_y = bar_width
    else:
        print 'y out of bounds: {:.2f}'.format(y)
        area_y = 0
    return area_y

def velocity(angular_velocity, y):
    if y == 0.0:
        return 0.0
    else:
        return angular_velocity/np.abs(y) * np.pi/180

def relative_cross_section(angular_velocity):
    dy = 0.005
    rod = np.arange(-2.0, 0.0, dy)
    cross_sections = [dy * velocity(angular_velocity, y)**2 * thickness(y) for y in rod]
    return np.sum(cross_sections)

def horizontal_cross_section():
    dy = 0.005
    rod = np.arange(-2.0, 0.0, dy)
    cross_sections = [dy * thickness(y) for y in rod]
    return np.sum(cross_sections)

def drag_force(angular_velocity, p = 1.225, c_d = 1.05):
    return 0.5 * p * relative_cross_section(angular_velocity) * c_d

print horizontal_cross_section()
print 'Drag force : {:.3f} N'.format(drag_force(30.0))
print 'Drag force per unit angular velocity: {:.3f} N'.format(drag_force(1.0)/(0.5 * 1.225 * 1.05))

