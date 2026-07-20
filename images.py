from dataclasses import dataclass
import pygame

@dataclass
class GestureImage():
    image: pygame.Surface

    @property
    def position(self) -> pygame.Rect: 
        return self.image.get_rect()

YAYGestureImage = GestureImage(pygame.image.load("YAYGesture.png").convert_alpha())
ONEGestureImage = GestureImage(pygame.image.load("ONEGesture.png").convert_alpha())
PALMGestureImage = GestureImage(pygame.image.load("PALMGesture.png").convert_alpha())

