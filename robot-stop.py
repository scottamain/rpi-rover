from gpiozero import Robot

robot = Robot(left=(12, 24), right=(13, 25))

robot.stop()
