from ev3dev_ext import *
from ev3dev.version import __version__
from PIL import Image, ImageDraw

#---------------------------------------------------------------------------

# Furnish mode_set class (which is a wrapper around std::set<std::string>)
# with __repr__ and __str__ methods which are better than defaults.
def mode_set_repr(self):
    return list(self).__repr__()

def mode_set_str(self):
    return list(self).__str__()

mode_set.__repr__ = mode_set_repr
mode_set.__str__  = mode_set_str

#---------------------------------------------------------------------------

# proxy classes for easy attribute access for device class
class attr_int_proxy:
    def __init__(self, dev):
        self.__dict__['dev'] = dev

    def __getattr__(self, name):
        return self.__dict__['dev'].get_attr_int(name)

    def __setattr__(self, name, val):
        self.__dict__['dev'].set_attr_int(name, val)

def attr_int_get(dev):
    return attr_int_proxy(dev)

device.attr_int = property(fget=attr_int_get)


class attr_string_proxy:
    def __init__(self, dev):
        self.__dict__['dev'] = dev

    def __getattr__(self, name):
        return self.__dict__['dev'].get_attr_string(name)

    def __setattr__(self, name, val):
        self.__dict__['dev'].set_attr_string(name, val)

def attr_string_get(dev):
    return attr_string_proxy(dev)

device.attr_string = property(fget=attr_string_get)

class attr_line_proxy:
    def __init__(self, dev):
        self.__dict__['dev'] = dev

    def __getattr__(self, name):
        return self.__dict__['dev'].get_attr_line(name)

def attr_line_get(dev):
    return attr_line_proxy(dev)

device.attr_line = property(fget=attr_line_get)

class attr_set_proxy:
    def __init__(self, dev):
        self.__dict__['dev'] = dev

    def __getattr__(self, name):
        return self.__dict__['dev'].get_attr_set(name)

def attr_set_get(dev):
    return attr_set_proxy(dev)

device.attr_set = property(fget=attr_set_get)

#---------------------------------------------------------------------------

# Helper function to compute power for left and right motors when steering
def steering(direction, power=100):
    """
    Computes how fast each motor in a pair should turn to achieve the
    specified steering.

    Input:
        direction [-100, 100]:
            -100 means turn left as fast as possible,
             0   means drive in a straight line, and
             100 means turn right as fast as possible.
        power: the outmost motor (the one rotating faster) should receive this
            value of power.

    Output:
        a tuple of power values for a pair of motors.
    """

    pl = power
    pr = power
    s = (50 - abs(float(direction))) / 50

    if direction >= 0:
        pr *= s
    else:
        pl *= s

    return (int(pl), int(pr))

#---------------------------------------------------------------------------

# Stop a motor on destruction
def stop_taho_motor(self):
    self.command = 'stop'

large_motor.__del__ = stop_taho_motor
medium_motor.__del__ = stop_taho_motor

def stop_dc_motor(self):
    self.command = 'coast'

dc_motor.__del__ = stop_dc_motor

def stop_servo_motor(self):
    self.command = 'float'

servo_motor.__del__ = stop_servo_motor

#~autogen python_motor_commands classes.motor>currentClass

def motor_run_forever(self, **attr):
    for key in attr:
        setattr(self, key, attr[key])
    self.command = "run-forever"

motor.run_forever = motor_run_forever

def motor_run_to_abs_pos(self, **attr):
    for key in attr:
        setattr(self, key, attr[key])
    self.command = "run-to-abs-pos"

motor.run_to_abs_pos = motor_run_to_abs_pos

def motor_run_to_rel_pos(self, **attr):
    for key in attr:
        setattr(self, key, attr[key])
    self.command = "run-to-rel-pos"

motor.run_to_rel_pos = motor_run_to_rel_pos

def motor_run_timed(self, **attr):
    for key in attr:
        setattr(self, key, attr[key])
    self.command = "run-timed"

motor.run_timed = motor_run_timed

def motor_run_direct(self, **attr):
    for key in attr:
        setattr(self, key, attr[key])
    self.command = "run-direct"

motor.run_direct = motor_run_direct

def motor_stop(self, **attr):
    for key in attr:
        setattr(self, key, attr[key])
    self.command = "stop"

motor.stop = motor_stop

def motor_reset(self, **attr):
    for key in attr:
        setattr(self, key, attr[key])
    self.command = "reset"

motor.reset = motor_reset



#~autogen

#~autogen python_motor_commands classes.dcMotor>currentClass

def dc_motor_run_forever(self, **attr):
    for key in attr:
        setattr(self, key, attr[key])
    self.command = "run-forever"

dc_motor.run_forever = dc_motor_run_forever

def dc_motor_run_timed(self, **attr):
    for key in attr:
        setattr(self, key, attr[key])
    self.command = "run-timed"

dc_motor.run_timed = dc_motor_run_timed

def dc_motor_stop(self, **attr):
    for key in attr:
        setattr(self, key, attr[key])
    self.command = "stop"

dc_motor.stop = dc_motor_stop



#~autogen

#~autogen python_motor_commands classes.servoMotor>currentClass

def servo_motor_run(self, **attr):
    for key in attr:
        setattr(self, key, attr[key])
    self.command = "run"

servo_motor.run = servo_motor_run

def servo_motor_float(self, **attr):
    for key in attr:
        setattr(self, key, attr[key])
    self.command = "float"

servo_motor.float = servo_motor_float



#~autogen

#---------------------------------------------------------------------------

# Provide a convenience wrapper for ev3dev.lcd class
class LCD(lcd):
    """
    A convenience wrapper for ev3dev.lcd class.
    Provides drawing functions from python imaging library (PIL).
    """

    def __init__(self):
        super(LCD, self).__init__()

        def alignup(n, m):
            r = n % m
            if r == 0:
                return n
            else:
                return n - r + m


        nx = alignup(self.resolution_x, 32)
        ny = self.resolution_y

        self.img = Image.new("1", (nx, ny), "white")

    @property
    def shape(self):
        """
        Dimensions of the LCD screen.
        """
        return (self.resolution_x, self.resolution_y)

    @property
    def draw(self):
        """
        Returns a handle to PIL.ImageDraw.Draw class associated with LCD.

        Example:
        lcd.draw.rectangle((10,10,60,20), fill=True)
        """
        return ImageDraw.Draw(self.img)

    def clear(self):
        """
        Clears the LCD.
        """
        self.draw.rectangle(((0,0),(self.shape)), fill="white")

    def update(self):
        """
        Applies pending changes to LCD.
        Nothing will be drawn on the screen until this function is called.
        """
        self.frame_buffer[:] = self.img.tobytes("raw", "1;IR")

