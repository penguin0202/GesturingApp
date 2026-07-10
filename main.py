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

WIDTH = 600
HEIGHT = 500

# run pygame window
# input video
# continuously get hand gestures (make functions for each)
# draw mountains and trees based on gestures
# z-axis
# what the fuck is this ordering

camera = Camera(WIDTH, HEIGHT)
detector = HandDetector("hand_landmarker.task")

while camera.opened(): 
    success, frame = camera.get_frame()
    if not success: break
    detection_result = detector.relay(frame)
    if detection_result.hand_landmarks: 
        for hand_landmark in detection_result.hand_landmarks: 
            pprint.pprint(hand_landmark)
    cv2.imshow("capture image", frame)
    if cv2.waitKey(1) == ord('q'): break

"""running=True
while running:
    for event in pygame.event.get(): #process events since last loop cycle
        if event.type == KEYDOWN:
            running=False
            
            
pygame.quit()"""
camera.release()
cv2.destroyAllWindows()