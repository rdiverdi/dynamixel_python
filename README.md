# dynamixel_python

dynamixel_python is a python wrapper for dynamixel's official dynamixel_sdk.
It supports all motors documented on dynamixel's website and provides a simplified 
but fully featured interface for interacting with the motor through the U2D2 usb adapter

## Hardware support

Full support of all dynamixel motors is achieved throught the built-in web scraper which pulls
the control table documentation from dynamixel's website for all available models. Any issues with
this library are likely caused by typos in dynamixel's website, so please fix them and add a pull
request.

## package architecture

### DynamixelManager

The DynamixelManager class manages the usb port and maintains a dictionary of motors.
This is crucial for systems with multiple motors, but still simplifes initialization with
a single motor.

There are two optional arguments:
- usb_port defaults to `/dev/ttyUSB0`
- baud_rate defaults to 57600

### DynamixelMotor

These are the objects in DynamixelManager's dictionary.

For every line in the control table for your model motor, the DynamixelMotor has a method called `get_data_name`, where `data_name` is the actual name for that line in all lowercase and with all spaces replaced by underscores (eg. to get the "Model Number", use `get_model_number`). In addition, for variables with write access, there is a `set_data_name`.

## Getting Started

### install

clone the repository, `cd` into `dynamixel_python`, and run `pip install .`.

### run first example

- Ensure you have a U2D2 plugged in and a dynamixel plugged in, powered, and set up so spinning the motor won't damage anything.
- Open `examples/python single_motor.py` in a text editor.
- Edit `USB_PORT` to match the usb port of your U2D2
- Edit the `DYNAMIXEL_MODEL` at the top to match your motor and change the ID if you configured your motor's ID.
- Run `python examples/python_single_motor.py`

Your motor should sweep between position 0 and 1024 three times.

### Closer look at the code

```
    motors = DynamixelManager(USB_PORT)
    testMotor = motors.add_dynamixel('TestMotor', ID, DYNAMIXEL_MODEL)
    motors.init()
```
This instantiates a DynamixelManager object to communicate to the U2D2 on the configured usb port,
then adds a motor to the U2D2 with the configured ID and model. Once the motors are added, 
`motors.init()` intializes the communication with the U2D2.

```
    if not testMotor.ping():
        raise BaseException('motor not configured correctly')
```
The ping method checks for communication with a dynamixel with the configured ID.

```
    testMotor.set_operating_mode(3)
    testMotor.set_led(True)
    testMotor.set_torque_enable(True)
    testMotor.set_profile_velocity(262)
```
All of these commands come directly from the documented control table.

`operating_mode` 3 is position mode, `led` True turns the light on, `torque_enable` True activates the motor, and `profile_velocity` sets the speed.

For each of these, the `set_<control_table_name>(value)` pattern is used to write to the values.

```
    for i in range(3):
        testMotor.set_goal_position(0)
        time.sleep(0.5)

        testMotor.set_goal_position(1024)
        time.sleep(0.5)

```
The goal position works like any other control table value. This just alternates between position 0 and 1024 3 times, giving the motor 0.5 seconds to reach the position.

The `multiple_motors.py` example demonstrates using `get_moving_status` to see when the motor
has reached its target position.


```
    testMotor.set_torque_enable(False)
    testMotor.set_led(False)
```
Finally, the script disables the motor and turns off the led.


### other examples

The other examples assume you have multiple motors, but also demonstrate some more capabilites of the package. They're worth checking out even if you only have one motor.

- multiple_motors incorporates DynamixelManager in a class and demonstrates some nice features for interacting with multiple motors at a time.
- two_wheel_robot demonstrates velocity control

