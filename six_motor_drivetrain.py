# ----------------------------------------------------------------------------- #
#                                                                               #             
# 	Project:        SmartDrive Drivetrain Sample                                #
#   Author:         Andrew Olin                                                 #
#   Created:        Sept 04 2024                                                #
#	Description:    This example will show configuring a SmartDrive             #
#                   Drivetrain with some control examples                       #
#                                                                               #                                                                          
#   Configuration:  6 motor skid-steer chassis (1-3,8-10),                      #
#                   Inertial in Port 11                                         #
#                                                                               #                                                                          
# ----------------------------------------------------------------------------- #

# Library imports
from vex import *

# Brain should be defined by default
brain=Brain()

# Define our motors by Port
left_drive_smart_1 = Motor(Ports.PORT8, GearSetting.RATIO_18_1, True)
left_drive_smart_2 = Motor(Ports.PORT9, GearSetting.RATIO_18_1, True)
left_drive_smart_3 = Motor(Ports.PORT10, GearSetting.RATIO_18_1, True)
right_drive_smart_1 = Motor(Ports.PORT1, GearSetting.RATIO_18_1, False)
right_drive_smart_2 = Motor(Ports.PORT2, GearSetting.RATIO_18_1, False)
right_drive_smart_3 = Motor(Ports.PORT3, GearSetting.RATIO_18_1, False)

# Define which motors are on the left and right sides of the drivetrain
left_drive_group = MotorGroup(
    left_drive_smart_1,
    left_drive_smart_2,
    left_drive_smart_3,
)
right_drive_group = MotorGroup(
    right_drive_smart_1,
    right_drive_smart_2,
    right_drive_smart_3,
)

# Define our Inertial Sensor
inertia_sensor = Inertial(Ports.PORT11)

# Create an instance of our SmartDrive drivetrain
drivetrain = SmartDrive(left_drive_group, right_drive_group, inertia_sensor)

# Define our controller
controller = Controller()

# A python dictionary to hold our setting values
settings = {
    'arcadeControl': True,
}

def output_drivetrain_values(drivetrain: DriveTrain | SmartDrive):
    """
    Print the key drivetrain values out to the screen for diagnostics

    Args:
        drivetrain : The DriveTrain or SmartDrive to pull values from

    Returns:
        None
    """
    brain.screen.clear_screen()
    brain.screen.set_cursor(1,1)

    brain.screen.print("Velocity:", drivetrain.velocity(PERCENT))
    brain.screen.next_row()

    brain.screen.print("Current:", drivetrain.current(CurrentUnits.AMP))
    brain.screen.next_row()

    brain.screen.print("Power:", drivetrain.power(PowerUnits.WATT))
    brain.screen.next_row()

    brain.screen.print("Torque:", drivetrain.torque(TorqueUnits.NM))
    brain.screen.next_row()

    brain.screen.print("Efficiency:", drivetrain.efficiency(PERCENT))
    brain.screen.next_row()

    brain.screen.print("Temperature:", drivetrain.temperature())
    brain.screen.next_row()

    # If the drivetrain is a SmartDrive, output SmartDrive specific values
    if isinstance(drivetrain, SmartDrive):
        brain.screen.print("Heading:", drivetrain.heading(DEGREES))
        brain.screen.next_row()

#Function to hold split arcade control logic
def splitArcadeControl(drivetrain: DriveTrain | SmartDrive, turnSensitivity: float=.7):
    """
    Split Arcade Drivetrain Control

    Args:
        drivetrain (DriveTrain or SmartDrive): the drivetrain to be controlled
        turnSensitivity (float): optional value to modify the turn sensitivity
    
    Returns:
        None
    """
    # Get Stick values
    turnVal = controller.axis1.position()
    forwardVal = controller.axis3.position()

    # Apply turn sensitivity multiplier
    turnVal = turnVal * turnSensitivity

    # Apply stick values to drivetrain motors
    drivetrain.lm.spin(FORWARD, forwardVal + turnVal, PERCENT)
    drivetrain.rm.spin(FORWARD, forwardVal - turnVal, PERCENT)

# Function to hold tank control logic
def tankDriveControl(drivetrain: DriveTrain | SmartDrive):
    """
    Tank Drive Drivetrain Control

    Args:
        drivetrain (DriveTrain or SmartDrive): the drivetrain to be controlled
    
    Returns:
        None
    """
    # For controller support, map each of the sides of the drivetrain to a thumb stick
    # controller axis3 is up and down on the left thumb stick, we'll map to the left motors
    drivetrain.lm.spin(FORWARD,controller.axis3.value(), PERCENT)
    # controller axis2 is up and down on the right thumb stick, we'll map to the right motors
    drivetrain.rm.spin(FORWARD,controller.axis2.value(), PERCENT)

# Function to update our control setting
def toggleDrivetrain():
    """
    Toggle the Drivetrain, turning Arcade Control on or off

    Args:
        None
    
    Returns:
        None
    """
    # Inverts the true/false value setting for "arcadeControl"
    # and saves the change back into "settings"
    settings['arcadeControl'] = not settings.get('arcadeControl')

# When Button A is pressed on the controller, call our toggle drivetrain function
controller.buttonA.pressed(toggleDrivetrain)

# Print all Drivetrain sensing values to the screen in an infinite loop
while True:
    # if our setting is set to arcade control, use that
    if settings.get('arcadeControl'):
        splitArcadeControl(drivetrain)
    # otherwise, default to tank style controls
    else:
        tankDriveControl(drivetrain)


    # Call our output function to write our drivetrain diagnostics
    output_drivetrain_values(drivetrain)


    # A brief delay to allow text to be printed without distortion or tearing
    wait(100,MSEC)
    
