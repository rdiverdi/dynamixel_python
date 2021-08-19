import time
from dynamixel_python import DynamixelManager

# set the model of dynamixel you are using as written in the motor's web url
DYNAMIXEL_MODEL = 'xl330-m077'
# set your list of motors formatted as (<human readable name>, <configured id>)
MOTOR_LIST = [('A', 1), ('B', 2), ('C', 3)]


class MyRobot:
    """
    example of controlling multiple dynamixels with pynamixel
    """
    def __init__(self):
        """
        set up and initialize motors according to MOTOR_LIST
        """
        self.motors = DynamixelManager()
        for dxl_name, dxl_id in MOTOR_LIST:
            self.motors.add_dynamixel(dxl_name, dxl_id, DYNAMIXEL_MODEL)

        self.motors.init()
        if not self.motors.ping_all():
            raise BaseException("motors aren't configured correctly")

    def test(self):
        """
        test all motors by turning on their LED and sweeping their position
        """
        # set operating mode to position control
        self.motors.for_all(lambda motor: motor.set_operating_mode(3))

        for motor in self.motors:
            # sequentially turn on leds
            motor.set_led(True)
            time.sleep(0.2)
        # enable motor control
        self.motors.enable_all()
        self.motors.for_all(lambda motor: motor.set_profile_velocity(262))
        # move all motors to 0
        self.motors.for_all(lambda motor: motor.set_goal_position(0))
        time.sleep(0.5)
        # move all motors to 1024
        self.motors.for_all(lambda motor: motor.set_goal_position(1024))
        time.sleep(1)

        # sequentially move each motor back to 0
        for dxl_name, dxl_id in MOTOR_LIST:
            self.motors[dxl_name].set_goal_position(0)
            time.sleep(0.5)

        # wait for movement to finish
        while not self.motors[MOTOR_LIST[-1][0]].get_moving_status()%2:
            time.sleep(0.001)
        
        # shut down
        self.motors.disable_all()
        self.motors.for_all(lambda motor: motor.set_led(False))

if __name__ == '__main__':
    robot = MyRobot()
    robot.test()

