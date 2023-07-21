# Pinouts for Turtle Robot board 2.1 and 2.2
# Ver 20200304
# Ver 20210515  allow for reversing turtle orientation

import math
import time
import calibration
from collections import namedtuple

_x = 0
_y = 0
_heading = 0
frac_error = 0
spacer = ''
DEBUG = True

class led_var:
    _value = False
    def __init__(self, name, value = False):
        self.name = name
        self._value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        print(f"{self.name} = {self._value}")
        self._value = value

class rgb_led(list):
    brightness = None

leftLED = led_var("leftLED")
rightLED = led_var("rightLED")
leftDetector = led_var("leftDetector", 5001)
rightDetector = led_var("rightDetector", 5001)
emitter = led_var("emitter")
rgbLED = rgb_led([0])

def setDebug(val):
    global DEBUG
    DEBUG = val


def step(distance):
    steps = distance * calibration.steps_rev/(calibration.wheel_dia * math.pi)
    frac = steps-int(steps)
    if frac > 0.5:
        return int(steps + 1), 1 - frac
    else:
        return int(steps), -frac


def forward(distance):
    global _x, _y, _heading
    steps, frac = step(distance)
    if DEBUG:
        print("%sforward(%s)" % (spacer, distance))

    # new point
    deltax = distance * math.cos(math.radians(_heading))
    deltay = distance * math.sin(math.radians(_heading))
    _x = _x + deltax
    _y = _y + deltay


def backward(distance):
    global _x, _y, _heading
    steps, frac = step(distance)
    if DEBUG:
        print("%sbackward(%s)" % (spacer, distance))

    # new point
    deltax = distance * math.cos(math.radians(_heading - 180))
    deltay = distance * math.sin(math.radians(_heading - 180))
    _x = _x + deltax
    _y = _y + deltay


def left(degrees):
    global _x, _y, _heading, frac_error
    if (degrees < 0):
        right(-degrees)
    else:
        if DEBUG:
            print("%sleft(%s)" % (spacer, degrees))
        rotation = degrees / 360.0
        distance = calibration.wheel_base * math.pi * rotation
        steps, frac = step(distance)
        frac_error += frac

        _heading = _heading + degrees
        while _heading > 360:
            _heading = _heading - 360
        if False:
            print("steps=%s, frac_error=%s" % (steps, frac_error))


def right(degrees):
    global _x, _y, _heading
    if (degrees < 0):
        left(-degrees)
    else:
        if DEBUG:
            print("%sright(%s)" % (spacer, degrees))
        rotation = degrees / 360.0
        distance = calibration.wheel_base * math.pi * rotation
        steps, frac = step(distance)
        _heading = _heading - degrees
        while _heading < 0:
            _heading = _heading + 360


def penup():
    if DEBUG:
        print("penup()")

def pendown():
    if DEBUG:
        print("pendown()")

def done():
    if DEBUG:
        print("done()")

def goto(x, y):
    global spacer
    spacer = '    '  # offsets debug statements after "goto(x, y)"
    center_x, center_y = position()
    bearing = getBearing(x, y, center_x, center_y)
    trnRight = heading() - bearing
    if DEBUG:
        print("goto(%s, %s)" % (x, y))
    if abs(trnRight) > 180:
        if trnRight >= 0:
            left(360 - trnRight)
            # if DEBUG: print('left(%s)' % (360 - trnRight))
        else:
            right(360 + trnRight)
            # if DEBUG: print('right(%s)' % (360 + trnRight))
    else:
        if trnRight >= 0:
            right(trnRight)
            # if DEBUG: print('right(%s)' % trnRight)
        else:
            left(-trnRight)
            # if DEBUG: print('left(%s)' % -trnRight)
    dist = distance(tuple(position()), (x, y))
    forward(dist)
    spacer = ''


