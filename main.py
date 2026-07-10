import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import cv2
import pygame
import pprint
from signs import *
import numpy as np
from camera import *

WIDTH = 600
HEIGHT = 500

# run pygame window
# input video
# continuously get hand gestures (make functions for each)
# draw mountains and trees based on gestures
# z-axis
# what the fuck is this ordering

base_options = python.BaseOptions(model_asset_path='hand_landmarker.task')
options = vision.HandLandmarkerOptions(base_options=base_options, num_hands=1)
detector = vision.HandLandmarker.create_from_options(options)

init_camera(WIDTH, HEIGHT)

while camera_opened(): 
    success, frame = get_camera_frame()
    if not success: break
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
    detection_result = detector.detect(mp_image)
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
cap.release()
cv2.destroyAllWindows()