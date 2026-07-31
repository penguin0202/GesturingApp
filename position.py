class Position:
    def __init__(self, x: float = 0, y: float = 0):
        self.x: float = x
        self.y: float = y
    def __add__(self, other: "Position"):
        return Position(x=self.x + other.x, y=self.y + other.y)
    def __sub__(self, other: "Position"):
        return Position(x=self.x - other.x, y=self.y - other.y)
    def __mul__(self, scalar: float):
        return Position(x=self.x * scalar, y=self.y * scalar)
    def __truediv__(self, scalar: float):
        return Position(x=self.x / scalar, y=self.y / scalar)
    def clamp(self, x_min, x_max, y_min, y_max):
        def _clamp(value, min, max): 
            if value < min: value = min
            if value > max: value = max
            return value
        self.x = _clamp(self.x, x_min, x_max)
        self.y = _clamp(self.y, y_min, y_max)
        return self
    def tuple(self): 
        return (self.x, self.y)