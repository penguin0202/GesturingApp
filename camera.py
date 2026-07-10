import cv2

class Camera: 
    def __init__(self, width, height): 
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    def opened(self): 
        return self.cap.isOpened()
    def get_frame(self): 
        success, frame = self.cap.read()
        frame = cv2.flip(frame, 1)
        if not success: return success, frame
        return success, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # auto RGB frame conversion; byebye BGR
    def release(self): 
        self.cap.release()