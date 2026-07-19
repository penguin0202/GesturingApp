from enum import Enum, auto

class Gesture(Enum): 
    NONE = auto()
    CONFIRM = auto() # fist
    YAY = auto()
    ONE = auto()
    PALM = auto()
    #THREE_SIDE = auto()
    #THREE_MIDDLE = auto()
    #PINKY = auto()

def isGesture(hand_landmark, gesture: Gesture): 
    if gesture == Gesture.NONE: raise Exception("cannot pass NONE into this field")
    if gesture == Gesture.YAY: #check yay
        pass
    if gesture == Gesture.ONE: #check one
        pass
    if gesture == Gesture.PALM: # check palm
        pass




# helper: 
def finger_up(landmarks, tip, pip):
    return landmarks[tip].y < landmarks[pip].y

def isStandingOnLegsSign(hand_landmark): 
    return False

def isHaltSign(hand_landmark): 
    return False

def isBackHandSign(hand_landmark): 
    return False

isOneSignAlready = False
def isOneSign(hand_landmark): 
    global isOneSignAlready
    index_up = finger_up(hand_landmark, 8, 6)
    middle_up = finger_up(hand_landmark, 12, 10)
    ring_up = finger_up(hand_landmark, 16, 14)
    pinky_up = finger_up(hand_landmark, 20, 18)

    result = (
        index_up
        and middle_up
        and not ring_up
        and not pinky_up
    )

    if result and isOneSignAlready: return False
    if result and not isOneSignAlready: 
        isOneSignAlready = True
        return True
    if not result: 
        isOneSignAlready = False
        return False

def isThumbingLeftSign(hand_landmark): 
    return False

def isThumbingRightSign(hand_landmark): 
    return False

def isThumbingUpSign(hand_landmark): 
    return False

def isThumbingDownSign(hand_landmark): 
    return False