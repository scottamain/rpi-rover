from gpiozero import Robot
from coralkit import vision
import pygame

pygame.init()
pygame.display.set_mode((100,100))
robot = Robot(left=(12, 24), right=(13, 25))
stop = False
curve_left = 0
curve_right = 0
direction = 0
speed = 0

try:
    for frame in vision.get_frames(flip=True):
        for event in pygame.event.get():
            print('EVENT')
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    direction = direction - 1 if direction > -10 else -10
                    print('left', direction)
                if event.key == pygame.K_RIGHT:
                    direction = direction + 1 if direction < 10 else 10
                    print('right', direction)
                if event.key == pygame.K_UP:
                    speed = speed + 1 if speed < 10 else 10
                    print('speed up', speed)
                if event.key == pygame.K_DOWN:
                    speed = speed - 1 if speed > -10 else -10
                    print('slow down', speed)
                if event.key == pygame.K_SPACE:
                    speed = 0
                
                if direction > 0:
                    curve_left = 0
                    curve_right = direction / 10
                elif direction < 0:
                    curve_right = 0
                    curve_left = abs(direction) / 10
                else:
                    curve_left = 0
                    curve_right = 0
                
                if speed > 0:
                    print('forward', speed, curve_left, curve_right)
                    robot.forward(speed=speed/10,
                                  curve_left=curve_left,
                                  curve_right=curve_right)
                elif speed < 0:
                    print('backward', speed, curve_left, curve_right)
                    robot.backward(speed=abs(speed)/10,
                                  curve_left=curve_left,
                                  curve_right=curve_right)
                else:
                    robot.stop()     
        
finally:
    robot.stop()
