import time
from gpiozero import Robot
from coralkit import vision

#import pygame

#clock = pygame.time.Clock()
robot = Robot(left=(12, 24), right=(13, 25))

curve_left = 0
curve_right = 0
speed = 0
accel_rate = 0.1
max_speed = 0.4

stop = False
backward = False
running = True

width, height = vision.VIDEO_SIZE
left_max = 0
left_min = int(width * 0.4)
right_min = int(width * 0.6)
right_max = width
turn_range = left_min - left_max
#vision_area = width * height

# Load the neural network model
detector = vision.Detector('models/efficientdet-lite-yarndoll_edgetpu.tflite')

def get_centerpoint(bbox):
    """Returns tuple of (x,y) for box center point"""
    return ((bbox.xmax + bbox.xmin) / 2, (bbox.ymax + bbox.ymin) / 2)

DELAY_SECS = 0.1
last_pred_time = time.monotonic()

for frame in vision.get_frames(flip=True):
    objs = detector.get_objects(frame, threshold=0.3)
    vision.draw_objects(frame, objs)
    x = 0
    if objs:
        obj = objs[0]
        speed = speed + accel_rate if speed < max_speed else max_speed
        x, _ = get_centerpoint(obj.bbox)
        
        if x < left_min:
            # Go left
            curve_right = 0
            curve_left = (left_min - x) / turn_range
        elif x > right_min:
            # Go right
            curve_right = (x - right_min) / turn_range
            curve_left = 0
        else:
            curve_right = 0
            curve_left = 0
        last_pred_time = time.monotonic()
    else:
        speed = speed - accel_rate if speed > 0.1 else 0
    
    speed = round(speed, 2)
    curve_left = round(curve_left, 2)
    curve_right = round(curve_right, 2)
    print(f'speed: {speed}, left: {curve_left}, right: {curve_right}')
    print(f'    x: {x}')
    robot.forward(speed=speed,
                  curve_left=curve_left,
                  curve_right=curve_right)

        

    #clock.tick(60)