def setheading(to_angle):
    '''
    Set the orientation of the turtle to to_angle.

    Aliases:  setheading | seth

    Argument:
    to_angle -- a number (integer or float)

    Set the orientation of the turtle to to_angle.
    Here are some common directions in degrees:

     standard - mode:          logo-mode:
    -------------------|--------------------
       0 - east                0 - north
      90 - north              90 - east
     180 - west              180 - south
     270 - south             270 - west

    Example:
    >>> setheading(90)
    >>> heading()
    90
    '''

    cur_heading = heading()
    if (to_angle - cur_heading) < 0:
        if (to_angle - cur_heading) > -180:
            left(to_angle - cur_heading)
            if DEBUG: print("Case 1 left(%s)" % (to_angle - cur_heading))
        else:
            left(to_angle - cur_heading + 360)
            if DEBUG: print("Case 2 left(%s)" % (to_angle - cur_heading + 360))
    else:
        if (to_angle - cur_heading) > 180:
            left(360 - to_angle - cur_heading - 180)
            if DEBUG: print("Case 3 left(%s)" % (360 - to_angle - cur_heading))
        else:
            left(to_angle - cur_heading)
            if DEBUG: print("Case 4 left(%s)" % (to_angle - cur_heading))


def pensize(size):
    print('pensize() is not implemented in Turtle Robot')
    pass


def pencolor(color):
    print('pencolor() is not implemented in Turtle Robot')
    pass


def speed(x):
    print('speed() is not implemented in Turtle Robot')
    pass

def shape(x):
    print('shape() is not implemented in Turtle Robot')
    pass


def position():
    return _x, _y


def heading():
    return _heading

def distance(pointA, pointB):
    return abs((pointB[0] - pointA[0])**2 + (pointB[1] - pointA[1])**2)**0.5

def getBearing2(x, y, center_x, center_y):
    angle = math.degrees(math.atan2(y - center_y, x - center_x))
    return 90 - angle

def getBearing(x, y, center_x, center_y):
    # https://stackoverflow.com/questions/5058617/bearing-between-two-points
    angle = math.degrees(math.atan2(y - center_y, x - center_x))
    bearing = (angle + 360) % 360
    return bearing


def circle(radius, extent=None, steps=None):
    """ Draw a circle with given radius.

    Arguments:
    radius -- a number
    extent (optional) -- a number
    steps (optional) -- an integer

    Draw a circle with given radius. The center is radius units left
    of the turtle; extent - an angle - determines which part of the
    circle is drawn. If extent is not given, draw the entire circle.
    If extent is not a full circle, one endpoint of the arc is the
    current pen position. Draw the arc in counterclockwise direction
    if radius is positive, otherwise in clockwise direction. Finally
    the direction of the turtle is changed by the amount of extent.

    As the circle is approximated by an inscribed regular polygon,
    steps determines the number of steps to use. If not given,
    it will be calculated automatically. Maybe used to draw regular
    polygons.

    call: circle(radius)                  # full circle
    --or: circle(radius, extent)          # arc
    --or: circle(radius, extent, steps)
    --or: circle(radius, steps=6)         # 6-sided polygon

    Example (for a Turtle instance named turtle):
    >>> turtle.circle(50)
    >>> turtle.circle(120, 180)  # semicircle
    """

    if extent is None:
        extent = 360
    if steps is None:
        frac = abs(extent)/360
        # print("frac = %s" % frac)
        steps = 1+int(min(11+abs(radius)/6.0, 59.0)*frac)
    w = 1.0 * extent / steps
    w2 = 0.5 * w
    length = 2.0 * radius * math.sin(w2*math.pi/180.0)
    if radius < 0:
        length, w, w2 = -length, -w, -w2
    if DEBUG:
        print("circle(%s, extent=%s, steps=%s)" % (radius, extent, steps))
    if False:
        print("length (step length) = %s" % length)
        print("w (turn angle)= %s" % w)		
        print("w2 (inital rotation) = %s" % w2)

        print("steps = %s" % steps)	
        print("extent = %s" % extent)
        # print("self._degreesPerAU = %s" % self._degreesPerAU)
    left(w2)
    for i in range(steps):
        forward(length)
        left(w)
    left(-w2)


def isButtonPushed():
    return True

# TODO: implementation?
def tone(freq, time):
    pass
