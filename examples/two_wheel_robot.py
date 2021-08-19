import time
from dynamixel_python import DynamixelManager

# set the model of dynamixel you are using as written in the motor's web url
DYNAMIXEL_MODEL = 'xl330-m077'


class MyRobot:
    """
    example of controlling multiple dynamixels with pynamixel
    """
    def __init__(self):
        self.motors = DynamixelManager()
        
        # setup two motors (Left and Right) with ids 1 and 2
        self.leftMotor = self.motors.add_dynamixel('leftMotor', 1, DYNAMIXEL_MODEL)
        self.rightMotor = self.motors.add_dynamixel('rightMotor', 2, DYNAMIXEL_MODEL)

        self.motors.init()
        if not self.motors.ping_all():
            raise BaseException("motors aren't configured correctly")

    def test(self):
        """
        spin left motor for 0.5 seconds, then right motor for 0.5 seconds, then both for 1 second
        also turn on motor leds when spinning
        """
        # set motors to velocity control mode
        self.motors.for_all(lambda motor: motor.set_operating_mode(1))
        # enable motor control
        self.motors.for_all(lambda motor: motor.set_goal_velocity(0))
        self.motors.enable_all()
        # run left motor
        self.leftMotor.set_led(True)
        self.leftMotor.set_goal_velocity(262)
        time.sleep(0.5)
        self.leftMotor.set_goal_velocity(0)
        self.leftMotor.set_led(False)
        # run right motor
        self.rightMotor.set_led(True)
        self.rightMotor.set_goal_velocity(262)
        time.sleep(0.5)
        self.rightMotor.set_goal_velocity(0)
        self.rightMotor.set_led(False)
        # run both motors
        self.leftMotor.set_led(True)
        self.rightMotor.set_led(True)
        self.leftMotor.set_goal_velocity(262)
        self.rightMotor.set_goal_velocity(262)
        time.sleep(1.0)
        self.leftMotor.set_goal_velocity(0)
        self.rightMotor.set_goal_velocity(0)
        self.leftMotor.set_led(False)
        self.rightMotor.set_led(False)
        
        # shut down
        self.motors.disable_all()
        self.motors.for_all(lambda motor: motor.set_led(False))

if __name__ == '__main__':
    robot = MyRobot()
    robot.test()

