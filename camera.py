import cv2

cap = cv2.VideoCapture(0)

def init_camera(width, height): 
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

def camera_opened(): 
    return cap.isOpened()

def get_camera_frame(): 
    success, frame = cap.read()
    if not success: return success, frame
    return success, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # auto RGB frame conversion; byebye BGR