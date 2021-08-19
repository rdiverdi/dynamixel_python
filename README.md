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

### DynamixelMotor

These are the objects in DynamixelManager's dictionary.

For every line in the control table for your model motor, the DynamixelMotor has a method called `get_data_name`, where `data_name` is the actual name for that line in all lowercase and with all spaces replaced by underscores (eg. to get the "Model Number", use `get_model_number`). In addition, for variables with write access, there is a `set_data_name`.

## Getting Started

### install

clone the repository, `cd` into `dynamixel_python`, and run `pip install .`.

### run first example

Go to the examples `cd examples`, plug in your dynamixel (make sure spinning the motor won't damage anything), and run `python single_motor.py`.

Your motor should sweep between position 0 and 1024 three times.

open the file to see how the simplest way to use dynamixel_python to control one motor

### other examples

The oter examples assume you have multiple motors, but also demonstrate some more capabilites of the package. They're worth checking out even if you only have one motor.

- multiple_motors incorporates DynamixelManager in a class and demonstrates some nice features for interacting with multiple motors at a time.
- two_wheel_robot demonstrates velocity control

