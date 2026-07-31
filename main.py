import cv2
import pygame
from signs import *
import numpy as np
from hand_detector import *
from dataclasses import dataclass
from position import Position
from copy import copy
import threading

DOT_COLOR = (127, 127, 127) #gray for now
DOT_RADIUS = 2

cap = cv2.VideoCapture(0)

allow_undo = True

WINDOW_WIDTH = 710
WINDOW_HEIGHT = 410
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Gesturing App")
clock = pygame.time.Clock()
pygame.init()

title_font = pygame.font.SysFont("Arial", 36)
title_surface = title_font.render("Gesturing App", True, (255, 255, 255))
screen.blit(title_surface, (420, 10))

description_font = pygame.font.SysFont("Arial", 24)
description_surface_1 = description_font.render("Press 'S' to save your gesturing", True, (200, 200, 200))
screen.blit(description_surface_1, (420, 65))
description_surface_3 = description_font.render("Press 'U' to undo last gesture", True, (200, 200, 200))
screen.blit(description_surface_3, (420, 95))
description_surface_4 = description_font.render("Press 'C' to center gestures", True, (200, 200, 200))
screen.blit(description_surface_4, (420, 125))
description_surface_5 = description_font.render("Press 'Q' to quit gesturing", True, (200, 200, 200))
screen.blit(description_surface_5, (420, 155))

@dataclass
class GestureImage():
    image: pygame.Surface
    position: Position

GESTURE_IMAGE_SCALE = (100, 100)
canvas_gestures: list[GestureImage] = []
ONEGestureImage = pygame.transform.scale(pygame.image.load("ONEGesture.png").convert_alpha(), GESTURE_IMAGE_SCALE)
PALMGestureImage = pygame.transform.scale(pygame.image.load("PalmGesture.png").convert_alpha(), GESTURE_IMAGE_SCALE)
YAYGestureImage = pygame.transform.scale(pygame.image.load("YayGesture.png").convert_alpha(), GESTURE_IMAGE_SCALE)
THREEGestureImage = pygame.transform.scale(pygame.image.load("ThreeGesture.png").convert_alpha(), GESTURE_IMAGE_SCALE)

DRAWING_SURFACE_WIDTH, DRAWING_SURFACE_HEIGHT = 400, 400
drawing_surface = pygame.Surface((DRAWING_SURFACE_WIDTH, DRAWING_SURFACE_HEIGHT))

CAMERA_SURFACE_WIDTH, CAMERA_SURFACE_HEIGHT = 300, 200

DRAWING_SURFACE_PLACEMENT = (0, 0)
CAMERA_SURFACE_PLACEMENT = (DRAWING_SURFACE_WIDTH+10, DRAWING_SURFACE_HEIGHT - CAMERA_SURFACE_HEIGHT)

detector = HandDetector("hand_landmarker.task")
previous_gesture = Gesture.NONE

camera_gesture_previous = Position()
drawing_gesture_previous = Position()
camera_gesture_current = Position()
drawing_gesture_current = Position(DRAWING_SURFACE_WIDTH / 2, DRAWING_SURFACE_HEIGHT / 2) # default/starting position
gesture_lost = False

def reset_allow_undo():
    global allow_undo
    allow_undo = True


def update_active_gesture(hand_landmark):
    """Update position anchors and move the currently-active gesture image.

    This consolidates the repeated code used by YAY, PALM, THREE, and ONE.
    """
    global gesture_lost, camera_gesture_previous, drawing_gesture_previous, camera_gesture_current, drawing_gesture_current, canvas_gestures
    if gesture_lost:
        gesture_lost = False
        camera_gesture_previous = Position(hand_landmark[0].x * CAMERA_SURFACE_WIDTH, hand_landmark[0].y * CAMERA_SURFACE_HEIGHT)
        drawing_gesture_previous = copy(drawing_gesture_current)

    camera_gesture_current = Position(hand_landmark[0].x * CAMERA_SURFACE_WIDTH, hand_landmark[0].y * CAMERA_SURFACE_HEIGHT)
    camera_gesture_offset = camera_gesture_current - camera_gesture_previous

    drawing_gesture_offset = Position(
        camera_gesture_offset.x / CAMERA_SURFACE_WIDTH * DRAWING_SURFACE_WIDTH,
        camera_gesture_offset.y / CAMERA_SURFACE_HEIGHT * DRAWING_SURFACE_HEIGHT,
    )

    drawing_gesture_current = (drawing_gesture_previous + drawing_gesture_offset).clamp(0, DRAWING_SURFACE_WIDTH, 0, DRAWING_SURFACE_HEIGHT)

    if canvas_gestures:
        canvas_gestures[-1].position = copy(drawing_gesture_current)


def start_gesture(gesture_enum, hand_landmark, gesture_image):
    """Initialize a new gesture on the canvas and set anchor positions."""
    global previous_gesture, gesture_lost, camera_gesture_previous, drawing_gesture_previous, canvas_gestures
    previous_gesture = gesture_enum
    gesture_lost = False
    camera_gesture_previous = Position(hand_landmark[0].x * CAMERA_SURFACE_WIDTH, hand_landmark[0].y * CAMERA_SURFACE_HEIGHT)
    drawing_gesture_previous = copy(drawing_gesture_current)
    canvas_gestures.append(GestureImage(gesture_image, drawing_gesture_previous))

