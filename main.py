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
from dataclasses import dataclass
from position import Position

DOT_COLOR = (127, 127, 127) #gray for now
DOT_RADIUS = 2

cap = cv2.VideoCapture(0)


WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Hand Drawing App")
clock = pygame.time.Clock()
pygame.init()

class GestureImage():
    def __init__(self, image: pygame.Surface, position: Position): 
        self.image: pygame.Surface = image
        self.position: Position = position

#YAYGestureImage = GestureImage(pygame.image.load("YAYGesture.png").convert_alpha())
#ONEGestureImage = GestureImage(pygame.image.load("ONEGesture.png").convert_alpha())
PALMGestureImage = GestureImage(pygame.image.load("PalmGesture.png").convert_alpha(), Position())
YAYGestureImage = GestureImage(pygame.image.load("YAYGesture.png").convert_alpha(), Position())

canvas_gestures: list[GestureImage] = []



DRAWING_SURFACE_WIDTH, DRAWING_SURFACE_HEIGHT = 600, 400
drawing_current_x = DRAWING_SURFACE_WIDTH / 2 # default/starting position
drawing_current_y = DRAWING_SURFACE_HEIGHT / 2 # default/starting position
drawing_surface = pygame.Surface((DRAWING_SURFACE_WIDTH, DRAWING_SURFACE_HEIGHT))
drawing_surface.fill((255, 255, 255)) # DRAWING_SURFACE_BACKGROUND_COLOR; it's white now

CAMERA_SURFACE_WIDTH, CAMERA_SURFACE_HEIGHT = 300, 200
cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_SURFACE_WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_SURFACE_HEIGHT)

DRAWING_SURFACE_PLACEMENT = (0, 0)
CAMERA_SURFACE_PLACEMENT = (DRAWING_SURFACE_WIDTH+5, 0)

detector = HandDetector("hand_landmarker.task")
previous_gesture = Gesture.NONE

camera_gesture_anchor = Position()
drawing_gesture_anchor = Position()


camera_gesture_anchor_x = 0
camera_gesture_anchor_y = 0

drawing_gesture_anchor_x = 0
drawing_gesture_anchor_y = 0

camera_gesture_current_x = 0
camera_gesture_current_y = 0

camera_anchor_position = None

def clamp(value, min, max): 
    if value < min: value = min
    if value > max: value = max
    return value

running=True
while running:
    for event in pygame.event.get(): #process events since last loop cycle
        if event.type == pygame.QUIT:
            running=False


    
    success, frame = cap.read()
    if not success: 
        print("can't get camera")
        break
    frame = cv2.flip(frame, 1)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    detection_result = detector.relay(frame)

    frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
    frame = cv2.flip(frame, 0)
    camera_surface = pygame.surfarray.make_surface(frame)
    screen.blit(camera_surface, CAMERA_SURFACE_PLACEMENT)

    screen.blit(drawing_surface, DRAWING_SURFACE_PLACEMENT)
    pygame.draw.circle(drawing_surface, DOT_COLOR, (drawing_current_x, drawing_current_y), DOT_RADIUS)

    if detection_result.hand_landmarks: 
        for hand_landmark in detection_result.hand_landmarks: 
            if isGesture(hand_landmark, Gesture.YAY): 
                if previous_gesture == Gesture.NONE: 
                    previous_gesture = Gesture.YAY
                    camera_gesture_anchor = Position(hand_landmark[0].x * CAMERA_SURFACE_WIDTH, hand_landmark[0].y * CAMERA_SURFACE_HEIGHT)
                    drawing_gesture_anchor = Position(drawing_current_x, drawing_current_y)
                    canvas_gestures.append(GestureImage(PALMGestureImage.image))









                    # draw YAY gesture onto screen at position (drawing_current_x, y)
                elif previous_gesture == Gesture.YAY: # itself
                    camera_gesture_current_x = hand_landmark[0].x
                    camera_gesture_current_y = hand_landmark[0].y

                    # these are NORMALIZED, NOT ACTUALLY THE CAMERA GESTURE OFFSET. Because google mediapipe is a bitch (a nice bitch)
                    camera_gesture_offset_x = camera_gesture_current_x - camera_gesture_anchor_x
                    camera_gesture_offset_y = camera_gesture_current_y - camera_gesture_anchor_y

                    # this is NOT normalized (im sorry about the naming)
                    drawing_gesture_offset_x = camera_gesture_offset_x * DRAWING_SURFACE_WIDTH / 2
                    drawing_gesture_offset_y = camera_gesture_offset_y * DRAWING_SURFACE_HEIGHT / 2

                    drawing_current_x = drawing_gesture_anchor_x + drawing_gesture_offset_x
                    drawing_current_y = drawing_gesture_anchor_y + drawing_gesture_offset_y

                    drawing_current_x = clamp(drawing_current_x, 0, DRAWING_SURFACE_WIDTH)
                    drawing_current_y = clamp(drawing_current_y, 0, DRAWING_SURFACE_HEIGHT)

                    pass # keep going?
                if previous_gesture == Gesture.CONFIRM: # if it's not a gesture other than itself, NONE, or CONFIRM, it'll pass
                    previous_gesture = Gesture.NONE # reset current gesture to NONE, which eans the only way to get OUT of a gesture is through this CONFIRM
                    drawing_gesture_anchor_x = drawing_current_x
                    drawing_gesture_anchor_y = drawing_current_y
                    # which eans the only way to get OUT of a gesture is through this CONFIRM
                    pass # stamp image
                else: 
                    pass # do nothing
            # other gestures chekc here
            else: 
                previous_gesture = Gesture.NONE
                drawing_gesture_anchor_x = drawing_current_x
                drawing_gesture_anchor_y = drawing_current_y
                pass # set current_Gesture to NONE?"""

    pygame.display.flip()
    clock.tick(60) # some sort of fps idk

cap.release()
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