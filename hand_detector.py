import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

class HandDetector: 
    def __init__(self, task: str): 
        base_options = python.BaseOptions(model_asset_path=task)
        options = vision.HandLandmarkerOptions(base_options=base_options, num_hands=1)
        self.detector = vision.HandLandmarker.create_from_options(options)
    def relay(self, frame): # auto converts frame into mediapipe-usable Image
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
        return self.detector.detect(mp_image)