running=True
while running:
    for event in pygame.event.get(): #process events since last loop cycle
        if event.type == pygame.QUIT:
            running=False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running=False
            if event.key == pygame.K_s:
                pygame.image.save(drawing_surface, "gesturing.png")
            if event.key == pygame.K_u: 
                if previous_gesture == Gesture.NONE: 
                    if canvas_gestures and allow_undo: 
                        allow_undo = False
                        canvas_gestures.pop(-1) # remove last gesture image
                        timer = threading.Timer(0.5, reset_allow_undo) # wait 0.5 seconds before allowing another gesture to be recognized
                        timer.start()
            if event.key == pygame.K_c:
                if canvas_gestures:
                    drawing_gesture_current = Position(DRAWING_SURFACE_WIDTH / 2, DRAWING_SURFACE_HEIGHT / 2)
                    drawing_gesture_previous = copy(drawing_gesture_current)
                    camera_gesture_previous = copy(camera_gesture_current)
                    canvas_gestures[-1].position = copy(drawing_gesture_current)
    
    success, frame = cap.read()
    if not success: 
        print("can't get camera")
        break
    frame = cv2.flip(frame, 1)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    detection_result = detector.relay(frame)
    if not detection_result.hand_landmarks and previous_gesture != Gesture.NONE:
        gesture_lost = True

    frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
    frame = cv2.flip(frame, 0)
    camera_surface = pygame.surfarray.make_surface(frame)
    camera_surface = pygame.transform.scale(camera_surface, (CAMERA_SURFACE_WIDTH, CAMERA_SURFACE_HEIGHT))
    screen.blit(camera_surface, CAMERA_SURFACE_PLACEMENT)

    screen.blit(drawing_surface, DRAWING_SURFACE_PLACEMENT)
    drawing_surface.fill((255, 255, 255))
    pygame.draw.rect(drawing_surface, (218, 165, 32), (0, 0, DRAWING_SURFACE_WIDTH, DRAWING_SURFACE_HEIGHT), width=10) # fill drawing surface with white
    for gesture_image in canvas_gestures:
        drawing_surface.blit(gesture_image.image, gesture_image.position.tuple())

    if detection_result.hand_landmarks: 
        for hand_landmark in detection_result.hand_landmarks: 
            if isGesture(hand_landmark, Gesture.CONFIRM): # if it's not a gesture other than itself, NONE, or CONFIRM, it'll pass
                previous_gesture = Gesture.NONE # reset current gesture to NONE, which eans the only way to get OUT of a gesture is through this CONFIRM
                # stamps image
                camera_gesture_previous = copy(camera_gesture_current)
                drawing_gesture_previous = copy(drawing_gesture_current)
                # which eans the only way to get OUT of a gesture is through this CONFIRM

            if isGesture(hand_landmark, Gesture.YAY): 
                if previous_gesture == Gesture.NONE: 
                    start_gesture(Gesture.YAY, hand_landmark, YAYGestureImage)
                elif previous_gesture == Gesture.YAY: # itself
                    update_active_gesture(hand_landmark)

            if isGesture(hand_landmark, Gesture.PALM):
                if previous_gesture == Gesture.NONE: 
                    start_gesture(Gesture.PALM, hand_landmark, PALMGestureImage)
                elif previous_gesture == Gesture.PALM: # itself
                    update_active_gesture(hand_landmark)

            if isGesture(hand_landmark, Gesture.THREE): 
                if previous_gesture == Gesture.NONE: 
                    start_gesture(Gesture.THREE, hand_landmark, THREEGestureImage)
                elif previous_gesture == Gesture.THREE: # itself
                    update_active_gesture(hand_landmark)

            if isGesture(hand_landmark, Gesture.ONE):
                if previous_gesture == Gesture.NONE: 
                    start_gesture(Gesture.ONE, hand_landmark, ONEGestureImage)
                elif previous_gesture == Gesture.ONE: # itself
                    update_active_gesture(hand_landmark)

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

"""if gesture_lost:
                        gesture_lost = False
                        camera_gesture_previous = Position(hand_landmark[0].x * CAMERA_SURFACE_WIDTH, hand_landmark[0].y * CAMERA_SURFACE_HEIGHT)
                        drawing_gesture_previous = copy(drawing_gesture_current)

                    camera_gesture_current = Position(hand_landmark[0].x * CAMERA_SURFACE_WIDTH, hand_landmark[0].y * CAMERA_SURFACE_HEIGHT)
                    camera_gesture_offset = camera_gesture_current - camera_gesture_previous

                    drawing_gesture_offset = Position(camera_gesture_offset.x / CAMERA_SURFACE_WIDTH * DRAWING_SURFACE_WIDTH, camera_gesture_offset.y / CAMERA_SURFACE_HEIGHT * DRAWING_SURFACE_HEIGHT)

                    drawing_gesture_current = (drawing_gesture_previous + drawing_gesture_offset).clamp(0, DRAWING_SURFACE_WIDTH, 0, DRAWING_SURFACE_HEIGHT)

                    canvas_gestures[-1].position = copy(drawing_gesture_current)"""
"""previous_gesture = Gesture.PALM
                    gesture_lost = False
                    camera_gesture_previous = Position(hand_landmark[0].x * CAMERA_SURFACE_WIDTH, hand_landmark[0].y * CAMERA_SURFACE_HEIGHT)
                    drawing_gesture_previous = copy(drawing_gesture_current)
                    canvas_gestures.append(GestureImage(PALMGestureImage, drawing_gesture_previous))"""