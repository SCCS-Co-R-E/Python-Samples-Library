# ----------------------------------------------------------------------------- #
#                                                                               #             
# 	Project:        Optical Sensor Sample                                       #
#   Author:         Andrew Olin                                                 #
#   Created:        Sept 04 2024                                                #
#	  Description:    This example will show some key ways the Optical            #
#                   sensor can be used                                          #
#                                                                               #                                                                          
#   Configuration:  Optical Sensor in Port 20                                   #
#                                                                               #                                                                          
# ----------------------------------------------------------------------------- #

# Library imports
from vex import *

# Brain should be defined by default
brain=Brain()

# Define optical sensor
opticalSensor1 = Optical(Ports.PORT20)

# Use this to toggle between object detection and color reading mode
objectDetectionMode = True

def objectDetected():
    """
    Function to run if optical sensor detects an object

    Args:
        None
    
    Returns:
        None
    """
    brain.screen.clear_screen()
    brain.screen.set_cursor(1,1)
    brain.screen.print('Object detected!')
    brain.screen.next_row()

def objectLost():
    """
    Function to run if optical sensor loses an object

    Args:
        None
    
    Returns:
        None
    """
    brain.screen.clear_screen()
    brain.screen.set_cursor(1,1)
    brain.screen.print('Object lost!')
    brain.screen.next_row()

# Set Light to 100% Brightness
opticalSensor1.set_light(100)

# If set to object detection mode, creates callbacks
if objectDetectionMode:
    opticalSensor1.object_detected(objectDetected)
    opticalSensor1.object_lost(objectLost)

# Else run a loop and output values
else:
    while True:
        brain.screen.clear_screen()
        brain.screen.set_cursor(1,1)

        brain.screen.print('Brightness: ',opticalSensor1.brightness())
        brain.screen.next_row()

        # Check if color detected is red
        if opticalSensor1.color() == Color.RED:
            brain.screen.print('Color: RED')
            brain.screen.next_row()
        # Check if color is blue
        elif opticalSensor1.color() == Color.BLUE:
            brain.screen.print('Color: BLUE')
            brain.screen.next_row()
        # Else output the detected color
        else:
            brain.screen.print('Color: ',opticalSensor1.color())
            brain.screen.next_row()

        brain.screen.print('Hue: ',opticalSensor1.hue())
        brain.screen.next_row()

        # A brief delay to allow text to be printed without distortion or tearing
        wait(300,MSEC)