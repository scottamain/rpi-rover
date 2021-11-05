from gpiozero import Robot
from coralkit import vision
import pygame
import json, os

pygame.init()
pygame.display.set_mode((100,100))
clock = pygame.time.Clock()
robot = Robot(left=(12, 24), right=(13, 25))

curve_left = 0
curve_right = 0
speed = 0
stop = False
backward = False
running = True

#Initialize controller
joysticks = []
for i in range(pygame.joystick.get_count()):
    joysticks.append(pygame.joystick.Joystick(i))
for joystick in joysticks:
    joystick.init()

with open(os.path.join("ps3_keys.json"), 'r+') as file:
    controller_keys = json.load(file)
    button_keys = controller_keys['buttons']
    analog_keys = controller_keys['analogs']
    
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.JOYBUTTONDOWN:
            if event.button == button_keys['start']:
                running = False

        # Joystick steering and analog forward/reverse
        if event.type == pygame.JOYAXISMOTION:
            if event.axis == analog_keys['left_horiz']:
                if event.value < -0.2:
                    curve_left = abs(event.value) if event.value >= -1 else 1
                    curve_right = 0
                elif event.value > 0.2:
                    curve_right = event.value if event.value <= 1 else 1
                    curve_left = 0
                else:
                    curve_right = 0
                    curve_left = 0
            # Forward/reverse are mutually exclusive
            if event.axis == analog_keys['right_trigger']:
                if event.value > -1 and event.value <= 0:
                    speed = (1 - abs(event.value)) / 2
                elif event.value > 0 and event.value < 1:
                    speed = (event.value / 2) + 0.5
                else:
                    speed = 0
                backward = False
            elif event.axis == analog_keys['left_trigger']:
                if event.value > -1 and event.value < 0:
                    speed = (1 - abs(event.value)) / 2
                elif event.value > 0 and event.value < 1:
                    speed = (event.value / 2) + 0.5
                else:
                    speed = 0
                backward = True
                            
            if backward:
                robot.backward(speed=speed,
                              curve_left=curve_left,
                              curve_right=curve_right)
            else:
                robot.forward(speed=speed,
                              curve_left=curve_left,
                              curve_right=curve_right)
                
    clock.tick(30)
