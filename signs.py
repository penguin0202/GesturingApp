from enum import Enum, auto

class Finger(Enum): 
    THUMB = auto()
    INDEX = auto()
    MIDDLE = auto()
    RING = auto()
    PINKY = auto()

class Gesture(Enum): 
    NONE = auto()
    CONFIRM = auto() # fist
    YAY = auto()
    ONE = auto()
    PALM = auto()
    THREE = auto()
    PINKY = auto()
    #THREE_SIDE = auto()
    #THREE_MIDDLE = auto()
    #PINKY = auto()

def _distance(a, b):
    return ((a.x - b.x) ** 2 + (a.y - b.y) ** 2 + (a.z - b.z) ** 2) ** 0.5

def _cosine_between(v1, v2):
    dot = v1[0] * v2[0] + v1[1] * v2[1] + v1[2] * v2[2]
    mag1 = (v1[0] ** 2 + v1[1] ** 2 + v1[2] ** 2) ** 0.5
    mag2 = (v2[0] ** 2 + v2[1] ** 2 + v2[2] ** 2) ** 0.5
    if mag1 == 0 or mag2 == 0:
        return 1.0
    return dot / (mag1 * mag2)

def finger_up(landmarks, finger: Finger):
    if finger == Finger.THUMB:
        tip, pip, mcp = landmarks[4], landmarks[2], landmarks[1]
    elif finger == Finger.INDEX:
        tip, pip, mcp = landmarks[8], landmarks[6], landmarks[5]
    elif finger == Finger.MIDDLE:
        tip, pip, mcp = landmarks[12], landmarks[10], landmarks[9]
    elif finger == Finger.RING:
        tip, pip, mcp = landmarks[16], landmarks[14], landmarks[13]
    elif finger == Finger.PINKY:
        tip, pip, mcp = landmarks[20], landmarks[18], landmarks[17]
    else:
        raise Exception("how the hell did you get here")

    tip_pip = _distance(tip, pip)
    pip_mcp = _distance(pip, mcp)
    tip_mcp = _distance(tip, mcp)

    if pip_mcp < 1e-6:
        return False

    v1 = (pip.x - mcp.x, pip.y - mcp.y, pip.z - mcp.z)
    v2 = (tip.x - pip.x, tip.y - pip.y, tip.z - pip.z)
    alignment = _cosine_between(v1, v2)

    return (
        tip_mcp > pip_mcp
        and tip_pip > 0.6 * pip_mcp
        and alignment > 0.7
    )

def isGesture(landmarks, gesture: Gesture): 
    if gesture == Gesture.NONE: raise Exception("cannot pass NONE into this field")
    if gesture == Gesture.YAY: #check yay
        return (
            finger_up(landmarks, Finger.INDEX)
            and finger_up(landmarks, Finger.MIDDLE)
            and not finger_up(landmarks, Finger.RING)
            and not finger_up(landmarks, Finger.PINKY)
        )
    if gesture == Gesture.ONE: #check one
        return (
            finger_up(landmarks, Finger.INDEX)
            and not finger_up(landmarks, Finger.MIDDLE)
            and not finger_up(landmarks, Finger.RING)
            and not finger_up(landmarks, Finger.PINKY)
        )
    if gesture == Gesture.PALM: # check palm
        return (
            finger_up(landmarks, Finger.INDEX)
            and finger_up(landmarks, Finger.MIDDLE)
            and finger_up(landmarks, Finger.RING)
            and finger_up(landmarks, Finger.PINKY)
        )
    if gesture == Gesture.CONFIRM: # check confirm
        return (
            not finger_up(landmarks, Finger.INDEX)
            and not finger_up(landmarks, Finger.MIDDLE)
            and not finger_up(landmarks, Finger.RING)
            and not finger_up(landmarks, Finger.PINKY)
        )
    if gesture == Gesture.THREE: # check three
        return (
            not finger_up(landmarks, Finger.INDEX)
            and finger_up(landmarks, Finger.MIDDLE)
            and finger_up(landmarks, Finger.RING)
            and finger_up(landmarks, Finger.PINKY)
        )
    raise Exception("what else could it be")