import cv2
import pygame
from signs import *
import numpy as np
from hand_detector import *
from dataclasses import dataclass
from position import Position
from copy import copy

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
PALMGestureImage = pygame.image.load("PalmGesture.png").convert_alpha()
YAYGestureImage = pygame.image.load("YAYGesture.png").convert_alpha()

canvas_gestures: list[GestureImage] = []



DRAWING_SURFACE_WIDTH, DRAWING_SURFACE_HEIGHT = 600, 400
drawing_current_position = Position(DRAWING_SURFACE_WIDTH / 2, DRAWING_SURFACE_HEIGHT / 2) # default/starting position
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
    pygame.draw.circle(drawing_surface, DOT_COLOR, drawing_current_position.tuple(), DOT_RADIUS)

    drawing_surface.fill((255, 255, 255))
    for gesture_image in canvas_gestures:
        drawing_surface.blit(gesture_image.image, gesture_image.position.tuple())

    print(len(canvas_gestures))

    if detection_result.hand_landmarks: 
        for hand_landmark in detection_result.hand_landmarks: 
            if isGesture(hand_landmark, Gesture.YAY): 
                if previous_gesture == Gesture.NONE: 
                    previous_gesture = Gesture.YAY
                    camera_gesture_anchor = Position(hand_landmark[0].x * CAMERA_SURFACE_WIDTH, hand_landmark[0].y * CAMERA_SURFACE_HEIGHT)
                    drawing_gesture_anchor = copy(drawing_current_position)
                    canvas_gestures.append(GestureImage(PALMGestureImage, drawing_gesture_anchor))
                elif previous_gesture == Gesture.YAY: # itself
                    camera_gesture_current = Position(hand_landmark[0].x * CAMERA_SURFACE_WIDTH, hand_landmark[0].y * CAMERA_SURFACE_HEIGHT)
                    camera_gesture_offset = camera_gesture_current - camera_gesture_anchor

                    drawing_gesture_offset = Position(camera_gesture_offset.x / CAMERA_SURFACE_WIDTH * DRAWING_SURFACE_WIDTH / 2, camera_gesture_offset.y / CAMERA_SURFACE_HEIGHT * DRAWING_SURFACE_HEIGHT / 2)

                    drawing_current = drawing_gesture_anchor + drawing_gesture_offset

                    drawing_current.x = clamp(drawing_current.x, 0, DRAWING_SURFACE_WIDTH)
                    drawing_current.y = clamp(drawing_current.y, 0, DRAWING_SURFACE_HEIGHT)

                    canvas_gestures[-1].position = copy(drawing_current)

                if previous_gesture == Gesture.CONFIRM: # if it's not a gesture other than itself, NONE, or CONFIRM, it'll pass
                    previous_gesture = Gesture.NONE # reset current gesture to NONE, which eans the only way to get OUT of a gesture is through this CONFIRM
                    drawing_gesture_anchor = copy(drawing_current_position)
                    # which eans the only way to get OUT of a gesture is through this CONFIRM
                    pass # stamp image
                else: 
                    pass # do nothing
            # other gestures chekc here
            else: 
                drawing_gesture_anchor = copy(drawing_current_position)
                pass # set current_Gesture to NONE?"""

    pygame.display.flip()
    clock.tick(60) # some sort of fps idk

cap.release()
pygame.quit()
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