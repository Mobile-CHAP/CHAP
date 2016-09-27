import math as m
            
def polar(x,y):
    """
    Find distance to user input location in radians and hypotenuse.

    @type  x: int
    @param x: X-axis input from user control joystick (1.0 <-> -1.0).
    
    @type  y: int
    @param y: Y-axis input from user control joystick (1.0 <-> -1.0).
    
    @rtype:   float,float
    @return:  mag (hypotenuse to destination, minimum value is 1) and ta (radians to destination)
    """
    
    vmax= 464;
    
    ta= m.atan2(y, x)
    ta= ta-1.5708
    
    mag= m.sqrt((x*x)+(y*y))
    mag = 1 if mag > 1 else mag
    mag= mag*vmax
    
    return mag, ta

def velocity(mag, ta):
    """
    Calculate required wheel velocitys to move towards given values.

    @type  mag: float
    @param mag: Hypotenuse to destination.
    
    @type  ta: float
    @param ta: Radians to destination.
    
    @rtype:   int,int,int
    @return:  v1 (velocity for front right),v2 (velocity for front left),v3 (velocity for rear).
    """

    # Distance from wheel to center.
    
    a = 0.4636484611    # Wheel 1 (front right).
    b = 2.6779476831    # Wheel 2 (front left).
    c = 4.71239         # Wheel 3 (front rear).
                        # Note: values are in radians. 
                        # Center line is perpendicular to front of base.
    
    v1 = mag*m.cos(a-ta)
    v2 = mag*m.cos(b-ta)
    v3 = mag*m.cos(c-ta)
	
    return int(v1), int(v2), int(v3)