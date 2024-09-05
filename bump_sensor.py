# ----------------------------------------------------------------------------- #
#                                                                               #             
# 	Project:        Bump Sensor Sample                                          #
#   Author:         Andrew Olin                                                 #
#   Created:        Sept 04 2024                                                #
#   Description:    This example will show some key ways the Bump               #
#                   sensor can be used                                          #
#                                                                               #                                                                          
#   Configuration:  Bump Sensor in Analog H                                     #
#                                                                               #                                                                          
# ----------------------------------------------------------------------------- #

# Library imports
from vex import *

# Brain should be defined by default
brain=Brain()

bumpSensor1 = Bumper(brain.three_wire_port.h)

def buttonCallback():
    """
    Function to run if bump sensor is pressed

    Args:
        None
    
    Returns:
        None
    """
    brain.screen.print('Button was clicked!')
    brain.screen.next_row()

bumpSensor1.pressed(buttonCallback)

while True:
    brain.screen.clear_screen()
    brain.screen.set_cursor(1,1)

    brain.screen.print('Value: ', bumpSensor1.value())
    brain.screen.next_row()

    if bumpSensor1.pressing():
        brain.screen.print('Button is currently being pressed!')
        brain.screen.next_row()

    # A brief delay to allow text to be printed without distortion or tearing
    wait(300,MSEC)