from enum import Enum

class MountainType(Enum): 
    SHARP = 0
    STRETCHED = 1

class Drawing(): 
    def __init__(self, draw_surface): 
        self.draw_surface = draw_surface
    def spawn_mountain(self, x: int, z: int, type: MountainType): 
        pass
    def spawn_tree(self, x, z): 
        pass