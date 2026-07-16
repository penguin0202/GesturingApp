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
from drawing import *

CAM_WIDTH = 300
CAM_HEIGHT = 200

DRAW_WIDTH = 600
DRAW_HEIGHT = 400

DRAW_START_X = DRAW_WIDTH / 2
DRAW_X_INCREMENT_STEP = 10
draw_current_x = DRAW_START_X

DRAW_START_Z = 0.1
DRAW_Z_INCREMENT_STEP = 1
draw_current_z = DRAW_START_Z

pygame.init()

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("hi this is a caption <3 niah~")
clock = pygame.time.Clock()

camera = Camera(CAM_WIDTH, CAM_HEIGHT)
detector = HandDetector("hand_landmarker.task")

running=True

while running:
    for event in pygame.event.get(): #process events since last loop cycle
        if event.type == pygame.QUIT:
            running=False
    
    success, frame = camera.get_frame()
    if not success: 
        print("can't get camera")
        break

    camera_surface = pygame.surfarray.make_surface(frame)
    screen.blit(camera_surface, (DRAW_WIDTH+5, 0))

    draw_surface = pygame.Surface((DRAW_WIDTH, DRAW_HEIGHT))
    drawing = Drawing(draw_surface)
    screen.blit(draw_surface, (0, 0))

    detection_result = detector.relay(frame)
    if detection_result.hand_landmarks: 
        for hand_landmark in detection_result.hand_landmarks: 
            if isOneSign(hand_landmark): 
                drawing.spawn_tree(draw_current_x, draw_current_z)
                print("one sign")
            elif isThumbingRightSign(hand_landmark): 
                # have to update visual indicator too
                draw_current_x += DRAW_X_INCREMENT_STEP
                if draw_current_x > DRAW_WIDTH: draw_current_x = DRAW_WIDTH
            elif isThumbingLeftSign(hand_landmark): 
                # have to update visual indicator too
                draw_current_x -= DRAW_X_INCREMENT_STEP
                if draw_current_x < 0: draw_current_x = 0
            elif isHaltSign(hand_landmark): 
                # unsure about visual indicator
                draw_current_z += DRAW_Z_INCREMENT_STEP
            elif isBackHandSign(hand_landmark): 
                # unsure about visual indicator
                draw_current_z -= DRAW_Z_INCREMENT_STEP
                if draw_current_z < DRAW_START_Z: draw_current_z = DRAW_START_Z



            #pprint.pprint(hand_landmark)

    pygame.display.flip()

    clock.tick(60) # some sort of fps idk

camera.release()
pygame.quit()
sys.exit()