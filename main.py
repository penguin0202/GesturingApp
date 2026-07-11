import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import cv2
import pygame
import pprint
from signs import *
import numpy as np
from camera import *
from hand_detector import *
import sys

CAM_WIDTH = 600
CAM_HEIGHT = 500

pygame.init()

WINDOW_WIDTH = 700
WINDOW_HEIGHT = 600

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("hi this is a caption <3 niah~")
clock = pygame.time.Clock()

# run pygame window
# input video
# continuously get hand gestures (make functions for each)
# draw mountains and trees based on gestures
# z-axis
# what the fuck is this ordering

camera = Camera(CAM_WIDTH, CAM_HEIGHT)
detector = HandDetector("hand_landmarker.task")

"""while camera.opened(): 
    success, frame = camera.get_frame()
    if not success: break
    detection_result = detector.relay(frame)
    if detection_result.hand_landmarks: 
        for hand_landmark in detection_result.hand_landmarks: 
            pprint.pprint(hand_landmark)
    cv2.imshow("capture image", frame)
    if cv2.waitKey(1) == ord('q'): break"""

running=True
while running:
    for event in pygame.event.get(): #process events since last loop cycle
        if event.type == pygame.QUIT:
            running=False
    
    success, frame = camera.get_frame()
    if not success: 
        print("can't get camera")
        break

    detection_result = detector.relay(frame)
    if detection_result.hand_landmarks: 
        for hand_landmark in detection_result.hand_landmarks: 
            pprint.pprint(hand_landmark)

    camera_surface = pygame.surfarray.make_surface(frame)

    screen.blit(camera_surface, (0, 0))
    pygame.display.flip()

    clock.tick(60) # some sort of fps idk

camera.release()
pygame.quit()
sys.exit()