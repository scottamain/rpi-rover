from gpiozero import Robot
from gpiozero import DigitalOutputDevice
from time import sleep

robot = Robot(left=(12, 24), right=(13, 25))

for i in range(3):
    robot.forward(curve_right=0.6)
    sleep(5)
    robot.forward(curve_left=0.6)
    sleep(5)

    
robot.stop()