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

DOT_COLOR = (127, 127, 127) #gray for now
DOT_RADIUS = 2

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Hand Drawing App")
clock = pygame.time.Clock()
pygame.init()

DRAWING_SURFACE_WIDTH = 600
DRAWING_SURFACE_HEIGHT = 400
DRAWING_START_X = DRAWING_SURFACE_WIDTH / 2
DRAWING_START_Y = DRAWING_SURFACE_HEIGHT / 2
DRAWING_SURFACE_PLACEMENT = (0, 0)
DRAWING_SURFACE_BACKGROUND_COLOR = (255, 255, 255) # white
drawing_current_x = DRAWING_START_X
drawing_current_y = DRAWING_START_Y
drawing_surface = pygame.Surface((DRAWING_SURFACE_WIDTH, DRAWING_SURFACE_HEIGHT))
drawing_surface.fill(DRAWING_SURFACE_BACKGROUND_COLOR)

CAMERA_SURFACE_WIDTH = 300
CAMERA_SURFACE_HEIGHT = 200
CAMERA_SURFACE_PLACEMENT = (DRAWING_SURFACE_WIDTH+5, 0)
camera = Camera(CAMERA_SURFACE_WIDTH, CAMERA_SURFACE_HEIGHT)

detector = HandDetector("hand_landmarker.task")
current_gesture = Gesture.NONE


drawng_anchor_position = (drawing_current_x, drawing_current_y)
camera_anchor_position = None

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
    screen.blit(camera_surface, CAMERA_SURFACE_PLACEMENT)






    screen.blit(drawing_surface, DRAWING_SURFACE_PLACEMENT)
    pygame.draw.circle(drawing_surface, DOT_COLOR, (drawing_current_x, drawing_current_y), DOT_RADIUS)










    detection_result = detector.relay(frame)
    if detection_result.hand_landmarks: 
        for hand_landmark in detection_result.hand_landmarks: 
            if isGesture(hand_landmark, Gesture.YAY): 
                if current_gesture == Gesture.NONE: 
                    current_gesture = Gesture.YAY
                    camera_anchor_position = (hand_landmark[0].x, hand_landmark[0].y)
                    # draw YAY gesture onto screen at position (drawing_current_x, y)
                if current_gesture == Gesture.YAY: # itself
                    pass # keep going?
                if current_gesture == Gesture.CONFIRM: 
                    pass # stamp image
                else: 
                    pass # do nothing
            if isGesture(hand_landmark, Gesture.ONE): 
                if current_gesture == Gesture.NONE: 
                    pass # set current_Gesture, update visuals to show the gesture to be painted onto canvas
                if current_gesture == Gesture.ONE: # itself
                    pass # keep going?
                if current_gesture == Gesture.CONFIRM: 
                    pass # stamp image
                else: 
                    pass # do nothing
            if isGesture(hand_landmark, Gesture.PALM): 
                if current_gesture == Gesture.NONE: 
                    pass # set current_Gesture, update visuals to show the gesture to be painted onto canvas
                if current_gesture == Gesture.PALM: # itself
                    pass # keep going?
                if current_gesture == Gesture.CONFIRM: 
                    pass # stamp image
                else: 
                    pass # do nothing
            else: 
                pass # set current_Gesture to NONE?

            #pprint.pprint(hand_landmark)

    pygame.display.flip()
    clock.tick(60) # some sort of fps idk

camera.release()
pygame.quit()
sys.exit()

"""if isOneSign(hand_landmark): 
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
            if draw_current_z < DRAW_START_Z: draw_current_z = DRAW_START_Z"""